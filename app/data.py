import os
from contextlib import contextmanager
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI", "localhost")

@contextmanager
def get_database():
    client = MongoClient(MONGO_URI)
    yield client.get_default_database()
    client.close()