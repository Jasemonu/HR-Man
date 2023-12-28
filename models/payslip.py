from mongoengine import Document, StringField, DateTimeField, ReferenceField
from datetime import date


class Payslip(Document):
    period = StringField(required=True)
    staff = ReferenceField('User', reverse_delete_rule=2, required=True)
    name = StringField(required=True, unique=True)
    created_at = DateTimeField(default=date.today().isoformat())
    updated_at = DateTimeField(default=date.today().isoformat())
