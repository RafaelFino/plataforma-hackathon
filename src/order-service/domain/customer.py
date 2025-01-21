import json

class CustomerInfoDomain:
    def __init__(self, json_data: str):
        data = json.loads(json_data)
        self.name = data['name']
        self.email = data['email']        
    
    def to_dict(self):
        return {
            'name': self.name,
            'email': self.email
        }