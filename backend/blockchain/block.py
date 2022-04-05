import time
import pandas as pd

from backend.bc_utils.crypto_hash import crypto_hash
from backend.config import MINE_RATE
from backend.bc_utils.hex_to_binary import hex_to_binary
GENESIS_DATA = {
    'timestamp': 1,
    'last_hash': 'genesis_last_hash',
    'hash': 'genesis_hash',
    'data': [],
    'difficulty': 3,
    'nonce': 'genesis_nonce'
}

class Block:
    """
    Block: a unit of storage.
    Store transactions in a blockchain that supports a cryptocurrency.
    """
    def __init__(self, timestamp, last_hash, hash, data, difficulty, nonce):
        self.timestamp = timestamp #creating time
        self.last_hash = last_hash #hash of the block just before this block
        self.hash = hash 
        self.data = data
        self.difficulty = difficulty
        self.nonce = nonce

    def __repr__(self): # string representation of the class
        return (
            'Block('
            f'timestamp: {self.timestamp}, '
            f'last_hash: {self.last_hash}, '
            f'hash: {self.hash}, '
            f'data: {self.data}, '
            f'difficulty: {self.difficulty}, '
            f'nonce: {self.nonce})'
        )

    @staticmethod #gets load when the class is imported and could work directly
    def mine_block(last_block, data): # create a block
        """
        Mine a block based on the given last_block and data, until a block hash is found that
        meets the leading 0's of proof of work requires.
        """
        last_hash = last_block.hash
        nonce = 0
        timestamp, hash, difficulty = None, None, None
        while not hash or hex_to_binary(hash)[0:difficulty] != '0' * difficulty:
            if hash:
                nonce += 1
            timestamp = time.time_ns()
            difficulty = Block.adjust_difficulty(last_block, timestamp)
            hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce)
        
        return Block(timestamp, last_hash, hash, data, difficulty, nonce)

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

    @staticmethod
    def adjust_difficulty(last_block, new_timestamp):
        """
        Calculate and adjust the difficulty according to the MINE_RATE
        """
        threshold = 0.2
        time_diff =new_timestamp - last_block.timestamp
        if time_diff < MINE_RATE + threshold:
            return last_block.difficulty + 1
        elif time_diff > MINE_RATE + threshold and last_block.difficulty > 1:
            return last_block.difficulty -1

        return last_block.difficulty #1


def main():
    genesis_block = Block.genesis()
    block = Block.mine_block(genesis_block, 'foo')
    print(f'block: {block}')

if __name__ == '__main__':
    main()