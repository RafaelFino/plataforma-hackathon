#!/bin/env python3

import logging
from http import HTTPStatus
from datetime import datetime
from fastapi import FastAPI, Request, Response

from domain.product import ProductDomain
from service.product import ProductService

# Insira mensagens de log para todas as funções
#   - Para funções que alteram o estado do domínio, inclua mensagens de log antes e depois da alteração (logs de info!)
#   - Para funções que não alteram o estado do domínio, inclua mensagens de log apenas no início da função (logs de debug!)
# Insira controler de Try/Except para todas as funções e logs nos casos de Exception usando logging.error
# Em caso de erro, envie um retorno HTTP adequado

print("Starting...")

app = FastAPI()
service = ProductService()
logging.basicConfig(
    level=logging.DEBUG, 
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="logs/product-service.log",
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
        logging.error(f"[PRODUCT-API] Invalid ID: {id}")
        
    return False

@app.get('/')
def root(response: Response):
    return makeResponse(response, "Product API", status=HTTPStatus.OK)

@app.post('/product')
def add_product(response: Response):
    data = Request.get_json()
    product = ProductDomain(data['name'], data['price'])
    product_id = service.add(product)

    return makeResponse(response, "Product added", {"product_id": product_id}, status=HTTPStatus.CREATED)

@app.put('/product/{id}')
def update_product(id, response: Response):
    if check_id(id) == False:
        return makeResponse(response, "Invalid ID", status=HTTPStatus.BAD_REQUEST)

    data = Request.get_json()
    product = ProductDomain(data['name'], data['price'])
    product.set_id(id)
    updated = service.update(product)

    if updated:
        return makeResponse(response, "Product updated", status=HTTPStatus.OK)
    else:
        return makeResponse(response, "Product not found", status=HTTPStatus.NO_CONTENT)
    
@app.delete('/product/{id}')
def delete_product(id, response: Response):
    if check_id(id) == False:
        return makeResponse(response, "Invalid ID", status=HTTPStatus.BAD_REQUEST)

    deleted = service.delete(id)

    if deleted:
        return makeResponse(response, "Product deleted", status=HTTPStatus.OK)
    else:
        return makeResponse(response, "Product not found", status=HTTPStatus.NO_CONTENT)
    
@app.get('/product/{id}')
def get_product(id, response: Response):
    if check_id(id) == False:
        return makeResponse(response, "Invalid ID", status=HTTPStatus.BAD_REQUEST)

    product = service.get(id)

    if product is not None:
        return makeResponse(response, "Product found", {"product": product.to_dict()}, status=HTTPStatus.OK)
    else:
        return makeResponse(response, "Product not found", status=HTTPStatus.NO_CONTENT)
    
@app.get('/product')
def get_all_products(response: Response):
    products = service.get_all()
    ret = []
    for product in products:
        ret.append(product.to_dict())

    return makeResponse(response, "Products found", {"products": ret}, status=HTTPStatus.OK)

print("Done!")
