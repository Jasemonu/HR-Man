#!/usr/bin/env python3
"""This creates a user class"""
from storage import Storage


class User(Storage):
    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        super().__init__()

    def add_user(self):
        data =  self.save("employee", self.__dict__)
        return data

    def find_user(self):
        pass

user = User(name="joe")

print(user.add_user())
