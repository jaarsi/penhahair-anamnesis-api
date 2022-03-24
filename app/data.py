from contextlib import contextmanager
from pymongo import MongoClient

@contextmanager
def get_database():
    client = MongoClient("mongodb://server.jdnw.lan:27017/penhahair")
    yield client.get_default_database()
    client.close()