from mongoengine import Document, StringField, DateTimeField
from datetime import date


class Payslip(Document):
    period = StringField(required=True)
    staff_number = StringField(required=True)
    name = StringField(required=True, unique=True)
    created_at = DateTimeField(default=date.today().isoformat())
    updated_at = DateTimeField(default=date.today().isoformat())
