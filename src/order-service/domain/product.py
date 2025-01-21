import json

class ProductInfoDomain:
    def __init__(self, json_data: str): 
        data = json.loads(json_data)
        self.name = data['name']
        self.price = data['price']

    def to_dict(self):
        return {
            'name': self.name,
            'price': self.price
        }