import logging
import sqlite3
from domain.product import ProductDomain

# Escreva os comandos SQL para as funções add, get, get_all, update e delete
# Escreva as mensagens de log para todos os comandos que alteram o estado do domínio
logger = logging.getLogger('uvicorn.debug')

class ProductStorage:
    def __init__(self):
        self.conn = sqlite3.connect("product-database.sqlite", check_same_thread=False)
        self.__create()
        logger.debug("[PRODUCT-STORAGE] Storage initialized")

    def __create(self):
        if self.conn is None:
            logging.error(f"[PRODUCT-STORAGE] Connection error!")

        c = self.conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS product (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL                  
            );
        ''')
        self.conn.commit()

    def add(self, product: ProductDomain) -> int:
        c = self.conn.cursor()
        logger.debug("[PRODUCT-STORAGE] Adding new product")
        c.execute('''
            INSERT INTO product (name, price) VALUES (?, ?);
        ''', (product.name, product.price,))

        logger.info(f"[PRODUCT-STORAGE] Product with name = {product.name} created")

        self.conn.commit()

        return c.lastrowid
    
    def update(self, product: ProductDomain) -> bool:
        c = self.conn.cursor()
        logging.debug("[PRODUCT-STORAGE] Updating a product")
        c.execute('''
            UPDATE product SET name = ?, price = ? WHERE id = ?;
        ''', (product.name, product.price, product.product_id,))

        logging.info(f"PRODUCT-STORAGE] Product with id = {product.product_id} updated")
        self.conn.commit()

        return c.rowcount > 0
    
    def delete(self, id) -> bool:
        c = self.conn.cursor()
        logger.debug("[PRODUCT-STORAGE] Deleting product")
        c.execute('''
            DELETE FROM product WHERE id = ?;
        ''', (id,))

        logger.info(f"[PRODUCT-STORAGE] Product with id = {id} deleted")
        self.conn.commit()  

        return c.rowcount > 0
    
    def get(self, id) -> ProductDomain:
        c = self.conn.cursor()
        logger.debug("[PRODUCT-STORAGE] Getting product by id")
        c.execute('''
            SELECT
                id,
                name,
                price
            FROM 
                product 
            WHERE id = ?;
        ''', (id,))

        row = c.fetchone()
        if row is None:
            return None

        ret = ProductDomain(row[1], row[2])
        ret.set_id(row[0])

        return ret
    
    def get_all(self) -> list:
        c = self.conn.cursor()
        logging.debug("[PRODUCT-STORAGE] Getting all products")
        c.execute('''
             SELECT
                id,
                name,
                price
            FROM 
                product;
        ''')
        products = c.fetchall()
        ret = []
        for product in products:
            item = ProductDomain(product[1], product[2])
            item.set_id(product[0])
            ret.append(item)

        return ret
    
