from mongoengine import Document, IntField, DateTimeField, ObjectIdField
from datetime import date

class Deduction(Document):
    user_id = ObjectIdField(unique=True, required=True)
    SSNIT = IntField(default=0, required=True)
    tax = IntField(default=0, required=True)
    tier_two = IntField(required=True, default=0,)
    tier_three = IntField(default=0)
    total = IntField(default=0)
    created_at = DateTimeField(default=date.today().isoformat())
    updated_at = DateTimeField(default=date.today().isoformat())
