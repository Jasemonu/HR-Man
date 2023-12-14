from mongoengine import Document, DateTimeField, ListField, StringField
from datetime import date

class Payroll(Document):
    name = StringField(required=True, unique=True)
    items = ListField(required=True, unique=True)
    created_at = DateTimeField(default=date.today().isoformat())
    updated_at = DateTimeField(default=date.today().isoformat())
