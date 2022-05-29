import requests
import time
# from PIL import Image, ImageDraw, ImageFont
# from io import BytesIO

session = requests.Session()
auth = {
    "username": "angel",
    "password": "anapoles"
}
response = session.post('http://localhost:8000/api/login-token/', data=auth)
data = response.json()
token = "JWT "+data["access"]
print(data)
headers = {
    "Authorization": token
}
customer = {
    "fullname": "angel",
    "email": "anapolesnapoles@gmail.com",
    "zip_code": "33102"
}
response = session.post(
    'http://localhost:8000/api/customers/', data=customer, headers=headers)
print('Customer -> ', response)
drone_list = [
    {
        "serial_number": "d1",
        "model": "Lightweight",
        "weight": 200,
        "battery": 80,
        "state": "Idle"
    },
    {
        "serial_number": "d2",
        "model": "Lightweight",
        "weight": 200,
        "battery": 80,
        "state": "Idle"
    },
    {
        "serial_number": "d3",
        "model": "Middleweight",
        "weight": 300,
        "battery": 80,
        "state": "Idle"
    },
    {
        "serial_number": "d4",
        "model": "Middleweight",
        "weight": 300,
        "battery": 80,
        "state": "Idle"
    },
    {
        "serial_number": "d5",
        "model": "Cruiserweight",
        "weight": 400,
        "battery": 80,
        "state": "Idle"
    },
    {
        "serial_number": "d6",
        "model": "Cruiserweight",
        "weight": 400,
        "battery": 80,
        "state": "Idle"
    },
    {
        "serial_number": "d7",
        "model": "Heavyweight",
        "weight": 500,
        "battery": 80,
        "state": "Idle"
    },
    {
        "serial_number": "d8",
        "model": "Heavyweight",
        "weight": 500,
        "battery": 80,
        "state": "Idle"
    },
    {
        "serial_number": "d9",
        "model": "Lightweight",
        "weight": 200,
        "battery": 80,
        "state": "Idle"
    },
    {
        "serial_number": "d10",
        "model": "Middleweight",
        "weight": 300,
        "battery": 80,
        "state": "Idle"
    }
]

for drone in drone_list:
    time.sleep(1)
    response = session.post(
        'http://localhost:8000/api/drones/', data=drone, headers=headers)
    print('Drone -> ', response)

medications = [
    {
        "files": [
            ('image', ('P1.jpg', open("medication.jpg", 'rb'), 'image/jpeg'))
        ],
        "medication": {
            'name': 'paracetamol',
            'weight': 900,
            'code': 'P1'
        }
    },
    {
        "files": [
            ('image', ('A1.jpg', open("medication.jpg", 'rb'), 'image/jpeg'))
        ],
        "medication": {
            "name": "alicil",
            "weight": 328,
            "code": "A1"
        }
    },
    {
        "files": [
            ('image', ('AZ2.jpg', open("medication.jpg", 'rb'), 'image/jpeg'))
        ],
        "medication": {
            "name": "azitromicina",
            "weight": 296,
            "code": "AZ2"
        }
    },
    {
        "files": [
            ('image', ('DU1.jpg', open("medication.jpg", 'rb'), 'image/jpeg'))
        ],
        "medication": {
            "name": "duralgina",
            "weight": 129,
            "code": "DU1"
        }
    },
    {
        "files": [
            ('image', ('ASP1.jpg', open("medication.jpg", 'rb'), 'image/jpeg'))
        ],
        "medication": {
            "name": "aspirina",
            "weight": 746,
            "code": "ASP1"
        }
    },
    {
        "files": [
            ('image', ('POL1.jpg', open("medication.jpg", 'rb'), 'image/jpeg'))
        ],
        "medication": {
            "name": "polivi",
            "weight": 678,
            "code": "POL1"
        }
    },
    {
        "files": [
            ('image', ('SP1.jpg', open("medication.jpg", 'rb'), 'image/jpeg'))
        ],
        "medication": {
            "name": "sulfaprin",
            "weight": 480,
            "code": "SP1"
        }
    }
]
for med in medications:
    time.sleep(1)
    response = requests.request(
        "POST", 'http://localhost:8000/api/medications/',
        headers=headers, data=med["medication"], files=med["files"])
    print(response)


entity = {
    "medications": [
        1, 2, 3, 4, 5, 6, 7
    ],
    "drones": [
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10
    ],
    "name": "Entity",
    "zip_code": "33186"
}
time.sleep(1)
response = session.post(
    'http://localhost:8000/api/entitys/',
    headers=headers,
    data=entity
)
print('entity -> ', response.text)
deliverys = [
    {
        "entity": 1,
        "customer": 1,
        "medications": [
            1, 2
        ]
    },
    {
        "entity": 1,
        "customer": 1,
        "medications": [
            3, 4
        ]
    },
    {
        "entity": 1,
        "customer": 1,
        "medications": [
            5, 6, 7
        ]
    }
]
# for delivery in deliverys:
response = session.post(
    'http://localhost:8000/api/deliverys/',
    headers=headers,
    data=deliverys[0]
)
print('delivery -> ', response)