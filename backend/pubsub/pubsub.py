from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from backend.secrets import *
from backend.pubsub.listener import *

from backend.message.train_msg import *
from backend.message.validation_msg import *
from backend.message.task_msg import *

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


class PubSub:
    def __init__(self, uuid):
        self.pubnub = PubNub(pn_conf)
            
    def publish(self, channel, message):
        """
        Publishes a message to given channel
        """
        self.pubnub.publish().channel(channel).message(message).sync()


class MinerPubSub(PubSub):
    def __init__(self, blockchain, train_pool, validation_pool, uuid=None):
        super().__init__(uuid)
        self.train_pool = train_pool
        self.validation_pool = validation_pool
        self.pubnub.subscribe().channels(['TRAIN', 'VALIDATE', 'MODEL_BLOCK']).execute()
        self.pubnub.add_listener(MinerListener(blockchain, train_pool, validation_pool))

    def broadcast_model_block(self, transaction):
        """
        Broadcast a model update to model update pool.
        """
        self.publish(CHANNELS['MODEL_BLOCK'], transaction)
    
    def broadcast_validation(self, ValidationMessage):
        """
        Broadcast a validation message to validation pool.
        """
        self.publish(CHANNELS['VALIDATE'], ValidationMessage.to_dict())

class TrainerPubSub(PubSub):
    def __init__(self, blockchain, task_pool, train_pool, uuid=None):
        super().__init__(uuid)
        self.pubnub.subscribe().channels(['TASK', 'TRAIN', 'MODEL_BLOCK']).execute()
        self.pubnub.add_listener(TrainerListener(blockchain, task_pool, train_pool))

    def broadcast_training(self, TrainMessage):
        """
        Broadcast a training to training pool.
        """
        self.publish(CHANNELS['TRAIN'], TrainMessage.to_dict())

class ValidatorPubSub(PubSub):
    def __init__(self, blockchain, train_pool, validation_pool, uuid=None):
        super().__init__(uuid)
        self.pubnub.subscribe().channels(['TRAIN', 'VALIDATE','MODEL_BLOCK']).execute()
        self.pubnub.add_listener(ValidatorListener(blockchain, train_pool, validation_pool))

    def broadcast_validation(self, ValidationMessage):
        """
        Broadcast a validation message to validation pool.
        """
        self.publish(CHANNELS['VALIDATE'], ValidationMessage.to_dict())

class RootPubSub(PubSub):
    """
    Handles the pub/sub layer of the application.
    Provides communication between the nodes of the blockchain network.
    """
    def __init__(self, blockchain, task_pool=None, train_pool=None, 
    validation_pool=None, transaction_pool=None, uuid=None):
        super().__init__(uuid)
        self.pubnub.subscribe().channels(CHANNELS.values()).execute()
        self.pubnub.add_listener(RootListener(blockchain, 
        task_pool, train_pool, validation_pool, transaction_pool))
            
    def publish(self, channel, message):
        """
        Publishes a message to given channel
        """
        self.pubnub.publish().channel(channel).message(message).sync()

    def broadcast_block(self, block):
        """
        Broadcast a block object to all nodes.
        """
        self.publish(CHANNELS['BLOCK'], block.to_dict())
    
    def broadcast_transaction(self, transaction):
        """
        Broadcast a transaction to all nodes.
        """
        
        self.publish(CHANNELS['TRANSACTION'], transaction.to_dict())
    
    def broadcast_task(self, TaskMessage):
        """
        Broadcast a task to task pool.
        """
        self.publish(CHANNELS['TASK'], TaskMessage.to_dict())

    def broadcast_validation(self, ValidationMessage):
        """
        Broadcast a validation message to validation pool.
        """
        self.publish(CHANNELS['VALIDATE'], ValidationMessage.to_dict())
    
    def broadcast_training(self, TrainMessage):
        """
        Broadcast a training to training pool.
        """
        self.publish(CHANNELS['TRAIN'], TrainMessage.to_dict())

    def broadcast_model_block(self, ModelBlock):
        """
        Broadcast a model update to model update pool.
        """
        self.publish(CHANNELS['MODEL_BLOCK'], ModelBlock)
    

def main():
    pbs = PubSub()
    pbs.publish(CHANNELS['TEST'], {'FOO': 'BAR'})


if __name__ == '__main__':
    main()