from mongoengine import Document, StringField, DateTimeField
from mongoengine import ObjectIdField, IntField
from datetime import date

class Leave(Document):
    employee_id = ObjectIdField(unique=True, required=True)
    remaining = IntField(required=True, default=30)
    start_date = DateTimeField(null=True)
    end_date = DateTimeField(null=True)
    leave_type = StringField(max_length=255)
    created_at = DateTimeField(default=date.today().isoformat())
    updated_at = DateTimeField(default=date.today().isoformat())
