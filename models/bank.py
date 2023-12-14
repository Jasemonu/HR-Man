from mongoengine import Document, StringField, DateTimeField, ObjectIdField
from datetime import date

class Bank(Document):
    user_id = ObjectIdField(required=True, max_length=70, unique=True)
    name = StringField(required=True, max_length=70)
    branch = StringField(required=True, max_length=70)
    code = StringField(required=True, max_length=70)
    account_number = StringField(required=True, max_length=70)
    account_name = StringField(required=True, max_length=70)
    created_at = DateTimeField(default=date.today().isoformat())
    updated_at = DateTimeField(default=date.today().isoformat())
