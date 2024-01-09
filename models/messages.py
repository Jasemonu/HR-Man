from mongoengine import Document, StringField, DateTimeField, EmailField
from mongoengine import  BooleanField
from datetime import date

class Message(Document):
    subject = StringField(required=True, max_length=70)
    name = StringField(required=True, max_length=70)
    email = EmailField(required=True, max_length=70)
    message = StringField(required=True, max_length=200)
    viewed = BooleanField(default=False)
    created_at = DateTimeField(default=date.today().isoformat())
