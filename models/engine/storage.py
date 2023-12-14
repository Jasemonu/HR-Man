#!/usr/bin/env python3

from mongoengine import connect, disconnect
#from models.user import User

class Storage:
    def __init__(self):
        self.db = None
    
    def connect(self):
        if self.db is None:
            self.db = connect(host="mongodb://localhost:27017/hr-mandb")

    def close(self):
        disconnect()

    def save(self, cls):
        cls.save()
        return cls.id

    def find_email(self, cls, email):
        data = cls.objects(email=email).first()
        return data

    def get(self, cls, id):
        data = cls.objects(id=id).first()
        return data

    def all(self, cls=None):
        if cls:
            return cls.objects.as_pymongo()
        return None
