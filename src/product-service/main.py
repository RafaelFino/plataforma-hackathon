#!/bin/env python3

import logging
from flask import Flask, request, jsonify
from http import HTTPStatus
from datetime import datetime
import json 

from domain.product import ProductDomain
from service.product import ProductService

# Insira mensagens de log para todas as funções
#   - Para funções que alteram o estado do domínio, inclua mensagens de log antes e depois da alteração (logs de info!)
#   - Para funções que não alteram o estado do domínio, inclua mensagens de log apenas no início da função (logs de debug!)
# Insira controler de Try/Except para todas as funções e logs nos casos de Exception usando logging.error

print("Starting...")

app = Flask(__name__)
service = ProductService()
logging.basicConfig(
    level=logging.DEBUG, 
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="logs/product-service.log",
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