#!/bin/bash
curl -X PUT http://localhost:8001/customer/101 \
  -H "Content-Type: application/json" \
  -d '{"name": "João Dorian", "email": "joão.dorian@example.com"}'
