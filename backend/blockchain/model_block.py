import time, json
from backend.bc_utils.crypto_hash import crypto_hash
from backend.config import MINE_RATE
from backend.bc_utils.hex_to_binary import hex_to_binary

GENESIS_DATA = {
    'timestamp': 1,
    'last_hash': 'ISMIHAN ILKER ATIK',
    'hash': 'genesis_hash',
    'nonce': 1,
    'data': {
        'task_id': 1,
        'contributors': {'trainer': 1, 
                        'validators': [1,2], 
                        'miner': 1},
        'model_update': {'source': 1, 
                        'gradient_vector': [1], 
                        'parameters': {'W1':0, 'W2':0, 'b1':0, 'b2':0}, 
                        'metrics': {'loss': 1}
                        },
    }
}

class ModelBlock:
    """
    Block: a unit of storage.
    """
    def __init__(self, timestamp, last_hash, hash, data, nonce=None):
        self.timestamp = timestamp #creating time
        self.last_hash = last_hash #hash of the block just before this block
        self.hash = hash 
        self.data = data
        self.nonce = nonce or 1

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    def __repr__(self): # string representation of the class
        return (
            'Block('
            f'timestamp: {self.timestamp}, '
            f'last_hash: {self.last_hash}, '
            f'hash: {self.hash}, '
            f'nonce: {self.nonce})'
            f'data: {self.data})'
        )

    def to_dict(self):
        """
        Convert-Serialize the block into a dict of its attributes.
        """
        return self.__dict__

    @staticmethod
    def from_dict(dict):
        """
        Turn json or dict to block object, Deserialize dict to block
        """
        return ModelBlock(**dict)
    

    @staticmethod
    def create_block(last_block, data): # create a block
        """
        Mine and validate a block based on the given last_block and data.
        """
        last_hash = last_block.hash
        nonce = last_block.nonce + 1
        timestamp = time.time_ns()
        hash = crypto_hash(timestamp, last_hash, data, nonce)
        
        return ModelBlock(timestamp, last_hash, hash, data, nonce)

    @staticmethod
    def mine_block(last_block, data): # create a block
        """
        Mine and validate a block based on the given last_block and data.
        """
        last_hash = last_block.hash
        nonce = last_block.nonce + 1
        timestamp = time.time_ns()
        data = json.loads(json.dumps(data, default=lambda o: o.tolist()))
        hash = crypto_hash(timestamp, last_hash, data, nonce)
        
        return ModelBlock(timestamp, last_hash, hash, data, nonce)

    @staticmethod
    def create_model_block_data(parameters, latest_gradient, contributors, min_validator, training_eval):
        return {
            'parameters': parameters,
            'latest_gradient': latest_gradient,
            'contributors': contributors,
            'min_validator': min_validator,
            'training_eval': training_eval
        }

    @staticmethod
    def genesis():
        """
        Generate the genesis block.
        """
        return ModelBlock(**GENESIS_DATA)

    @staticmethod
    def is_valid_block(last_block, block):
        """
        Validate:
            - the block must have the proper last_hash reference
            - the block hash must be a valid combination of the block field
        """

        if block.last_hash != last_block.hash:
            raise Exception("The block last_hash must be correct")
        
        # if hex_to_binary(block.hash)[0:block.difficulty] != '0' * block.difficulty:
        #     raise Exception("PoW requirement was not meet")
        
        # if abs(last_block.difficulty - block.difficulty) > 1:
        #     raise Exception("The block difficulty must only adjust by 1")

        reconstructed_hash = crypto_hash(
            block.timestamp,
            block.last_hash,
            block.data,
            block.nonce
        )
        if block.hash != reconstructed_hash:
            print(block.hash, reconstructed_hash)
            raise Exception("The block hash must be correct")
