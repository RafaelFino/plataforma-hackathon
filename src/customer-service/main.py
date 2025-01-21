#!/bin/env python3

import logging
from http import HTTPStatus
from datetime import datetime
from fastapi import FastAPI, Request, Response

from domain.customer import CustomerDomain
from service.customer import CustomerService

# Insira mensagens de log para todas as funções
#   - Para funções que alteram o estado do domínio, inclua mensagens de log antes e depois da alteração (logs de info!)
#   - Para funções que não alteram o estado do domínio, inclua mensagens de log apenas no início da função (logs de debug!)
# Insira controler de Try/Except para todas as funções e logs nos casos de Exception usando logger.error
# Em caso de erro, envie um retorno HTTP adequado

app = FastAPI()
service = CustomerService()

logger = logging.getLogger('uvicorn.error')

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
        logger.error(f"[CUSTOMER-API] Invalid ID: {id}")
        
    return False

@app.get('/')
def root(response: Response):
    return makeResponse(response, "Customer API", status=HTTPStatus.OK)

@app.post('/customer')
def add_customer(response: Response):
    data = Request.get_json()
    customer = CustomerDomain(data['name'], data['email'])
    customer_id = service.add(customer)

    return makeResponse(response, "Customer added", {"customer_id": customer_id }, status=HTTPStatus.CREATED)

@app.put('/customer/{id}')
def update_customer(id, response: Response):
    if check_id(id) == False:
        return makeResponse("Invalid ID"), HTTPStatus.BAD_REQUEST

    data = Request.get_json()
    customer = CustomerDomain(data['name'], data['email'])
    customer.set_id(id)
    updated = service.update(customer)

    if updated:
        return makeResponse(response, "Customer updated", status=HTTPStatus.OK)
    else:
        return makeResponse(response, "Customer not found", status=HTTPStatus.NO_CONTENT)
    
@app.delete('/customer/{id}')
def delete_customer(id, response: Response):
    if check_id(id) == False:
        return makeResponse(response, "Invalid ID", status=HTTPStatus.BAD_REQUEST)

    deleted = service.delete(id)

    if deleted:
        return makeResponse(response, "Customer deleted", status=HTTPStatus.OK)
    else:
        return makeResponse(response, "Customer not found", status=HTTPStatus.NO_CONTENT)
    
@app.get('/customer/{id}')
def get_customer(id, response: Response):
    if check_id(id) == False:
        return makeResponse(response, "Invalid ID", status=HTTPStatus.BAD_REQUEST)
        
    customer = service.get(id)

    if customer:
        return makeResponse(response, "Customer found", customer.to_json(), status=HTTPStatus.OK)
    else:
        return makeResponse(response, "Customer not found", status=HTTPStatus.NO_CONTENT)
    
@app.get('/customer')
def get_all_customers(response: Response):
    customers = service.get_all()
    customers_json = [customer.to_json() for customer in customers]

    return makeResponse(response, "Customers found", {"customers": customers_json}, status=HTTPStatus.OK)