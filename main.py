from models.user import User
from datetime import date
from mongoengine.errors import NotUniqueError
from models import storage
import bcrypt

password = '5555555555'

h_pwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

objects = {
        'staff_number': 'NCT78649',
        'first_name': 'Joseph',
        'last_name': 'Asemonu',
        'email': 'jose@mail.com',
        'password': h_pwd,
        'date_of_birth': date(2020, 8, 25).isoformat(),
        'phone': '0215122652',
        'NID': '5565636524',
        'employment_date': date(2020, 8, 25).isoformat(),
        'gender': 'Male',
        'department': 'IT',
        'position': 'Software engineer',
        'Superuser': True
        }

# objects = {
#         'staff_number': 'NCT1111',
#         'first_name': 'Rosemary',
#         'last_name': 'Efebe',
#         'email': 'rozey247@gmail.com',
#         'password': h_pwd,
#         'date_of_birth': date(2020, 8, 25).isoformat(),
#         'phone': '08077763334',
#         'NID': '5565636526',
#         'employment_date': date(2020, 8, 25).isoformat(),
#         'gender': 'Female',
#         'department': 'Project',
#         'position': 'PMO',
#         'Superuser': True
#         }


user = User(**objects)
storage.connect()
storage.delete_staff(User, "JJ226")
try:
   # id = storage.save(user)
    print(user.password, user.Superuser)
except NotUniqueError:
    print("user exsit")
    print(User.objects.as_pymongo())
