import json

class CustomerDomain:
    def __init__(self, json_data: str = None, customer_id: int = None, name: str = None, email: str = None):
        if json_data is None:
            self.customer_id = customer_id
            self.name = name
            self.email = email
        else:
            self.from_json(json_data)

    def from_json(self, json_data: str):
        data = json.loads(json_data)
        self.customer_id = data['customer_id']
        self.name = data['name']
        self.email = data['email']        

    def __str__(self):
        return f'Customer ID: {self.customer_id}, Name: {self.name}, Email: {self.email}'
    
    def to_dict(self):
        return {
            'customer_id': self.customer_id,
            'name': self.name,
            'email': self.email
        }