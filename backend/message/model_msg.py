class ModelMessage:
    def __init__(self, id, name, description, data_path, parameters, latest_gradient=None, current_metrics=None, contributors=None):
        self.id = id
        self.name = name
        self.description = description
        self.data_path = data_path
        self.parameters = parameters
        self.latest_gradient = latest_gradient
        self.current_metrics = current_metrics
        self.contributors = contributors
    
    def to_dict(self):
        dict = {
            'header' : {
                'id': self.id,
                'name': self.name,
                'description': self.description
            },
            'data': {
                'data_path': self.data_path,
                'parameters': self.parameters,
                'latest_gradient': self.latest_gradient,
                'current_metrics': self.current_metrics,
                'contributors': self.contributors
            }
        }
        return dict

    def raw_dict(self):
        return self.__dict__
    @staticmethod
    def from_dict(dict):
        return ModelMessage(**dict)

    @staticmethod
    def from_message_dict(dictx):
        header = dictx['header']
        data = dictx['data']
        data.update(header)
        return ModelMessage(**data)
        
    def add_contributor(self, contributor):
        if self.contributors is None:
            self.contributors = []
        self.contributors.append(contributor)