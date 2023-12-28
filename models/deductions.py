from mongoengine import Document, IntField, DateTimeField, StringField
from mongoengine import ReferenceField
from datetime import date

class Deduction(Document):
    staff = ReferenceField('User', reverse_delete_rule=2, required=True)
    period = StringField(required=True)
    SSNIT = IntField(default=0, required=True)
    tax = IntField(default=0, required=True)
    tier_two = IntField(required=True, default=0,)
    tier_three = IntField(default=0)
    total = IntField(default=0)
    created_at = DateTimeField(default=date.today().isoformat())
    updated_at = DateTimeField(default=date.today().isoformat())
