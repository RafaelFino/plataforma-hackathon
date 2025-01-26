import json

class ProductInfoDomain:
    def __init__(self, name: str, price: float): 
        self.name = name
        self.price = price

    def to_dict(self):
        return {
            'name': self.name,
            'price': self.price
        }