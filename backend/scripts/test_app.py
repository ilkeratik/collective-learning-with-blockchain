
import requests
import time, json
from backend.message.model_msg import ModelMessage
from backend.message.task_msg import TaskMessage
from backend.message.train_msg import TrainMessage
from backend.message.validation_msg import ValidationMessage
from backend.wallet.wallet import Wallet
from backend.learning.utils import *
BASE_URL = 'http://localhost:5000'

TRAINER_URL = 'http://localhost:5000'
VALIDATOR_URL = 'http://localhost:5000'
VALIDATOR_URL2 = 'http://localhost:5000'
MINER_URL = 'http://localhost:5000'
def get_blockchain():
    return requests.get(f'{BASE_URL}/api/blockchain').json()

def get_blockchain_mine():
    return requests.get(f'{BASE_URL}/api/blockchain/mine').json()   

def post_wallet_transact(recipient, amount): 
    return requests.post(
        f'{BASE_URL}/api/wallet/transact',
        json={ 'recipient': recipient, 'amount': amount }
    ).json()

def get_wallet_info():
    return requests.get(f'{BASE_URL}/api/wallet/info').json()

def get_transactions():
        return requests.get(f'{BASE_URL}/api/transactions').json()

def initialize_parameters(n_x, n_h, n_y):
        """
        Argument:
        n_x -- size of the input layer
        n_h -- size of the hidden layer
        n_y -- size of the output layer
        
        Returns:
        params -- python dictionary containing your parameters:
                        W1 -- weight matrix of shape (n_h, n_x)
                        b1 -- bias vector of shape (n_h, 1)
                        W2 -- weight matrix of shape (n_y, n_h)
                        b2 -- bias vector of shape (n_y, 1)
        """ 
        #np.random.seed(2)   
        W1 = (np.random.randn(n_h,n_x) * 0.01 ).tolist()
        b1 = (np.zeros((n_h,1))).tolist()
        W2 = (np.random.randn(n_y,n_h) * 0.01).tolist()
        b2 = (np.zeros((n_y,1))).tolist()

        parameters = {"W1": W1,
                    "b1": b1,
                    "W2": W2,
                    "b2": b2}
        return parameters

def publish_task_message():
    parameters = initialize_parameters(31,1,5)
    model_msg = ModelMessage.from_dict({'id':322
                                    , 'name': 'OneHiddenLayerModel'
                                    , 'description': 'Test One hidden layer model to train fraud data'
                                    , 'data_path': 'D:\Desktop\BC\Blockchain_APP\\backend\learning\datasets\\fraud_detection\mini_ds_creditcard.csv'
                                    , 'parameters': parameters
                                    , 'latest_gradient': [0.1,0.2,0.3]
                                    , 'current_metrics': {'loss': 0.4}
                                    ,'contributors': ['ilker_aa']
    })
    
    header={'id':33
            ,'timestamp':1212
            ,'public_key':424242}

    data = {'owner_address': 'ilker_aa'
            ,'model': model_msg.to_dict()
            ,'min_validator': 2
            ,'evaluation_metrics': ['loss']
    }
    task_msg = TaskMessage.from_message_dict({'header': header, 'data': data})
    json_msg = task_msg.to_dict()
    # print(json_msg.keys())
    # print(json_msg.get('header').keys())
    # print(json_msg.get('data').keys())
    # print('\n\n\njson')
    # print(json.dumps(json_msg,
    #   sort_keys=True, indent=4))
    return requests.post(
        f'{BASE_URL}/api/model-blockchain/task/add',
        json= json_msg
    ).json()

def publish_train_message():
    header={'id':33
            ,'timestamp':1212
            ,'public_key':424242}
    
    data = {'task_id':33
            ,'trainer_address': 'ilker_aa'
            ,'examples_list': [1,222,24]
            ,'gradient_vector': {'W1': [0.2,0.23,0.11],
                                "b1": [0],
                                "W2": [0.1,0.2,0.3],
                                "b2": [1]},
            'metrics': {'loss': 0.4}
            ,'bet_amount': 32}
    train_message = TrainMessage.from_message_dict({'header': header, 'data': data})
    json_msg = train_message.to_dict()
    return requests.post(
        f'{TRAINER_URL}/api/model-blockchain/train/add',
        json= json_msg).json()

def publish_validation_message():
    header={'id':33
            ,'timestamp':1212
            ,'public_key':424242}
    
    data = {'train_id':33
            ,'validator_adress': 'vali'
            ,'sub_trained_examples': [1,222,24]
            ,'gradient_vector': {'W1': [0.2,0.23,0.11],
                                "b1": [0],
                                "W2": [0.1,0.2,0.3],
                                "b2": [1]},
            'metrics': {'loss': 0.4}
            ,'bet_amount': 32}
    validation_message = ValidationMessage.from_message_dict({'header': header, 'data': data})
    json_msg = validation_message.to_dict()
    return requests.post(
        f'{VALIDATOR_URL}/api/model-blockchain/validation/add',
        json= json_msg).json()

def train_model():
    return requests.get(f'{TRAINER_URL}/api/model-blockchain/train')

def validate_model(validator_url):
    return requests.get(f'{validator_url}/api/model-blockchain/validate')

def create_model_blockx(miner_url):
    return requests.get(f'{miner_url}/api/model-blockchain/create-block')


res = publish_task_message()
#print('\nresult task')
#print(json.dumps(res,
#      sort_keys=True, indent=3))

time.sleep(1)
res_train = train_model()
time.sleep(1)
res_valid1 = validate_model(VALIDATOR_URL)
time.sleep(1)
res_valid2 = validate_model(VALIDATOR_URL2)
time.sleep(1)
res_create_block = create_model_blockx(MINER_URL)




# start_blockchain = get_blockchain()
# print(f'start_blockchain: {start_blockchain}')

# recipient = Wallet().address
# post_wallet_transact_1 = post_wallet_transact(recipient, 21)
# print(f'\npost_wallet_transact_1: {post_wallet_transact_1}')

# 
# post_wallet_transact_2 = post_wallet_transact(recipient, 13)
# print(f'\npost_wallet_transact_2: {post_wallet_transact_2}')

# time.sleep(1)
# mined_block = get_blockchain_mine()
# print(f'\nmined_block: {mined_block}')

# wallet_info = get_wallet_info()
# print(f'\nwallet_info: {wallet_info}')

# print('========Transactions=========')
# print(get_transactions())


# res = publish_task_message()
# print('\nresult task')
# print(res.keys())
# print(json.dumps(res,
#       sort_keys=True, indent=3))

# res = publish_train_message()

# print('\nresult train')
# print(res.keys())
# print(json.dumps(res,
#       sort_keys=True, indent=3))