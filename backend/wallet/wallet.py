import uuid
import json
from backend.config import STARTING_BALANCE
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec #elliptic curve
from cryptography.exceptions import InvalidSignature
class Wallet:
    """
    An individual wallet for miners.
    Keeps track of miner assets.
    Allows a miner to authorize transactions.
    """
    def __init__(self):
        self.address = str(uuid.uuid4())[0:8]
        self.balance = STARTING_BALANCE
        self.private_key = ec.generate_private_key(ec.SECP256K1(), #the one bitcoin uses
        default_backend) 
        self.public_key = self.private_key.public_key()
        
    def sign(self, data):
        """
        Generate a signature based on given data using private key.
        """
        return self.private_key.sign(
            json.dumps(data).encode('utf-8'), 
            ec.ECDSA(hashes.SHA256()))
    @staticmethod 
    def verify(public_key, data, signature):
        """
        Verify a signature based on the public key and data
        """
        try:
            public_key.verify(signature, 
                json.dumps(data).encode('utf-8'), 
                ec.ECDSA(hashes.SHA256())
            )
            return True
        except InvalidSignature:
            return False

def main():
    wall = Wallet()
    print(f'wallet.__dict__: {wall.__dict__}')

    data = {'weights': [1.1, 3.4]}
    signature = wall.sign(data)
    print(f'signature: {signature}')

    valid_ex = wall.verify(wall.public_key, data, signature)
    print(f'valid_ex: {valid_ex}')

    data['weights']=[0.0, 0]
    invalid_ex = wall.verify(wall.public_key, data, signature)
    print(f'invalid_ex: {invalid_ex}')

    data = {'weights': [1.1, 3.4]}
    invalid_ex = wall.verify(Wallet().public_key, data, signature)
    print(f'invalid_ex2: {invalid_ex}')
    
if __name__ == '__main__':
    main()
