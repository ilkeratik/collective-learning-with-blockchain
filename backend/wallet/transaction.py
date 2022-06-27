import uuid, time
from backend.wallet.wallet import Wallet
class Transaction:
    """
    The Document or ADT of transaction messages.
    """
    def __init__(self, sender_wallet, recipient, amount):
        self.id = str(uuid.uuid4())[0:15]
        
        self.output = self.create_output(
            sender_wallet,
            recipient,
            amount)
        self.input  = self.create_input(sender_wallet, self.output) 

    def create_output(self, sender_wallet, recipient, amount):
        """
        Structure the output data for the transaction.
        """
        if sender_wallet.balance < amount :
            raise Exception('Amount exceeds balance')
        output = {}
        output[recipient] = amount
        output[sender_wallet.address] = sender_wallet.balance - amount

        return output

    def create_input(self, sender_wallet, output):
        """
        Structure the input data for the transaction.
        Signs the transaction and the senders public key and address
        """

        input = {
            'timestamp': time.time_ns(),
            'amount': sender_wallet.balance,
            'address': sender_wallet.address,
            'public_key': sender_wallet.public_key,
            'signature': sender_wallet.sign(output)
        }
        return input

    def update(self, sender_wallet, recipient, amount):
        """
        Update the transaction with an existing or new recipient.
        """
        if amount> self.output[sender_wallet.address]:
            raise Exception('Amount exceeds balance')
        
        if recipient in self.output:
            self.output[recipient] = self.output[recipient] + amount
        else:
            self.output[recipient] = amount
        
        self.output[sender_wallet.address] = self.output[sender_wallet.address] - amount

        self.input = self.create_input(sender_wallet, self.output)

    @staticmethod
    def is_valid_transaction(transaction):
        """
        Validate a transaction.
        Raises an exception for invalid transactions.
        """
        output_total = sum(transaction.output.values())

        if transaction.input['amount'] != output_total:
            raise Exception('Invalid transaction output values')

        if not Wallet.verify(
            transaction.input['public_key'], transaction.output, transaction.input['signature']):
            raise Exception('Invalid signature')


def main():
    wl = Wallet()
    tx = Transaction(wl, 'recipient', 31)

    print(f'transaction.__dict__: {tx.__dict__}')


if __name__ == '__main__':
    main()