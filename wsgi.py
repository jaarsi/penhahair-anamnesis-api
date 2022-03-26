# pylint: disable=wrong-import-position
# pylint: disable=wrong-import-order

from dotenv import load_dotenv

load_dotenv()

import os
from flask import Flask, jsonify
from app import routers

app = Flask(__name__, static_folder=None)
app.secret_key = os.getenv("FLASK_SECRET_KEY", None)
app.register_blueprint(routers.auth_router, url_prefix="/auth")
app.register_blueprint(routers.api_router, url_prefix="/api")

@app.errorhandler(Exception)
def handle_general_error(error: Exception):
    return jsonify(error=str(error)), 500