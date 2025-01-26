#!/bin/bash
curl -X DELETE http://localhost:8001/customer/101 \
  -H "Content-Type: application/json" 
