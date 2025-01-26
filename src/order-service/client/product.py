import logging
import requests
import http
import json
from domain.product import ProductInfoDomain

logger = logging.getLogger('uvicorn.debug')

class ProductClient:
    def __init__(self, product_service_url: str = "http://localhost:8002"):
        self.product_service_url = product_service_url
        self.cache = {}
        logger.info("[PRODUCT-CLIENT] Client initialized")

    def load(self, product_id: int) -> ProductInfoDomain:        
        try:
            logger.info(f"[PRODUCT-CLIENT] Trying to load product ID:{product_id}")
            if product_id in self.cache:
                return self.cache[product_id]

            logging.info(f"[CUSTOMER-CLIENT] Loading customer {product_id} from {self.product_service_url}")
            r = requests.get(f'{self.product_service_url}/product/{product_id}')
            if r.status_code == http.HTTPStatus.OK:
                logger.debug(f"[CUSTOMER-CLIENT] Data loaded from ID {product_id} -> {r.text}")
                data = r.json()
                ret = ProductInfoDomain(data["product"]["name"], data["product"]["price"])
                logger.debug(f"[PRODUCT-CLIENT] Add item to cache: {product_id}")
                self.cache[product_id] = ret
                return ret
            else:
                logging.error(f"[PRODUCT-CLIENT] Product {product_id} not found")
        
        except Exception as e:
            logging.error(f"[PRODUCT-CLIENT] Error loading product {product_id}: {e}")
        
        return None
    
    def reset_cache(self):
        self.cache = {}
        logging.info("[PRODUCT-CLIENT] Cache reset")