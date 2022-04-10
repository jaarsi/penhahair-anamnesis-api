from contextlib import contextmanager
from pymongo import MongoClient
from . import consts

@contextmanager
def get_database():
    client = MongoClient(consts.MONGO_URI)
    yield client.get_default_database()
    client.close()