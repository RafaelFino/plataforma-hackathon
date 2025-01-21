#!/bin/env python3

import logging
from flask import Flask, request, jsonify
from http import HTTPStatus
from datetime import datetime
import json 

from domain.customer import CustomerDomain
from service.customer import CustomerService

# Insira mensagens de log para todas as funções
#   - Para funções que alteram o estado do domínio, inclua mensagens de log antes e depois da alteração (logs de info!)
#   - Para funções que não alteram o estado do domínio, inclua mensagens de log apenas no início da função (logs de debug!)
# Insira controler de Try/Except para todas as funções e logs nos casos de Exception usando logging.error

print("Starting...")

app = Flask(__name__)
service = CustomerService()
logging.basicConfig(
    level=logging.DEBUG, 
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="logs/customer-service.log",
    filemode='a',
    datefmt='%H:%M:%S',
)

def makeResponse(msg: str, args: dict = {}):
    ret = {
        "message": msg,
        "timestamp": datetime.now().isoformat()
    }

    for key in args:
        ret[key] = args[key]

    return ret

@app.route('/customer', methods=['POST'])
def add_customer():
    data = request.get_json()
    customer = CustomerDomain(data['name'], data['email'])
    customer_id = service.add(customer)

    return jsonify(makeResponse("Customer added", {"customer_id": customer_id})), HTTPStatus.CREATED

@app.route('/customer/<int:id>', methods=['PUT'])
def update_customer(id):
    data = request.get_json()
    customer = CustomerDomain(data['name'], data['email'])
    customer.set_id(id)
    updated = service.update(customer)

    if updated:
        return jsonify(makeResponse("Customer updated")), HTTPStatus.OK
    else:
        return jsonify(makeResponse("Customer not found")), HTTPStatus.NO_CONTENT
    
@app.route('/customer/<int:id>', methods=['DELETE'])
def delete_customer(id):
    deleted = service.delete(id)

    if deleted:
        return jsonify(makeResponse("Customer deleted")), HTTPStatus.OK
    else:
        return jsonify(makeResponse("Customer not found")), HTTPStatus.NO_CONTENT
    
@app.route('/customer/<int:id>', methods=['GET'])
def get_customer(id):
    customer = service.get(id)

    if customer:
        return jsonify(makeResponse("Customer found", customer.to_json())), HTTPStatus.OK
    else:
        return jsonify(makeResponse("Customer not found")), HTTPStatus.NO_CONTENT
    
@app.route('/customer', methods=['GET'])
def get_all_customers():
    customers = service.get_all()
    customers_json = [customer.to_json() for customer in customers]

    return jsonify(makeResponse("Customers found", {"customers": customers_json})), HTTPStatus.OK

if __name__ == '__main__':
    app.run(port=5000, debug=True)

print("Done!")

