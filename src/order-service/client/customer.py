import logging
import requests
import http
from domain.customer import CustomerInfoDomain

logger = logging.getLogger('uvicorn.debug')

class CustomerClient:
    def __init__(self, customer_service_url: str = "http://localhost:8001"):
        self.customer_service_url = customer_service_url
        self.cache = {}
        logger.info("[CUSTOMER-CLIENT] Client initialized")

    def load(self, customer_id: int) -> CustomerInfoDomain:        
        try:
            if customer_id in self.cache:
                return self.cache[customer_id]

            logging.info(f"[CUSTOMER-CLIENT] Loading customer {customer_id} from {self.customer_service_url}")
            r = requests.get(f'{self.customer_service_url}/customer/{customer_id}')
            if r.status_code == http.HTTPStatus.OK:
                data = r.json()
                ret = CustomerInfoDomain(data['customer']['name'], data['customer']['email'])
                self.cache[customer_id] = ret
                return ret
            else:
                logging.error(f"[CUSTOMER-CLIENT] Customer {customer_id} not found")
        
        except Exception as e:
            logging.error(f"[CUSTOMER-CLIENT] Error loading customer {customer_id}: {e}")
        
        return None
    
    def reset_cache(self):
        self.cache = {}
        logging.info("[CUSTOMER-CLIENT] Cache reset")