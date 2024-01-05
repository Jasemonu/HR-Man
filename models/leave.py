from mongoengine import Document, StringField, DateTimeField, ReferenceField
from mongoengine import ObjectIdField, IntField, ReferenceField
from datetime import date
from models.user import User

class Leave(Document):
	staff = ReferenceField('User', reverse_delete_rule=2, required=True)
	staff_name = StringField(max_length=255)
	remaining = IntField(required=True, default=30)
	start_date = DateTimeField(null=True)
	end_date = DateTimeField(null=True)
	requested_days = IntField()
	leave_type = StringField(max_length=255)
	leave_status = StringField(max_length=255, default='pending')
	comment = StringField(max_length=255, default='No comments')
	created_at = DateTimeField(default=date.today().isoformat())
	updated_at = DateTimeField(default=date.today().isoformat())
	user = ReferenceField(User)
