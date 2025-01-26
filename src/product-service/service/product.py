import logging
from domain.product import ProductDomain
from storage.product import ProductStorage

# Crie uma instância para o Storage
# Inclua mensagens de log para todas as funções
#   - Para funções que alteram o estado do domínio, inclua mensagens de log antes e depois da alteração (logs de info!)
#   - Para funções que não alteram o estado do domínio, inclua mensagens de log apenas no início da função (logs de debug!)
# Faça todas as chamadas para a storage
# Insira controler de Try/Except para todas as funções e logs nos casos de Exception usando logging.error
logger = logging.getLogger('uvicorn.debug')

class ProductService:
    def __init__(self):
        self.storage = ProductStorage()
        logger.info("[PRODUCT-SERVICE] Service initialized")        
    
    def add(self, product: ProductDomain) -> int:
        ret = None
        
        try:
            ret = self.storage.add(product)
            logger.info("[PRODUCT-SERVICE] Insert product")
        except Exception as e:
            logger.error(f"[PRODUCT-SERVICE] Fail to add product - Exception: {e}")
        
        return ret

    def update(self, product: ProductDomain) -> bool:
        ret = False
        
        try:
            ret = self.storage.update(product)
            logger.info("[PRODUCT-SERVICE] Update product")
        except Exception as e:
            logger.error(f"[PRODUCT-SERVICE] Fail to update product - Exception: {e}")
            
        return ret

    def delete(self, product_id: int) -> bool:
        ret = False

        try:
            ret = self.storage.delete(product_id)
            logger.info("[PRODUCT-SERVICE] Delete product")
        except Exception as e:
            logger.error(f"[PRODUCT-SERVICE] Fail to delete product - Exception: {e}")
            
        return ret
    
    def get(self, product_id: int) -> ProductDomain:
        ret = None

        try:            
            ret = self.storage.get(product_id)            
            logger.debug("[PRODUCT-SERVICE] Get product")
        except Exception as e:
            logger.error(f"[PRODUCT-SERVICE] Fail to load product - Exception: {e}")
        
        return ret
    
    def get_all(self):
        ret = []

        try:    
            ret = self.storage.get_all()
            logger.debug("[PRODUCT-SERVICE] Get all products")
        except Exception as e:
            logger.error(f"[PRODUCT-SERVICE] Fail to load all users - Exception: {e}")
        
        return ret
