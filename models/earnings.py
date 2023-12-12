from mongoengine import Document, Decimal128Field, DateTimeField, ObjectIdField
from datetime import date

class Earning(Document):
    user_id = ObjectIdField(unique=True, required=True)
    basic = Decimal128Field(precision=2,)
    overtime = Decimal128Field(precision=2)
    allawance = Decimal128Field(precision=2)
    bonus = Decimal128Field(precision=2)
    created_at = DateTimeField(default=date.today().isoformat())
    updated_at = DateTimeField(default=date.today().isoformat())
