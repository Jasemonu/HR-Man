from mongoengine import Document, StringField, DateTimeField
from mongoengine import ObjectIdField, IntField
from datetime import date

class Leave(Document):
	staff_number = StringField(required=True)
	staff_name = StringField(max_length=255)
	remaining = IntField(required=True, default=30)
	start_date = DateTimeField(null=True)
	end_date = DateTimeField(null=True)
	leave_type = StringField(max_length=255)
	leave_status = StringField(max_length=255, default='pending')
	created_at = DateTimeField(default=date.today().isoformat())
	updated_at = DateTimeField(default=date.today().isoformat())
