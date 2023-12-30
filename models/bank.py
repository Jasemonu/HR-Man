from mongoengine import Document, StringField, DateTimeField, ObjectIdField
from mongoengine import ReferenceField
from datetime import date

class Bank(Document):
    staff = ReferenceField('User', required=True, reverse_delete_rule=2)
    name = StringField(required=True, max_length=70, unique=True)
    branch = StringField(required=True, max_length=70)
    code = StringField(required=True, max_length=70)
    account_number = StringField(required=True, max_length=70)
    account_name = StringField(required=True, max_length=70)
    created_at = DateTimeField(default=date.today().isoformat())
    updated_at = DateTimeField(default=date.today().isoformat())
