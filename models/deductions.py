from mongoengine import Document, Decimal128Field, DateTimeField, ObjectIdField
from datetime import date

class Deductions(Document):
    user_id = ObjectIdField(unique=True, required=True)
    SSNIT = Decimal128Field(precision=2,)
    tax = Decimal128Field(precision=2)
    tier_two = Decimal128Field(precision=2)
    tier_three = Decimal128Field(precision=2)
    created_at = DateTimeField(default=date.today().isoformat())
    updated_at = DateTimeField(default=date.today().isoformat())
