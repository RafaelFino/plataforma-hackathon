import logging
import sqlite3
from domain.customer import CustomerDomain

# Escreva os comandos SQL para as funções add, get, get_all, update e delete
# Escreva as mensagens de log para todos os comandos que alteram o estado do domínio
logger = logging.getLogger('uvicorn.debug')

class CustomerStorage:
    def __init__(self):        
        self.conn = sqlite3.connect("customer-database.sqlite", check_same_thread=False)
        self.__create()
        logger.debug("[CUSTOMER-STORAGE] Storage initialized")

    def __create(self):
        if self.conn is None:
            logging.error(f"[CUSTOMER-STORAGE] Connection error!")

        c = self.conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL
            );
        ''')
        self.conn.commit()

    def add(self, customer: CustomerDomain) -> int:
        logger.info("[CUSTOMER-STORAGE] Add")
        c = self.conn.cursor()
        c.execute('''
            INSERT INTO customers (name, email) VALUES (?, ?)
        ''', (customer.name, customer.email))

        self.conn.commit()
        
        return c.lastrowid
   
    def update(self, customer: CustomerDomain) -> bool:
        logger.info("[CUSTOMER-STORAGE] Update")
        c = self.conn.cursor()
        c.execute('''
            UPDATE customers SET name = ?, email = ? WHERE id = ?
        ''', (customer.name, customer.email, customer.customer_id))

        self.conn.commit()

        return c.rowcount > 0

    def delete(self, id) -> bool:
        logger.info("[CUSTOMER-STORAGE] Delete")
        c = self.conn.cursor()
        c.execute('''
            DELETE FROM customers WHERE id = ?
        ''', (id,))

        self.conn.commit()  

        return c.rowcount > 0      

    def get(self, id: int) -> CustomerDomain:
        logger.debug("[CUSTUMER-STORAGE] Load")
        c = self.conn.cursor()
        c.execute('''
            SELECT 
                id,
                name,
                email
            FROM 
                customers 
            WHERE id = ?
        ''', (id,))
        customer = c.fetchone()
        logger.info(f"[CUSTOMER-STORAGE] Data: {customer}")
        ret = CustomerDomain(customer[1], customer[2])
        ret.set_id(customer[0])

        return ret
    
    def get_all(self) -> list:
        logger.debug("[CUSTOMER-STORAGE] Load users")
        c = self.conn.cursor()
        c.execute('''
            SELECT 
                id,
                name,
                email
            FROM 
                customers 
        ''')
        customers = c.fetchall()
        ret = []

        for customer in customers:
            logger.debug(f"[CUSTOMER-STORAGE] data: {customer}")
            item = CustomerDomain(customer[1], customer[2])
            item.set_id(customer[0])
            ret.append(item)

        return ret