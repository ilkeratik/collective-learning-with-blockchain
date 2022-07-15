class TransactionPool:
    def __init__(self):
        self.transaction_map = {}

    def set_transaction(self, transaction):
        """
        Set a transaction in the transaction pool.
        """
        self.transaction_map[transaction.id] = transaction
    
    def is_transaction_exists_by_tx_id(self, transaction_id):
        """
        Check if a transaction_id exists in the transaction pool map
        and return transaction if found.
        """
        if transaction_id in self.transaction_map:
            return self.transaction_map[transaction_id]
    
    def is_transaction_exists_by_address(self, address):
        """
        Check if a address exists in the transaction pool map ['address']
        and return transaction if found.
        """
        for transaction in self.transaction_map.values():
            if address in transaction.input['address'] == address:
                return transaction

    def transaction_data(self):
        """
        Return the transactions of the transaction pool represented in their
        json serialized form.
        """
        return list(map(
            lambda transaction: transaction.to_dict(),
            self.transaction_map.values()
        ))

    def clear_blockchain_transactions(self, blockchain):
        """
        Delete blockchain recorded transactions from the transaction pool.
        """
        for block in blockchain.chain:
            for transaction in block.data:
                try:
                    del self.transaction_map[transaction['id']]
                except KeyError:
                    pass