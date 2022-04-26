
from backend.blockchain.block import Block
import pandas as pd

from backend.tests.blockchain.test_block import last_block
class Blockchain:
    """
    Blockchain: a public ledger(book) of transactions.
    Implemented as a list of blocks - data sets of transactions
    """
    def __init__(self):
        self.chain = [Block.genesis()] #chain is a list that has all blocks in it, the first element is generated manually because a block should have a manually setted up last_hash value

    def add_block(self, data):
        self.chain.append(Block.mine_block(self.chain[-1], data)) # adding a new node to the chain

    def __repr__(self): #a structured string representation of instances, instead of memory location
        return pd.DataFrame([t.__dict__ for t in self.chain]).to_string()
    
    @staticmethod
    def is_valid_chain(chain):
        """
        Validate the incoming chain with the rules below:
            - the chain must start with the genesis block
            - blocks must be formatted correctly
        """
        for i,block in enumerate(chain):
            if i == 0: #for the genesis block(chain[0]), there is no previous block to check, we check if it's true
                if block != Block.genesis():
                    #print(block, Block.genesis())
                    raise Exception("The genesis block must be valid")
            else:
                last_block = chain[i-1]
                Block.is_valid_block(last_block, block)

def main(): #for testing purposes
    blockchain = Blockchain()
    blockchain.add_block('one')
    blockchain.add_block('two')

    print(blockchain)
    print(f'blockchain.py __name__: {__name__}')

if __name__ == '__main__': #only works when the file directly executed, preventing to work when another module uses this class
    main()