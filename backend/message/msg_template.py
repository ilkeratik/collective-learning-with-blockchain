class Message:
    def __init__(self, id, timestamp, public_key):
        self.id = id
        self.timestamp = timestamp
        self.public_key = public_key
    
    def to_dict(self):
        return {'id': self.id,
                'timestamp': self.timestamp, 
                'public_key': self.public_key}
        
    @staticmethod
    def from_dict(dict):
        return Message(**dict)
    