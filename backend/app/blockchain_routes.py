from flask import Flask, jsonify, request

from backend.blockchain.blockchain import Blockchain
from backend.blockchain.model_blockchain import ModelBlockchain
from backend.message.task_msg import TaskMessage
from backend.message.train_msg import TrainMessage
from backend.message.model_msg import ModelMessage 
from backend.wallet.wallet import Wallet
from backend.wallet.transaction import Transaction
from backend.wallet.transaction_pool import TransactionPool

from backend.pool.task_pool import TaskPool
from backend.pool.train_pool import TrainPool
from backend.pool.validation_pool import ValidationPool

import  backend.learning.utils as l_util

pubsub = None
blockchain = Blockchain()
model_blockchain = ModelBlockchain()
wallet = Wallet(blockchain=model_blockchain)
transaction_pool = TransactionPool()
task_pool = TaskPool()
train_pool = TrainPool()
validation_pool = ValidationPool()

def set_pubsub(pubsuba):
    global pubsub
    pubsub = pubsuba
app = Flask(__name__)
@app.route('/')
def index():
    return 'The beginning of everything'

@app.route('/test')
def test():
    return 'Ilker'

@app.route('/blockchain')
def route_view_blockchain():
    df = blockchain.chain_df()
    return df.to_html()

@app.route('/api/blockchain')
def route_json_blockchain():
    return jsonify(blockchain.to_json())


# @app.route('/api/blockchain/mine/<data>', methods=[ 'GET' ])
# def route_mine_block_get(data):
#     try:
#         blockchain.add_block(data)

#         block = blockchain.chain[-1]
#         print(pubsub)
#         pubsub.broadcast_block(block)
#         return f'Successfully added block to blockchain, data={data}'
#     except Exception as e:
#         return e, 500


@app.route('/api/blockchain/mine', methods=[ 'POST', 'GET' ])
def route_mine_block():
    try:
        transaction_data = transaction_pool.transaction_data()
        print(transaction_data)
        transaction_data.append(Transaction.reward_transaction(wallet).to_dict())
        blockchain.add_block(transaction_data)
        block = blockchain.chain[-1]
        pubsub.broadcast_block(block)
        transaction_pool.clear_blockchain_transactions(blockchain)

        return jsonify(block.to_dict())
    except Exception as e:
        return e, 500

@app.route('/api/wallet/transact', methods=[ 'POST' ])
def route_wallet_transact():
    tx_data = request.get_json()
    transaction = transaction_pool.is_transaction_exists_by_address(wallet.address)
    if transaction:
        transaction.update(wallet,
                           tx_data['recipient'],
                           tx_data['amount'])
    else:
        transaction = Transaction(wallet, 
                                tx_data['recipient'], 
                                tx_data['amount'])
    
    pubsub.broadcast_transaction(transaction)
    return jsonify(transaction.to_dict()) 

@app.route('/api/transactions')
def route_transactions():
    return jsonify(transaction_pool.transaction_data())

@app.route('/api/wallet/info')
def route_wallet_info():
    return jsonify({ 'address': wallet.address, 'balance': wallet.balance })

@app.route('/api/known-addresses')
def route_known_addresses():
    known_addresses = set()

    for block in blockchain.chain:
        for transaction in block.data:
            known_addresses.update(transaction['output'].keys())
    return jsonify(list(known_addresses))

####### MODEL BLOCKCHAIN ROUTES #######
#-------------------------------------#
@app.route('/api/model-blockchain')
def route_json_model_blockchain():
    print(model_blockchain.to_json())
    return jsonify(model_blockchain.to_json())

@app.route('/api/task-pool')
def route_task_pool():
    return jsonify(task_pool.pool_data())

@app.route('/api/train-pool')
def route_train_pool():
    return jsonify(train_pool.pool_data())

@app.route('/api/validation-pool')
def route_validation_pool():
    return jsonify(validation_pool.pool_data())

@app.route('/api/model-blockchain/task/add', methods=[ 'POST' ])
def route_add_task():
    print('Started adding task')
    data_json = request.get_json()
    task_msg = TaskMessage.from_message_dict(data_json)
    pubsub.broadcast_task(task_msg)
    print('\nSuccessful task addition and broadcast')
    
    return jsonify(task_msg.to_dict())

@app.route('/api/model-blockchain/train/add', methods=[ 'POST' ])
def route_add_train():
    print('Started train addition')
    data_json = request.get_json()
    train_msg = TrainMessage.from_message_dict(data_json)
    pubsub.broadcast_training(train_msg)
    print('\nSuccessful train and broadcast')
    return jsonify(train_msg.to_dict())

@app.route('/api/model-blockchain/validation/add', methods=[ 'POST' ])
def route_add_validation():
    print('Started validation addition')
    data_json = request.get_json()
    validation_msg = TrainMessage.from_message_dict(data_json)
    pubsub.broadcast_validation(validation_msg)
    print('\nSuccessful validation and broadcast')
    return jsonify(validation_msg.to_dict())

@app.route('/api/model-blockchain/train')
def route_model_train():
    print('Started training')
    last_task_data = task_pool.pool_data()[-1]
    task_msg = TaskMessage.from_message_dict(last_task_data)
    train_msg = l_util.training(wallet, task_msg)
    pubsub.broadcast_training(train_msg)
    print('\nSuccessful train and broadcast')
    return jsonify(train_msg.to_dict())

@app.route('/api/model-blockchain/validate')
def route_model_validate():
    print('Started validation')
    last_train_data = train_pool.pool_data()[-1]
    train_msg = TrainMessage.from_message_dict(last_train_data)
    task_msg = task_pool.pool_map[train_msg.task_id]
    valid_msg = l_util.validation(wallet, task_msg, train_msg)
    pubsub.broadcast_validation(valid_msg)
    print('\nSuccessful validation and broadcast')
    return jsonify(valid_msg.to_dict())

@app.route('/api/model-blockchain/create-block')
def route_model_create_block():
    print('Started creating block')
    last_train_data = train_pool.pool_data()[-1]
    train_msg = TrainMessage.from_message_dict(last_train_data)
    task_msg = task_pool.pool_map[train_msg.task_id]
    block = l_util.create_block(wallet, model_blockchain, train_msg, task_msg, validation_pool.pool_data())
    #print(block)
    pubsub.broadcast_model_block(block)
    print('\nSuccessful block creation and broadcast')
    return jsonify(block.to_dict())