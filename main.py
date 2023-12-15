from models.user import User
from datetime import date
from mongoengine.errors import NotUniqueError
from models import storage
import bcrypt

password = '5555555555'

h_pwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

objects = {
        'staff_number': 'NCT3333',
        'first_name': 'Samuel',
        'last_name': 'Affum',
        'email': 'sam2@mail.com',
        'password': h_pwd,
        'date_of_birth': date(2020, 8, 25).isoformat(),
        'phone': '0215122552',
        'NID': '5565636525',
        'employment_date': date(2020, 8, 25).isoformat(),
        'gender': 'Female',
        'department': 'Maintenace',
        'position': 'Tecnician',
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
try:
    id = storage.save(user)
    print(user.password, user.Superuser)
except NotUniqueError:
    print("user exsit")
    print(User.objects.as_pymongo())
