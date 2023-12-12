from mongoengine import Document, StringField, DateTimeField
from mongoengine import ObjectIdField, IntField
from datetime import date

class User(Document):
    user_id = ObjectIdField(unique=True, required=True)
    taken = IntField()
    remaining = IntField(required=True, max_length=70)
    start_date = DateTimeField(null=True)
    resume_date = DateTimeField(null=True)
    purpose = StringField(max_length=255)
    created_at = DateTimeField(default=date.today().isoformat())
    updated_at = DateTimeField(default=date.today().isoformat())
