from pymongo import MongoClient


class MongoRepository():
    def __init__(self, host, port, database, collection):
        self.collection = MongoClient(host, port)[database][collection]

    def upsert(self, short_model):
        self.collection.replace_one({
            '_id': short_model['_id']
        }, short_model, upsert=True)

    def get_one(self, id):
        return self.collection.find_one({
            '_id': id
        })