import logging
from domain.order import OrderDomain
from storage.order import OrderStorage
from client.customer import CustomerClient
from client.product import ProductClient

# Crie uma instância para o Storage
# Inclua mensagens de log para todas as funções
#   - Para funções que alteram o estado do domínio, inclua mensagens de log antes e depois da alteração (logs de info!)
#   - Para funções que não alteram o estado do domínio, inclua mensagens de log apenas no início da função (logs de debug!)
# Faça todas as chamadas para a storage
# Insira controler de Try/Except para todas as funções e logs nos casos de Exception usando logging.error
# Fiquem atentos as URLs dos serviços remotos caso tentem rodar em máquinas diferentes!

class OrderService:
    def __init__(self, customer_client: CustomerClient, product_client: ProductClient):
        self.customer_client = customer_client
        self.product_client = product_client
        self.order_storage = OrderStorage()

    def create_order(self, customer_id: int) -> int:
        customer = self.customer_client.get()

        if customer is None:
            logging.error(f"[ORDER-SERVICE] Customer not found: {customer_id}")
            return None
        
        order_id = self.order_storage.add(customer_id)
        return order_id
    
    def add_product(self, order_id: int, product_id: int) -> int:
        product = self.product_client.get(product_id)

        if product is None:
            logging.error(f"[ORDER-SERVICE] Product not found: {product_id}")
            return None

        order = self.order_storage.get(order_id)

        if order is None:
            logging.error(f"[ORDER-SERVICE] Order not found: {order_id}")
            return None

        item_id = self.order_storage.update(order)

        return item_id
    
    def remove_product(self, order_id: int, product_id: int) -> bool:
        # TODO
        # Valide a ordem e o produto
        return False
    
    def get_order(self, order_id: int) -> OrderDomain:
        order = self.order_storage.get(order_id)

        if order is None:
            logging.error(f"[ORDER-SERVICE] Order not found: {order_id}")
            return None
        
        customer_info = self.customer_client.get(order.customer_id)
        order.add_customer_info(customer_info)

        for product_id in order.products:
            product_info = self.product_client.get(product_id)
            order.add_product_info(product_info)

        return order
    
    def get_all_from_customer(self, customer_id: int) -> list:
        # TODO
        return None