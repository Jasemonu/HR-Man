#!/usr/bin/env python3
"""This creates a user class"""
from flask_login import UserMixin
from models.engine.storage import Storage
import bcrypt


class User(Storage, UserMixin):
    def __init__(self, *args, **kwargs):
        self.dict = {}
        for key, value in kwargs.items():
            self.dict[key] = value
        super().__init__()

    def hash_password(self, password):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed_password.decode('utf-8')
    
    def check_password(self, plain_password, hashed_password):
         return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


    def add_user(self):
        user = self.save('employees', self.dict)
        return user.inserted_id

    def find_user(self, **kwargs):
        data = self.find_item('employees', kwargs)
        return data

user = User(name='affum', phone=555555, location='ghana')
data = user.add_user()
print(data)
data = user.find_user()
print(data)
