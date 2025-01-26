import logging
import sqlite3
from domain.order import OrderDomain, OrderItemDomain


# Escreva os comandos SQL para as funções add, get, get_all, update e delete
# Escreva as mensagens de log para todos os comandos que alteram o estado do domínio

logger = logging.getLogger('uvicorn.debug')

class OrderStorage:
    def __init__(self):
        self.conn = sqlite3.connect("order-database.sqlite", check_same_thread=False)
        self.__create()
        logger.debug("[ORDER-STORAGE] Storage initialized")

    def __create(self):
        if self.conn is None:
            logger.error(f"[ORDER-STORAGE] Connection error!")

        c = self.conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')          
        c.execute('''
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL REFERENCES orders(id),
                product_id INTEGER NOT NULL,
                price REAL NOT NULL,
                quantity INTEGER NOT NULL
            );
        ''')
        self.conn.commit()

    def create_order(self, customer_id: int) -> int:
        c = self.conn.cursor()
        c.execute('''
            INSERT INTO orders 
                (customer_id)
            VALUES
                (?);
        ''', (customer_id,))

        self.conn.commit()

        id = c.lastrowid

        logger.info(f"[ORDER-STORAGE] Create Order ID:{id}")

        return id
    
    def add_item(self, order_id: int, product_id: int, price: float, quantity: int) -> int:
        c = self.conn.cursor()
        
        c.execute('''
            INSERT INTO order_items
                (order_id,
                product_id,
                price,
                quantity)
            VALUES
                (?, ? , ? , ?);
        ''', (order_id, product_id, price, quantity))

        self.conn.commit()

        id = c.lastrowid

        logger.info(f"[ORDER-STORAGE] Add Item ID:{id}")   

        return id
    
    def delete_item(self, item_id: int) -> bool:
        c = self.conn.cursor()
        c.execute('''
            DELETE FROM order_items
            WHERE id = ?
        ''', (item_id,))

        self.conn.commit()

        logger.info("[ORDER-STORAGE] Delete Item")

        return c.rowcount > 0
    
    def get(self, order_id: int) -> OrderDomain:
        c = self.conn.cursor()
        c.execute('''
            SELECT
                id,
                customer_id,
                created_at
            FROM
                orders
            WHERE
                id = ?
        ''', (order_id,))
        
        data = c.fetchone()

        order_id = data[0]
        customer_id = data[1]
        created_at = data[2]
        
        order = OrderDomain(customer_id)        
        order.set_id(order_id)
        order.set_created_at(created_at)

        c.close()        

        return self.__get_order_items(order)

    def __get_order_items(self, order: OrderDomain) -> OrderDomain:
        c = self.conn.cursor()

        c.execute('''
            SELECT 
                id,
                product_id,
                price,
                quantity
            FROM
                order_items
            WHERE
                order_id = ?
            ORDER BY
                id
        ''', (order.order_id,))
        
        data = c.fetchall()

        for item in data:
            order.add_item(item_id=item[0], product_id=item[1], price=item[2], quantity=item[3])

        c.close()

        return order
    
    def get_all_customer_orders(self, customer_id: int) -> list:
        c = self.conn.cursor()
        c.execute('''
            SELECT
                id,
                created_at
            FROM
                orders
            WHERE
                customer_id = ?
        ''', (customer_id,))
        
        data = c.fetchall()
        c.close() 

        orders = []
        
        for o in data:
            order = OrderDomain(customer_id)
            order.set_id(o[0])
            order.set_created_at(o[1])
            orders.append(orders.append(self.__get_order_items(order)))        

        return orders       