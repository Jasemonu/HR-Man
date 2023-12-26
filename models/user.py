from mongoengine import Document, StringField, DateTimeField
from mongoengine import EmailField, BooleanField
from flask_login import UserMixin
from datetime import date
import random
import string
import smtplib
from email.mime.text import MIMEText

class User(Document, UserMixin):
    staff_number = StringField(required=True, unique=True, max_length=70)
    first_name = StringField(required=True, max_length=70)
    last_name = StringField(required=True, max_length=70)
    email = EmailField(required=True, max_length=70, unique=True)
    password = StringField(required=True, max_length=70)
    phone = StringField(required=True, max_length=70)
    date_of_birth = DateTimeField(default=date(1670, 12,20).isoformat())
    NID = StringField(required=True, max_length=70)
    SSNIT = StringField(required=True, default='GH55LOM')
    employment_date = DateTimeField(default=date(200, 12,20).isoformat())
    gender = StringField(required=True, max_length=20)
    department = StringField(required=True, max_length=70)
    position = StringField(required=True, max_length=70)
    Superuser = BooleanField(required=True, default=False)
    created_at = DateTimeField(default=date.today().isoformat())
    updated_at = DateTimeField(default=date.today().isoformat())

EMAIL_ADDRESS = 'asemonu@yahoo.com'
EMAIL_PASSWORD = 'wuvoqdjygbsnxtxd'


def random_password():
    password_length = 10
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(password_length))

def gen_employee_id(first_name, last_name):
    employee_initials = f"{first_name[0]}{last_name[0]}".upper()
    random_number = ''.join(random.choice(string.digits) for _ in range(3))
    staff_number = f"{employee_initials}{random_number}"
    return staff_number


def send_email(email, password):
    msg = MIMEText(
    f"You are registered in HR-Man as a user and "
    f"your login details are email: {email} password: {password}"
    )
    msg['Subject'] = 'Registration Confirmation'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = email

    with smtplib.SMTP('smtp.mail.yahoo.com', 587) as smtp_server:
        smtp_server.starttls()
        smtp_server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp_server.send_message(msg)


def valid_fields(data):
    required_fields = [
    'first_name', 'last_name', 'email', 'date_of_birth',
    'phone_number', 'employment_date', 'NID', 'gender',
    'department', 'position'
    ]
    for field in required_fields:
        if field not in data or not data[field]:
            return False
    return True

