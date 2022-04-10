# pylint: disable=wrong-import-position
# pylint: disable=wrong-import-order

from dotenv import load_dotenv

load_dotenv()

from flask import Flask, jsonify
from app import routers, consts

app = Flask(__name__, static_folder=None)
app.secret_key = consts.SECRET_KEY
app.register_blueprint(routers.auth_router, url_prefix="/auth")
app.register_blueprint(routers.api_router, url_prefix="/api")

@app.errorhandler(Exception)
def _(error: Exception):
    return jsonify(error=str(error)), 500