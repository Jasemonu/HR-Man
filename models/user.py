from mongoengine import Document, StringField, DateTimeField
from mongoengine import EmailField, BooleanField
from flask_login import UserMixin
from datetime import date

class User(Document, UserMixin):
    staff_number = StringField(required=True, max_length=70)
    first_name = StringField(required=True, max_length=70)
    last_name = StringField(required=True, max_length=70)
    email = EmailField(required=True, max_length=70, unique=True)
    password = StringField(required=True, max_length=70)
    phone = StringField(required=True, max_length=70)
    date_of_birth = DateTimeField(default=date(1670, 12,20).isoformat())
    NID = StringField(required=True, max_length=70)
    employment_date = DateTimeField(default=date(200, 12,20).isoformat())
    gender = StringField(required=True, max_length=20)
    department = StringField(required=True, max_length=70)
    position = StringField(required=True, max_length=70)
    Superuser = BooleanField(required=True, default=False)
    created_at = DateTimeField(default=date.today().isoformat())
    updated_at = DateTimeField(default=date.today().isoformat())
