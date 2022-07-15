
from backend.message.msg_template import Message

class TrainMessage(Message):
    def __init__(self, id, timestamp,public_key, task_id, 
    trainer_address, examples_list, gradient_vector, metrics, bet_amount):
        super().__init__(id, timestamp, public_key)
        self.task_id = task_id
        self.trainer_address = trainer_address
        self.examples_list = examples_list
        self.gradient_vector = gradient_vector
        self.metrics = metrics
        self.bet_amount = bet_amount

    def to_dict(self):
        dictx = {}
        dictx['header'] = super().to_dict()
        dictx['data'] = {
                'task_id': self.task_id,
                'trainer_address': self.trainer_address,
                'examples_list': self.examples_list,
                'gradient_vector': self.gradient_vector,
                'metrics': self.metrics,
                'bet_amount': self.bet_amount,
            }
        
        return dictx


    @staticmethod
    def from_dict(dictx):
        return TrainMessage(**dictx)

    @staticmethod
    def from_message_dict(dictx):
        header = dictx['header']
        data = dictx['data']
        data.update(header)
        return TrainMessage(**data)
