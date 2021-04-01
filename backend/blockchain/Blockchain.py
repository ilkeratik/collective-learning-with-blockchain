
from backend.blockchain.block import Block

class Blockchain:
    """
    Blockchain: a public ledger(book) of transactions.
    Implemented as a list of blocks - data sets of transactions
    """
    def __init__(self):
        self.chain = [Block.genesis()] #chain is a list that has all blocks in it, the first element is generated manually because a block should have a manually setted up last_hash value

    def add_block(self, data):
        self.chain.append(Block.mine_block(self.chain[-1], data)) # adding a new node to the chain

    def __repr__(self): #a structured representation of instances, instead of memory location
        return f'Blockchain: {self.chain}'

def main(): #for testing purposes
    blockchain = Blockchain()
    blockchain.add_block('one')
    blockchain.add_block('two')

    print(blockchain)
    print(f'blockchain.py __name__: {__name__}')

if __name__ == '__main__': #only works when the file directly executed, preventing to work when another module uses this class
    main()