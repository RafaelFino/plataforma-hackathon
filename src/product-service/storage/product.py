import logging
import sqlite3
from domain.product import ProductDomain

# Escreva os comandos SQL para as funções add, get, get_all, update e delete
# Escreva as mensagens de log para todos os comandos que alteram o estado do domínio

class ProductStorage:
    def __init__(self):
        self.conn = sqlite3.connect("product-database.sqlite", check_same_thread=False)
        self.__create()
        logging.debug("[PRODUCT-STORAGE] Storage initialized")

    def __create(self):
        if self.conn is None:
            logging.error(f"[PRODUCT-STORAGE] Connection error!")

        c = self.conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS prodcut (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL                  
            )
        ''')
        self.conn.commit()

    def add(self, product: ProductDomain) -> int:
        c = self.conn.cursor()
        c.execute('''
            // FAÇA SEU SQL AQUI
        ''', (product.name, product.price))

        self.conn.commit()

        return c.lastrowid
    
    def update(self, product: ProductDomain) -> bool:
        c = self.conn.cursor()
        c.execute('''
            //FAÇA SEU SQL AQUI
        ''', (product.name, product.price, product.product_id))

        self.conn.commit()

        return c.rowcount > 0
    
    def delete(self, id) -> bool:
        c = self.conn.cursor()
        c.execute('''
            //FAÇA SEU SQL AQUI
        ''', (id,))

        self.conn.commit()  

        return c.rowcount > 0
    
    def get(self, id) -> ProductDomain:
        c = self.conn.cursor()
        c.execute('''
            //FAÇA SEU SQL AQUI
        ''', (id,))
        
        row = c.fetchone()
        if row is None:
            return None

        return ProductDomain(row[0], row[1], row[2])
    
    def get_all(self) -> list:
        c = self.conn.cursor()
        c.execute('''
            //FAÇA SEU SQL AQUI
        ''')
        products = c.fetchall()
        ret = []
        for product in products:
            ret.append(ProductDomain(product[0], product[1], product[2]))

        return ret
    
    