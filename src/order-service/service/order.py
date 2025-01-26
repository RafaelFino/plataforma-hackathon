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

logger = logging.getLogger('uvicorn.debug')

class OrderService:
    def __init__(self, customer_client: CustomerClient, product_client: ProductClient):
        self.customer_client = customer_client
        self.product_client = product_client
        self.order_storage = OrderStorage()

    def create_order(self, customer_id: int) -> int:
        ret = None
        try:
            logger.debug(f"[ORDER-SERVICE] Trying to create order from customer_id: {customer_id}")
            customer = self.customer_client.load(customer_id)

            if customer is None:
                logging.error(f"[ORDER-SERVICE] Customer not found: {customer_id}")
                return None
            
            ret = self.order_storage.create_order(customer_id)
            logger.info(f"[ORDER-SERVICE] Order create succefully! ID:{ret}")
        
        except Exception as ex:
            logger.error(f"[ORDER-SERVICE] Fail to crete order: {ex}")

        return ret
    
    def add_product(self, order_id: int, product_id: int, price: float, quantity: int) -> int:
        ret = None

        try:
            logger.debug("[ORDER-SERVICE] Trying to add product to order -> order_id:{order_id} product_id: {product_id} quantity: {quantity}")
            product = self.product_client.load(product_id)

            if product is None:
                logging.error(f"[ORDER-SERVICE] Product not found: {product_id}")
                return None

            order = self.order_storage.get(order_id)

            if order is None:
                logging.error(f"[ORDER-SERVICE] Order not found: {order_id}")
                return None

            ret = self.order_storage.add_item(order_id, product_id, price, quantity)
            logger.info(f"[ORDER-SERVICE] Adding product to Order succefully! ID:{ret}")
        except Exception as ex:
            logger.error(f"[ORDER-SERVICE] Fail to add item to order: {ex}")

        return ret
    
    def remove_product(self, item_id: int) -> bool:
        ret = False 

        try:
            logger.debug(f"[ORDER-SERVICE] Trying to remove item from order ID:{item_id}")
            
            ret = self.order_storage.delete_item(item_id)
            logger.info(f"[ORDER-SERVICE] Item removed from order succefully! ID:{item_id}")
        except Exception as ex:
            logger.error(f"[ORDER-SERVICE] Fail to remove item from order: {ex}")

        return ret
    
    def get_order(self, order_id: int) -> OrderDomain:
        ret = None
        
        try:
            logger.debug("[ORDER-SERVICE] Trying to load order ID:{order_id}")
            ret = self.order_storage.get(order_id)

            if ret is None:
                logging.error(f"[ORDER-SERVICE] Order not found: {order_id}")
                return None
            
            customer_info = self.customer_client.get(ret.customer_id)
            ret.add_customer_info(customer_info)

            for product_id in ret.products:
                product_info = self.product_client.get(product_id)
                ret.add_product_info(product_info)

            logger.info("[ORDER-SERVICE] Geted order succefully!")
        except Exception as ex:
            logger.error(f"[ORDER-SERVICE] Fail to load order: {ex}")

        return ret
    
    def get_all_from_customer(self, customer_id: int) -> list:
        logger.debug("[ORDER-SERVICE] Trying to load all customers orders")
        ret = []

        try:
            ret = self.order_storage.get_all_from_customer(customer_id)

            logger.info("[ORDER-SERVICE] All customer orders are loadesd!")
        except Exception as ex:
            logger.error(f"[ORDER-SERVICE] Fail to load all orders from customer: {ex}")

        return ret
