from backend.message.msg_template import Message
from backend.message.model_msg import ModelMessage 
import json
class TaskMessage(Message):
    def __init__(self, id, timestamp, public_key,
    owner_address, model, min_validator,evaluation_metrics):
        super().__init__(id, timestamp, public_key)
        self.owner_address = owner_address
        if type(model) is dict:
            if 'header' in model:
                self.model = ModelMessage.from_message_dict(model)
            else:
                self.model = ModelMessage.from_dict(model)
        else:
            self.model = model
        self.min_validator = min_validator
        self.evaluation_metrics = evaluation_metrics
    
    def to_dict(self):
        dictx = {}
        dictx['header'] = super().to_dict()
        dictx['data'] = {
                'model': self.model,
                'owner_address': self.owner_address,
                'min_validator': self.min_validator,
                'evaluation_metrics': self.evaluation_metrics
        }
        return self.to_dict_json(dictx)

    def to_dict_json(self, obj):
        return json.loads(json.dumps(obj, default=lambda o: o.__dict__))

    @staticmethod
    def from_dict(dictx):
        return TaskMessage(**dictx)

    @staticmethod
    def from_message_dict(dictx):
        header = dictx['header']
        data = dictx['data']
        data.update(header)
        return TaskMessage(**data)
    
