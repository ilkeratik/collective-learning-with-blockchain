from pubnub.callbacks import SubscribeCallback
from backend.message.task_msg import TaskMessage
from backend.message.train_msg import TrainMessage
from backend.message.validation_msg import ValidationMessage
from backend.secrets import *
from backend.blockchain.block import Block
from backend.wallet.transaction import Transaction
from pubnub.pnconfiguration import PNConfiguration
import copy

pn_conf = PNConfiguration()
pn_conf.subscribe_key = subscribe_key
pn_conf.publish_key = publish_key
pn_conf.uuid = "custom uuid"

CHANNELS = {
    'TEST': 'TEST',
    'BLOCK': 'BLOCK',
    'TRANSACTION': 'TRANSACTION',
    'TASK': 'TASK',
    'TRAIN': 'TRAIN',
    'VALIDATE': 'VALIDATE',
    'MODEL_BLOCK': 'MODEL_BLOCK'
}



class Listener(SubscribeCallback):
    def __init__(self, blockchain, task_pool=None, train_pool=None, validation_pool=None, transaction_pool=None):   
        self.blockchain = blockchain

    def clear_pools_with_blockchain(self, block_data, train_pool, validation_pool):
        """
        Delete blockchain recorded data from the pools.
        """
        #block_data = blockchain.chain[-1].data
        trainer = block_data['contributors']['trainer']
        train_pool.remove_from_pool_by_id(trainer)
        miner = block_data['contributors']['miner']
        validation_pool.remove_from_pool_by_id(miner)
        validators = block_data['contributors']['validators']
        for validator in validators:
            validation_pool.remove_from_pool_by_id(validator)

    
class RootListener(Listener):
    def __init__(self, blockchain, task_pool, train_pool, validation_pool, transaction_pool=None):
        super().__init__(blockchain)
        self.task_pool = task_pool
        self.train_pool = train_pool
        self.validation_pool = validation_pool
        self.transaction_pool = transaction_pool
        self.current_task_id = None

    def message(self, pubnub, message_object):
        print(f'>>> Channel: {message_object.channel}, New message recieved.')

        if message_object.channel == CHANNELS['BLOCK']:

            block = Block.from_dict(message_object.message)
            potential_chain = self.blockchain.chain[:]
            potential_chain.append(block)
            try:
                self.blockchain.replace_chain(potential_chain)
                self.transaction_pool.clear_blockchain_transactions(
                    self.blockchain
                )
                print(f'++ Successfully replaced the local chain')
            except Exception as e:
                print(f'-- Did not replace the chain: {e}')
        
        elif message_object.channel == CHANNELS['MODEL_BLOCK']:
            potential_blockchain = copy.deepcopy(self.blockchain)
            potential_blockchain.add_block(message_object.message)
         
            self.blockchain.replace_chain(potential_blockchain.chain)
            block_data = self.blockchain.chain[-1].data
            #self.clear_pools_with_blockchain(block_data, self.train_pool, self.validation_pool)
            print(f' -- Successfully replaced the local chain and uptaded the pools')
     
        elif message_object.channel == CHANNELS['TRANSACTION']:
            transaction = Transaction.from_message_dict(message_object.message)
            self.transaction_pool.set_transaction(transaction)
            print(f'++ Set transaction in the transaction pool')

        elif message_object.channel == CHANNELS['TRAIN']:
            data = message_object.message
            train_msg = TrainMessage.from_message_dict(data)
            self.train_pool.add_to_pool(train_msg)
            print(f'++ Added new message to train pool')

        elif message_object.channel == CHANNELS['VALIDATE']:
            data = message_object.message
            validation_msg = ValidationMessage.from_message_dict(data)
            self.validation_pool.add_to_pool(validation_msg)
            print(f'++ Added new message to validation pool')

        elif message_object.channel == CHANNELS['TASK']:
            data = message_object.message
            task_msg = TaskMessage.from_message_dict(data)
            self.task_pool.add_to_pool(task_msg)
            print(f'++ Added new message to task pool')


class MinerListener(Listener, SubscribeCallback):
    def __init__(self, blockchain, train_pool, validation_pool):
        super().__init__(blockchain)
        self.train_pool = train_pool
        self.validation_pool = validation_pool
        self.current_task_id = None

    def message(self, pubnub, message_object):
        print(f'>>> Channel: {message_object.channel}, New message recieved.')

        if message_object.channel == CHANNELS['TRAIN']:
            data = message_object.message
            train_msg = TrainMessage.from_message_dict(data)
            self.train_pool.add_to_pool(train_msg)
            print(f'++ Added new message to train pool')

        elif message_object.channel == CHANNELS['VALIDATE']:
            data = message_object.message
            validation_msg = ValidationMessage.from_message_dict(data)
            self.validation_pool.add_to_pool(validation_msg)
            print(f'+ Added new message to validation pool')
        
        elif message_object.channel == CHANNELS['MODEL_BLOCK']:
            copy_blockchain = copy.deepcopy(self.blockchain)
            potential_blockchain = copy_blockchain.add_block(message_object.message)
            try:
                self.blockchain.replace_chain(potential_blockchain.chain)
                self.clear_pools_with_blockchain(self.blockchain, self.train_pool, self.validation_pool)
                print(f' -- Successfully replaced the local chain and uptaded the pools')
            except Exception as e:
                print(f' -- Did not replace the chain: {e}')
            

class TrainerListener(Listener, SubscribeCallback):
    def __init__(self, blockchain, task_pool, train_pool):
        super().__init__(blockchain)
        self.task_pool = task_pool
        self.train_pool = train_pool

    def message(self, pubnub, message_object):
        print(f'>>> Channel: {message_object.channel}, New message recieved.')
        if message_object.channel == CHANNELS['TASK']:
            task_msg = TaskMessage.from_message_dict(message_object.message)
            self.task_pool.add_to_pool(task_msg)
            print(f'++ Added new message to task pool')

        elif message_object.channel == CHANNELS['TRAIN']:
            data = message_object.message
            train_msg = TrainMessage.from_message_dict(data)
            self.train_pool.add_to_pool(train_msg)
            print(f'++ Added new message to train pool')
        
        elif message_object.channel == CHANNELS['MODEL_BLOCK']:
            copy_blockchain = copy.deepcopy(self.blockchain)
            potential_blockchain = copy_blockchain.add_block(message_object.message)
            try:
                self.blockchain.replace_chain(potential_blockchain.chain)
    
                self.clear_pools_with_blockchain(self.blockchain, self.train_pool, self.validation_pool)
                print(f' -- Successfully replaced the local chain and uptaded the pools')
            except Exception as e:
                print(f'-- Did not replace the chain: {e}')
            


class ValidatorListener(Listener, SubscribeCallback):
    def __init__(self, blockchain, train_pool, validation_pool):
        super().__init__(blockchain)
        self.train_pool = train_pool
        self.validation_pool = validation_pool
        self.current_task_id = None

    def message(self, pubnub, message_object):
        print(f'>>> Channel: {message_object.channel}, New message recieved.')
        
        if message_object.channel == CHANNELS['TRAIN']:
            data = message_object.message
            train_msg = TrainMessage.from_message_dict(data)
            self.train_pool.add_to_pool(train_msg)
            print(f'++ Added new message to train pool')

        elif message_object.channel == CHANNELS['VALIDATE']:
            data = message_object.message
            validation_msg = ValidationMessage.from_message_dict(data)
            self.validation_pool.add_to_pool(validation_msg)
            print(f'++ Added new message to validation pool')
        
        elif message_object.channel == CHANNELS['MODEL_BLOCK']:
            copy_blockchain = copy.deepcopy(self.blockchain)
            potential_blockchain = copy_blockchain.add_block(message_object.message)
            try:
                self.blockchain.replace_chain(potential_blockchain.chain)
                self.clear_pools_with_blockchain(self.blockchain, self.train_pool, self.validation_pool)
                print(f' -- Successfully replaced the local chain and uptaded the pools')
            except Exception as e:
                print(f' -- Did not replace the chain: {e}')
            