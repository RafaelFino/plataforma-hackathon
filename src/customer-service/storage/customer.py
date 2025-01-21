import logging
import sqlite3
from domain.customer import CustomerDomain

# Escreva os comandos SQL para as funções add, get, get_all, update e delete
# Escreva as mensagens de log para todos os comandos que alteram o estado do domínio

class CustomerStorage:
    def __init__(self):
        self.conn = sqlite3.connect("customer-database.sqlite", check_same_thread=False)
        self.__create()
        logging.debug("[CUSTOMER-STORAGE] Storage initialized")

    def __create(self):
        if self.conn is None:
            logging.error(f"[CUSTOMER-STORAGE] Connection error!")

        c = self.conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def add(self, customer: CustomerDomain) -> int:
        c = self.conn.cursor()
        c.execute('''
            // FAÇA SEU SQL AQUI
        ''', (customer.name, customer.email))

        self.conn.commit()

        return c.lastrowid
   
    def update(self, customer: CustomerDomain) -> bool:
        c = self.conn.cursor()
        c.execute('''
            //FAÇA SEU SQL AQUI
        ''', (customer.name, customer.email, customer.customer_id))

        self.conn.commit()

        return c.rowcount > 0

    def delete(self, id) -> bool:
        c = self.conn.cursor()
        c.execute('''
            //FAÇA SEU SQL AQUI
        ''', (id,))

        self.conn.commit()  

        return c.rowcount > 0      

    def get(self, id) -> CustomerDomain:
        c = self.conn.cursor()
        c.execute('''
            //FAÇA SEU SQL AQUI  
        ''')
        customer = c.fetchone()
        ret = CustomerDomain(customer[1], customer[2])
        ret.set_id(customer[0])

        return ret
    
    def get_all(self) -> list:
        c = self.conn.cursor()
        c.execute('''
            //FAÇA SEU SQL AQUI
        ''')
        customers = c.fetchall()
        ret = []

        for customer in customers:
            customer = CustomerDomain(customer[1], customer[2])
            customer.set_id(customer[0])
            ret.append(customer)

        return ret
