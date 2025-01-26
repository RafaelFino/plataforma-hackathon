#!/bin/bash
curl -X POST http://localhost:8001/customer \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john.doe@example.com"}'
