import logging
from domain.product import ProductDomain
from storage.product import ProductStorage

# Crie uma instância para o Storage
# Inclua mensagens de log para todas as funções
#   - Para funções que alteram o estado do domínio, inclua mensagens de log antes e depois da alteração (logs de info!)
#   - Para funções que não alteram o estado do domínio, inclua mensagens de log apenas no início da função (logs de debug!)

class ProductService:
    def __init__(self):
        self.storage = ProductStorage()
        logging.info("[PRODUCT-SERVICE] Service initialized")        

    def add(self, product: ProductDomain) -> int:
        # TODO
        return None

    def update(self, product: ProductDomain) -> bool:
        # TODO
        return None

    def delete(self, product_id: int) -> bool:
        # TODO
        return None
    
    def get(self, product_id: int) -> ProductDomain:
        # TODO
        return None    
    
    def get_all(self):
        # TODO
        return None