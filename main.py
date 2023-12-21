from models.user import User
from datetime import date
from mongoengine.errors import NotUniqueError
from models import storage
import bcrypt

password = '5555555555'

h_pwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

objects1 = {
        'staff_number': 'NCT88649',
        'first_name': 'Joseph',
        'last_name': 'Asemonu',
        'email': 'jos@mail.com',
        'password': h_pwd,
        'date_of_birth': date(2020, 8, 25).isoformat(),
        'phone': '0215122652',
        'SSNIT': 'HFT55555',
        'NID': '5565636524',
        'employment_date': date(2020, 8, 25).isoformat(),
        'gender': 'Male',
        'department': 'IT',
        'position': 'Software engineer',
        'Superuser': True
        }

objects2 = {
        'staff_number': 'NCT2111',
        'first_name': 'Rosemary',
        'last_name': 'Efebe',
        'email': 'roze247@gmail.com',
        'password': h_pwd,
        'date_of_birth': date(2020, 8, 25).isoformat(),
        'phone': '08077763334',
        'SSNIT': 'HFT56324',
        'NID': '5565636526',
        'employment_date': date(2020, 8, 25).isoformat(),
        'gender': 'Female',
        'department': 'Project',
        'position': 'PMO',
        'Superuser': True
        }

storage.connect()
user1 = User(**objects1)
user2 = User(**objects2)
try:
    id1 = storage.save(user1)
    id2 = storage.save(user2)
    print(id1, id2)
storage.all(User)
'''try:
    id = storage.save(user)
    print(user.password, user.Superuser)
except NotUniqueError:
    print("user exsit")
    print(User.objects.as_pymongo())'''
