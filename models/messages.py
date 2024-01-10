from mongoengine import Document, StringField, DateTimeField, EmailField
from mongoengine import  BooleanField
from datetime import date
import smtplib
from email.mime.text import MIMEText


class Message(Document):
    subject = StringField(required=True, max_length=70)
    name = StringField(required=True, max_length=70)
    email = EmailField(required=True, max_length=70)
    message = StringField(required=True, max_length=200)
    viewed = BooleanField(default=False)
    reply = BooleanField(default=False)
    created_at = DateTimeField(default=date.today().isoformat())


EMAIL_ADDRESS = 'asemonu@yahoo.com'
EMAIL_PASSWORD = 'wuvoqdjygbsnxtxd'

def reply_email(email, subject, message):
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = email

    with smtplib.SMTP('smtp.mail.yahoo.com', 587) as smtp_server:
        smtp_server.starttls()
        smtp_server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp_server.send_message(msg)

