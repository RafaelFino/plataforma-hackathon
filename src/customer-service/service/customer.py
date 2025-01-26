import logging
from domain.customer import CustomerDomain
from storage.customer import CustomerStorage

# Crie uma instância para o Storage
# Inclua mensagens de log para todas as funções
#   - Para funções que alteram o estado do domínio, inclua mensagens de log antes e depois da alteração (logs de info!)
#   - Para funções que não alteram o estado do domínio, inclua mensagens de log apenas no início da função (logs de debug!)
# Faça todas as chamadas para a storage
# Insira controler de Try/Except para todas as funções e logs nos casos de Exception usando logging.error


logger = logging.getLogger('uvicorn.debug')

class CustomerService:
    def __init__(self):
        self.storage = CustomerStorage()
        logger.info("[CUSTOMER-SERVICE] Service initialized")

    def add(self, customer: CustomerDomain) -> int:
        ret = None

        try:
            ret = self.storage.add(customer)
            logger.info("[CUSTOMER-SERVICE] User added")
        except Exception as e:
            logger.error(f"[CUSTOMER-SERVICE] Error to add user: {e}")    
        
        return ret
        
    def update(self, customer: CustomerDomain) -> bool:
        ret = False
        
        try:
            ret = self.storage.update(customer)
            logger.info("[CUSTOMER-SERVICE] User updated")
        except Exception as e:
            logger.error(f"[CUSTOMER-SERVICE] Error to update user: {e}") 
        
        return ret

    def delete(self, id) -> bool:
        ret = False
        
        try:
            ret = self.storage.delete(id)
            logger.info("[CUSTOMER-SERVICE] User deleted")
        except Exception as e:
            logger.error(f"[CUSTOMER-SERVICE] Error to delete user: {e}") 
        
        return ret

    def get(self, id: int) -> CustomerDomain:
        ret = None

        try:
            ret = self.storage.get(id)
            logger.debug("[CUSTOMER-SERVICE] User loaded")
        except Exception as e:
            logger.error(f"[CUSTOMER-SERVICE] Error to load user: {e}") 

        return ret

    def get_all(self) -> list:
        ret = []
    
        try:
            ret = self.storage.get_all()
            logger.debug("[CUSTOMER-SERVICE] all users catched")
        except Exception as e:
            logger.error(f"[CUSTOMER-SERVICE] Error to load all users: {e}")     

        return ret