#!/usr/bin/env python3

from mongoengine import connect, disconnect


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

    def find_staff(self, cls, number):
        data = cls.objects(staff_number=number).first()
        return data

    def all(self, cls=None):
        if cls:
            data = cls.objects()
            return list(data)
        return None

    def get(self, cls, id):
        data = cls.objects(id=id).first()
        return data

    def all(self, cls=None):
        if cls:
            data = cls.objects()
            return list(data) 
        return None

    def delete_staff(self, cls, staff_number):
        try:
            obj = cls.objects(staff_number=staff_number).first()
            if obj:
                obj.delete()
                return True  # Successfully deleted
            else:
                return False  # Object not found
        except Exception as e:
            print(f"Error deleting object with ID {staff_number}: {e}")
            return False


    def find_staff(staff, cls, number):
        data = cls.objects(staff_number=number).first()
        return data
   
