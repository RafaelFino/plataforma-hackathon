import json

class ProductDomain:
    def __init__(self, json_data: str = None, product_id: int = None, name: str = None, price: float = None): 
        if json_data is None:
            self.product_id = product_id
            self.name = name
            self.price = price
        else:
            self.from_json(json_data)
        
    def from_json(self, json_data: str):
        data = json.loads(json_data)
        self.product_id = data['product_id']
        self.name = data['name']
        self.price = data['price']

    def to_dict(self):
        return {
            'product_id': self.product_id,
            'name': self.name,
            'price': self.price
        }