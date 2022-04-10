import os

SECRET_KEY = os.getenv("SECRET_KEY", None)
MONGO_URI = os.getenv("MONGO_URI", "localhost")