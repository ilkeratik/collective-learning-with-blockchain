import requests
from backend.blockchain.blockchain import Blockchain
from backend.blockchain.model_blockchain import ModelBlockchain
from backend.message.task_msg import TaskMessage
from backend.message.train_msg import TrainMessage
from backend.message.validation_msg import ValidationMessage
ROOT_PORT = 5000

def sync_blockchain(blockchain):
    res = requests.get(f'http://localhost:{ROOT_PORT}/api/blockchain') #sync latest blockchain
    print(f'result: {res.json()}')

    res_blockchain = Blockchain.from_json(res.json())
    try:
        blockchain.replace_chain(res_blockchain.chain)
        print('\n -- Successfully synchronized the local chain')
    except Exception as e:
        print(f'Error when syncing: {e}')

    return res

def sync_model_blockchain(model_blockchain):
    res = requests.get(f'http://localhost:{ROOT_PORT}/api/model-blockchain') #sync latest model blockchain
    res_blockchain = ModelBlockchain.from_json(res.json())
    try:
        model_blockchain.replace_chain(res_blockchain.chain)
        print('\n -- Successfully synchronized the local chain')
    except Exception as e:
        print(f'Error when syncing: {e}')

    print(f'Synced model_blockchain to : {res.json()}')

def sync_transaction_pool(transaction_pool):
    res = requests.get(f'http://localhost:{ROOT_PORT}/api/transaction-pool') #sync latest transaction pool
    res = res.json()
    for transaction in res:
        transaction_pool.set_transaction(transaction['id'])

    print(f'Synced transaction_pool to : {res}')

def sync_task_pool(task_pool):
    res = requests.get(f'http://localhost:{ROOT_PORT}/api/task-pool') #sync latest task pool
    res = res.json()
    for task in res:
        task_msg = TaskMessage.from_dict(task)
        task_pool.add_to_pool(task_msg)

    print(f'Synced task_pool to : {res}')

def sync_training_pool(training_pool):
    res = requests.get(f'http://localhost:{ROOT_PORT}/api/train-pool') #sync latest training pool
    res = res.json()
    for train in res:
        train_msg = TrainMessage.from_dict(train)
        training_pool.add_to_pool(train_msg)

    print(f'Synced training_pool to : {res}')

def sync_validation_pool(validation_pool):
    res = requests.get(f'http://localhost:{ROOT_PORT}/api/validation-pool') #sync latest validation pool
    res = res.json()
    for validate in res:
        validation_msg = ValidationMessage.from_dict(validate)
        validation_pool.add_to_pool(validation_msg)

    print(f'Synced validation_pool to : {res}')

