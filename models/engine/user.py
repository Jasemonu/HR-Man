#!/usr/bin/env python3
"""This creates a user class"""
from models.engine.storage import Storage


class User(Storage):
    def __init__(self, *args, **kwargs):
        self.dict = {}
        for key, value in kwargs.items():
            self.dict[key] = value
        super().__init__()

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
