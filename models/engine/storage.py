#!/usr/bin/env python3

from pymongo import MongoClient

class Storage:
    def __init__(self):
        client = MongoClient("mongodb://localhost:27017")
        self.db = client["hr-mandb"]

    def save(self, collection, document):
        collection = self.db[f"{collection}"]
        data = collection.insert_one(document)
        return data

    def find_item(self, collection, search_item):
        collection = self.db[f"{collection}"]
        data = collection.find_one(search_item)
        return data
