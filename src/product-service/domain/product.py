class ProductDomain:
    def __init__(self, product_id: int, name: str, price: float):
        self.product_id = product_id
        self.name = name
        self.price = price

    def __str__(self):
        return f'Product ID: {self.product_id}, Name: {self.name}, Price: {self.price}'
    
    def to_json(self):
        return {
            'product_id': self.product_id,
            'name': self.name,
            'price': self.price
        }