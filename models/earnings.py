from mongoengine import Document, DecimalField, DateTimeField, StringField
from mongoengine import IntField, ReferenceField
from datetime import date

class Earning(Document):
    staff = ReferenceField('User', reverse_delete_rule=2, required=True)
    period = StringField(required=True)
    pay_hour = IntField(default=0)
    total_hours = IntField(default=0)
    basic = IntField(default=0.00)
    overtime_hour = IntField(default=0)
    overtime_hours = IntField(default=0)
    overtime = IntField(default=0)
    allawance = IntField(default=0)
    bonus = IntField(default=0)
    gross = IntField(default=0)
    created_at = DateTimeField(default=date.today().isoformat())
    updated_at = DateTimeField(default=date.today().isoformat())
