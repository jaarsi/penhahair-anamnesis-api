# pylint: disable=wrong-import-position

from dotenv import load_dotenv

load_dotenv()

from flask import Flask
from app.router import router

app = Flask(__name__, static_folder=None)
app.register_blueprint(router)