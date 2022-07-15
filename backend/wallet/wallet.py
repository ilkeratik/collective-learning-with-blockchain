import uuid
import json
from backend.config import STARTING_BALANCE
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec #elliptic curve
from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature, decode_dss_signature
from cryptography.exceptions import InvalidSignature
class Wallet:
    """
    An individual wallet for miners.
    Keeps track of miner assets.
    Allows a miner to authorize transactions.
    """
    
    def __init__(self, address=None, private_key=None, blockchain=None):
        self.blockchain = blockchain
        if address and private_key and blockchain.reverse():
            
            for block in blockchain[:,-1]:
                for tx in block.data:
                    if tx['input']['address'] == address:
                        public_key = tx['input']['public_key']
                        if private_key.public_key() == public_key:
                            self.address = address
                            self.balance = tx['output'][address]
                            self.private_key=private_key
                            self.public_key=self.private_key.public_key()
                            print('Found and loaded wallet from blockchain with the address and private_key')
                            break
        else:
            self.address = str(uuid.uuid4())[0:8]
            #self.balance = STARTING_BALANCE
            self.private_key = ec.generate_private_key(ec.SECP256K1(), #the one bitcoin uses
            default_backend) 
            self.public_key = self.private_key.public_key()
            self.public_key
            self.serialize_public_key()
            
    @property
    def balance(self):
        return Wallet.calculate_wallet_balance(self.blockchain, self.address)
        
    def sign(self, data):
        """
        Generate a signature based on given data using private key.
        """
        return decode_dss_signature(self.private_key.sign(
            json.dumps(data).encode('utf-8'), 
            ec.ECDSA(hashes.SHA256()))
        )
    @staticmethod 
    def verify(public_key, data, signature):
        """
        Verify a signature based on the public key and data
        """
        deserialized_public_key = serialization.load_pem_public_key(
            public_key.encode('utf-8'),
            default_backend()
        )
        (r, s) = signature
        try:
            deserialized_public_key.verify(
                encode_dss_signature(r,s),
                json.dumps(data).encode('utf-8'), 
                ec.ECDSA(hashes.SHA256())
            )
            return True
        except InvalidSignature:
            return False

    @staticmethod
    def login_to_wallet(private_key):
        """
        Login to a wallet using a private key.
        """
        deserialized_private_key = serialization.load_pem_private_key(
            private_key.encode('utf-8'),
            password=None,
            backend=default_backend()
        )
        return Wallet(deserialized_private_key)

    def serialize_public_key(self):
        """
        Serialize the public key.
        """
        self.public_key = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')

    @staticmethod
    def calculate_wallet_balance(blockchain, address):
        """
        Calculate balance of the given address considering the transaction data within the blockchain.
        
        """
        balance = STARTING_BALANCE
        for block in blockchain.chain:
            for transaction in block.data:
                if transaction['input']['address'] == address:
                    #In any transaction, sender publishes its current balance in the output.
                    balance = transaction['output'][address]
                elif address in transaction['output']:
                    balance += transaction['output'][address]
        return balance
    
def main(): 
    wall = Wallet()
    print(f'wallet.__dict__: {wall.__dict__}')

    data = {'weights': [1.1, 3.4]}
    signatured_data = wall.sign(data)
    print(f'signatured data: {signatured_data}')

    valid_ex = wall.verify(wall.public_key, data, signatured_data)
    print(f'valid_ex: {valid_ex}')

    data['weights']=[0.0, 0]
    invalid_ex = wall.verify(wall.public_key, data, signatured_data)
    print(f'invalid_ex: {invalid_ex}')

    data = {'weights': [1.1, 3.4]}
    invalid_ex = wall.verify(Wallet().public_key, data, signatured_data)
    print(f'invalid_ex2: {invalid_ex}')
    
if __name__ == '__main__':
    main()
