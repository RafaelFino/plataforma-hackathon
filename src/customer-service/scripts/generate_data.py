import random

names = [
    "Alice",
    "Bob",
    "Charlie",
    "David",
    "Eve",
    "Fiona"
    "Frank",
    "Grace",
    "Gus",
    "Heidi",
    "Holly",
    "Igor",
    "Ivan",
    "Jack",
    "Jane",
    "Jill",
    "John",
    "Kate",
    "Kevin",
    "Lena",
    "Liam",
    "Mia",
    "Mike",
    "Nina",
    "Noah",
    "Olivia",
    "Oscar",
    "Pam",
    "Paul",
    "Quincy",
    "Quinn",
    "Rex",
    "Ryan",
    "Sophia",
    "Sue",
    "Tom",
    "Troy",
    "Uma",
    "Ursula",
    "Violet",
    "Vlad",
    "Wendy",
    "Will",
    "Xander",
    "Xena",
    "Yuri",
    "Yvonne",
    "Zack",
]

surnames = [
    "Adams",
    "Allen",
    "Anderson",
    "Baker",
    "Brown",
    "Campbell",
    "Carter",
    "Clark",
    "Collins"
    "Davis",
    "Edwards",
    "Evans",
    "Garcia",
    "Gonzalez",
    "Green",
    "Hall",
    "Harris",
    "Hernandez",
    "Hill",
    "Jackson",
    "Johnson",
    "Jones",
    "King",
    "Lee",
    "Lewis",
    "Lopez",
    "Martin",
    "Martinez",
    "Miller",
    "Mitchell",
    "Moore",
    "Nelson",
    "Parker",
    "Perez",
    "Phillips",
    "Roberts",
    "Robinson",
    "Rodriguez",
    "Scott",
    "Smith",
    "Taylor",
    "Thomas",
    "Thompson",
    "Turner",
    "Walker",
    "White",
    "Williams",
    "Wilson",
    "Wright",
    "Young",
]

mail_providers = [
    "gmail.com",
    "yahoo.com",
    "hotmail.com",
    "outlook.com",
    "aol.com",
    "protonmail.com",
    "zoho.com",
    "yandex.com",
    "mail.com",
    "icloud.com"
]

def create() -> str:
    name = f"{random.choice(names)}"
    surname = f"{random.choice(surnames)}"
    email = f"{name.lower()}.{surname.lower()}@{random.choice(mail_providers)}"
    return f"INSERT INTO customers (name, email) VALUES ('{name} {surname}', '{email}');\n"

def generate(n: int):
    with open(f"customer_data.sql", "w") as f:
        for i in range(n):        
            f.write(create())

generate(100)