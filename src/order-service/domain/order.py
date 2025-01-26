from domain.customer import CustomerInfoDomain
from domain.product import ProductInfoDomain
from datetime import datetime

class OrderDomain:
    def __init__(self, customer_id: int):
        self.customer_id = customer_id
        self.items = []
        self.created_at = datetime.now().strftime('%Y%m%d %H%M%S')

    def set_id(self, order_id: int):
        self.order_id = order_id

    def set_created_at(self, created_at: str):
        self.created_at = created_at

    def add_customer_info(self, customer_info: CustomerInfoDomain):
        self.customer_info = customer_info

    def add_item(self, item_id, product_id, price: float, quantity: float):
        self.items.append(OrderItemDomain(item_id=item_id, product_id=product_id, price=price, quantity=quantity))

    def to_dict(self):
        return {
            'order_id': self.order_id,
            'customer_id': self.customer_id,
            'customer_info': self.customer_info.to_dict(),
            'items': [item.to_dict() for item in self.items],
            'created_at': self.created_at,
            'total': self.total()
        }
    
    def total(self):
        return sum([item.total() for item in self.items])
    
class OrderItemDomain:
    def __init__(self, item_id: int, product_id: int, price: float, quantity: float):
        self.item_id = item_id
        self.product_id = product_id
        self.price = price
        self.quantity = quantity

    def add_product_info(self, product_info: ProductInfoDomain):
        self.product_info = product_info

    def to_dict(self):
        return {
            'item_id': self.item_id,
            'product_id': self.product_id,
            'product_info': self.product_info.to_dict(),
            'price': self.price,
            'quantity': self.quantity,
            'total': self.total()
        }
    
    def total(self):
        return self.price * self.quantity