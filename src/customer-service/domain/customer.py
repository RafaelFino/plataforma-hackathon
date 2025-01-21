class CustomerDomain:
    def __init__(self, name: str, email: str):
        self.customer_id = None
        self.name = name
        self.email = email

    def set_id(self, customer_id: int):
        self.customer_id = customer_id

    def __str__(self):
        return f'Customer ID: {self.customer_id}, Name: {self.name}, Email: {self.email}'
    
    def to_json(self):
        return {
            'customer_id': self.customer_id,
            'name': self.name,
            'email': self.email
        }