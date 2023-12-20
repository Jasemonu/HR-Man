from mongoengine import Document, StringField, DateTimeField


class Attendance(Document):
    staff_number = StringField(required=True)
    name = StringField(required=True, unique=True)
    staff_name = StringField(required=True)
    date = DateTimeField(required=True)
    entry_time = StringField(required=True)
    exit_time = StringField()

