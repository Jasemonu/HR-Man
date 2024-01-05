from mongoengine import Document, StringField, DateTimeField, ReferenceField
from models.user import User


class Attendance(Document):
    staff = ReferenceField('User', reverse_delete_rule=2, required=True)
    name = StringField(required=True, unique=True)
    date = DateTimeField(required=True)
    entry_time = StringField(required=True)
    exit_time = StringField()

