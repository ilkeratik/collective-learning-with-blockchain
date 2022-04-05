import time

from backend.bc_utils.crypto_hash import crypto_hash
import pandas as pd
GENESIS_DATA = {
    'timestamp': 1,
    'last_hash': 'genesis_last_hash',
    'hash': 'genesis_hash',
    'data': []
}

class Block:
    """
    Block: a unit of storage.
    Store transactions in a blockchain that supports a cryptocurrency.
    """
    def __init__(self, timestamp, last_hash, hash, data):
        self.timestamp = timestamp #creating time
        self.last_hash = last_hash #hash of the block just before this block
        self.hash = hash 
        self.data = data

    def add_block(self, data):
        self.chain.append(Block(data))

    def __repr__(self): # string representation of the class
        return (
            'Block('
            f'timestamp: {self.timestamp}, '
            f'last_hash: {self.last_hash}, '
            f'hash: {self.hash}, '
            f'data: {self.data})'
        )

    @staticmethod #gets load when the class is imported and could work directly
    def mine_block(last_block, data): # create a block
        """
        Mine a block based on the given last_block and data.
        """
        timestamp = time.time_ns()
        last_hash = last_block.hash
        hash = crypto_hash(timestamp, last_hash, data) 

        return Block(timestamp, last_hash, hash, data)

    @staticmethod
    def genesis():
        """
        Generate the genesis block.
        """
        # return Block(
        #     timestamp=GENESIS_DATA['timestamp'],
        #     last_hash=GENESIS_DATA['last_hash'],
        #     hash=GENESIS_DATA['hash'],
        #     data=GENESIS_DATA['data']
        # )
        return Block(**GENESIS_DATA) #unpacks the dictionary and passes values as parameter with their original order

def main():
    genesis_block = Block.genesis()
    block = Block.mine_block(genesis_block, 'foo')
    print(f'block: {block}')

if __name__ == '__main__':
    main()