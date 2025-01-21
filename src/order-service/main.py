#!/bin/env python3

import logging
from http import HTTPStatus
from datetime import datetime
from fastapi import FastAPI, Request, Response

from service.order import OrderService
from domain.order import OrderDomain
from client.product import ProductClient
from client.customer import CustomerClient


# Insira mensagens de log para todas as funções
#   - Para funções que alteram o estado do domínio, inclua mensagens de log antes e depois da alteração (logs de info!)
#   - Para funções que não alteram o estado do domínio, inclua mensagens de log apenas no início da função (logs de debug!)
# Insira controler de Try/Except para todas as funções e logs nos casos de Exception usando logging.error
# Em caso de erro, envie um retorno HTTP adequado

print("Starting...")

app = FastAPI()
customer_client = CustomerClient(customer_service_url="http://localhost:8001")
product_client = ProductClient(product_service_url="http://localhost:8002")
order_service = OrderService(customer_client, product_client)
logging.basicConfig(
    level=logging.DEBUG, 
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="logs/order-service.log",
    filemode='a',
    datefmt='%H:%M:%S',
)

def makeResponse(response: Response, msg: str, args: dict = {}, status: HTTPStatus = HTTPStatus.OK ) -> dict:
    ret = {
        "message": msg,
        "timestamp": datetime.now().isoformat()
    }

    for key in args:
        ret[key] = args[key]

    response.status_code = status

    return ret

def check_id(id):
    try:
        tmp = int(id)
        if tmp > 0:
            return True
        
    except ValueError:
        logging.error(f"[ORDER-API] Invalid ID: {id}")
        
    return False

@app.get('/')
def root(response: Response):
    return makeResponse(response, "Order API", status=HTTPStatus.OK)

@app.post('/order')
def add_customer(response: Response):
    data = Request.get_json()
    customer_id = data['customer_id']

    if check_id(customer_id) == False:
        return makeResponse("Invalid CUSTOMER ID"), HTTPStatus.BAD_REQUEST

    order_id = order_service.create_order(customer_id)

    return makeResponse(response, "Order created", {"order_id": order_id }, status=HTTPStatus.CREATED)

@app.patch('/order/{order_id}')
def add_order_item(order_id, product_id, quantity, response: Response):
    if check_id(order_id) == False:
        return makeResponse("Invalid ORDER ID"), HTTPStatus.BAD_REQUEST

    data = Request.get_json()
    product_id = data['product_id']

    if check_id(product_id) == False:
        return makeResponse("Invalid PRODUCT ID"), HTTPStatus.BAD_REQUEST

    quantity = data['quantity']    
    product_info = product_client.load(product_id)

    if product_info is None:
        return makeResponse(response, "Product not found", {"product_id": product_id}, status=HTTPStatus.NOT_FOUND)
    
    item_id = order_service.add_product(order_id, product_id, quantity)

    if item_id is not None:
        return makeResponse(response, "Product added to order", { "product_info": product_info, "item_id": item_id }, status=HTTPStatus.CREATED)
    else:
        return makeResponse(response, "Product not added to order", status=HTTPStatus.INTERNAL_SERVER_ERROR)
    
    
@app.delete('/order/{order_id}/{item_id}')
def delete_customer(order_id, item_id, response: Response):
    if check_id(order_id) == False:
        return makeResponse("Invalid ORDER ID"), HTTPStatus.BAD_REQUEST

    if check_id(item_id) == False:
        return makeResponse("Invalid ITEM ID"), HTTPStatus.BAD_REQUEST

    deleted = order_service.remove_product(order_id, item_id)

    if deleted:
        return makeResponse(response, "Product removed from order", status=HTTPStatus.OK)
    else:
        return makeResponse(response, "Product not removed from order", status=HTTPStatus.INTERNAL_SERVER_ERROR)
    
@app.get('/order/{order_id}')
def get_customer(order_id, response: Response):
    if check_id(order_id) == False:
        return makeResponse(response, "Invalid ORDER ID", status=HTTPStatus.BAD_REQUEST)
        
    order = order_service.get_order(order_id)

    if order:
        return makeResponse(response, "Order found", order.to_json(), status=HTTPStatus.OK)
    else:
        return makeResponse(response, "Order not found", status=HTTPStatus.NO_CONTENT)
    
@app.get('/customer/{customer_id}')
def get_all_customers(customer_id, response: Response):
    if check_id(customer_id) == False:
        return makeResponse(response, "Invalid CUSTOMER ID", status=HTTPStatus.BAD_REQUEST)
    
    customer_info = customer_client.load(customer_id)

    if customer_info is None:
        return makeResponse(response, "Customer not found", {"customer_id": customer_id}, status=HTTPStatus.NOT_FOUND)

    orders = order_service.get_all_from_customer(customer_id)

    if orders is not None:
        return makeResponse(response, "Orders found", {"orders": orders, "customer_info": customer_info}, status=HTTPStatus.OK)
    else:
        return makeResponse(response, "Orders not found", status=HTTPStatus.NO_CONTENT)


print("Done!")

