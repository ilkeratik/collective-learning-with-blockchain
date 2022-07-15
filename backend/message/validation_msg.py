from backend.message.msg_template import Message

class ValidationMessage(Message):
    def __init__(self, id, timestamp, public_key, train_id,
    validator_address, sub_trained_examples, gradient_vector, metrics, bet_amount):
        super().__init__(id, timestamp, public_key)
        self.train_id = train_id
        self.validator_address = validator_address
        self.sub_trained_examples = sub_trained_examples
        self.gradient_vector = gradient_vector
        self.metrics = metrics
        self.bet_amount = bet_amount
    
    def to_dict(self):
        dictx = {}
        dictx['header'] = super().to_dict()
        dictx['data'] = {
                'train_id': self.train_id,
                'validator_address': self.validator_address,
                'sub_trained_examples': self.sub_trained_examples,
                'gradient_vector': self.gradient_vector,
                'metrics': self.metrics,
                'bet_amount': self.bet_amount,
            }
        return dictx

    @staticmethod
    def from_dict(dictx):
        return ValidationMessage(**dictx)

    @staticmethod
    def from_message_dict(dictx):
        header = dictx['header']
        data = dictx['data']
        data.update(header)
        return ValidationMessage(**data)