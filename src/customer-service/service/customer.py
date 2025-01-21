import logging
from domain.customer import CustomerDomain
from storage.customer import CustomerStorage

# Crie uma instância para o Storage
# Inclua mensagens de log para todas as funções
#   - Para funções que alteram o estado do domínio, inclua mensagens de log antes e depois da alteração (logs de info!)
#   - Para funções que não alteram o estado do domínio, inclua mensagens de log apenas no início da função (logs de debug!)
# Faça todas as chamadas para a storage
# Insira controler de Try/Except para todas as funções e logs nos casos de Exception usando logging.error
logger = logging.getLogger('uvicorn.error')

class CustomerService:
    def __init__(self):
        self.storage = CustomerStorage()
        logger.info("[CUSTOMER-SERVICE] Service initialized")

    def add(self, customer: CustomerDomain) -> int:
        # TODO
        return None

    def update(self, customer: CustomerDomain) -> bool:
        # TODO
        return

    def delete(self, id) -> bool:
        # TODO
        return

    def get(self, id) -> CustomerDomain:
        # TODO
        return None

    def get_all(self) -> list:
        # TODO
        return None