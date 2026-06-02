from pymongo import MongoClient
from django.conf import settings
from bson import ObjectId
from datetime import datetime, date

class MongoDB:
    _client = None
    _db = None

    @classmethod
    def get_db(cls):
        if cls._db is None:
            cls._client = MongoClient(settings.MONGO_URI)
            cls._db = cls._client[settings.MONGO_DB_NAME]
        return cls._db

    @classmethod
    def get_collection(cls, name):
        return cls.get_db()[name]

# ---------- Customer Helper ----------
class CustomerManager:
    collection = MongoDB.get_collection('customers')

    @classmethod
    def all(cls):
        return list(cls.collection.find())

    @classmethod
    def get(cls, id):
        if isinstance(id, str):
            id = ObjectId(id)
        return cls.collection.find_one({'_id': id})

    @classmethod
    def create(cls, data):
        return cls.collection.insert_one(data).inserted_id

    @classmethod
    def update(cls, id, data):
        if isinstance(id, str):
            id = ObjectId(id)
        cls.collection.update_one({'_id': id}, {'$set': data})

    @classmethod
    def delete(cls, id):
        if isinstance(id, str):
            id = ObjectId(id)
        cls.collection.delete_one({'_id': id})

# ---------- Booking Helper ----------
class BookingManager:
    collection = MongoDB.get_collection('bookings')

    @classmethod
    def all(cls):
        return list(cls.collection.find().sort('date', -1))

    @classmethod
    def filter(cls, query_dict):
        return list(cls.collection.find(query_dict).sort('date', -1))

    @classmethod
    def get(cls, id):
        if isinstance(id, str):
            id = ObjectId(id)
        return cls.collection.find_one({'_id': id})

    @classmethod
    def create(cls, data):
        return cls.collection.insert_one(data).inserted_id

    @classmethod
    def update(cls, id, data):
        if isinstance(id, str):
            id = ObjectId(id)
        cls.collection.update_one({'_id': id}, {'$set': data})

    @classmethod
    def delete(cls, id):
        if isinstance(id, str):
            id = ObjectId(id)
        cls.collection.delete_one({'_id': id})

# ---------- HeadOfficeReport Helper ----------
class HOManager:
    collection = MongoDB.get_collection('ho_reports')

    @classmethod
    def all(cls):
        return list(cls.collection.find().sort('date', -1))

    @classmethod
    def create(cls, data):
        return cls.collection.insert_one(data).inserted_id

# ---------- Expense Helper ----------
class ExpenseManager:
    collection = MongoDB.get_collection('expenses')

    @classmethod
    def all(cls):
        return list(cls.collection.find().sort('date', -1))

    @classmethod
    def create(cls, data):
        return cls.collection.insert_one(data).inserted_id

# ---------- Invoice Helper ----------
class InvoiceManager:
    collection = MongoDB.get_collection('invoices')

    @classmethod
    def all(cls):
        return list(cls.collection.find().sort('created_at', -1))

    @classmethod
    def create(cls, data):
        return cls.collection.insert_one(data).inserted_id

    @classmethod
    def get(cls, id):
        if isinstance(id, str):
            id = ObjectId(id)
        return cls.collection.find_one({'_id': id})

    @classmethod
    def update(cls, id, data):
        if isinstance(id, str):
            id = ObjectId(id)
        cls.collection.update_one({'_id': id}, {'$set': data})

# ---------- Tracking History Helper ----------
class TrackingHistoryManager:
    collection = MongoDB.get_collection('tracking_history')

    @classmethod
    def get_by_tracking_id(cls, tracking_id):
        return list(cls.collection.find({'tracking_id': tracking_id}).sort('timestamp', 1))

    @classmethod
    def create(cls, data):
        return cls.collection.insert_one(data).inserted_id