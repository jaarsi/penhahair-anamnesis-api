# pylint: disable=invalid-name
# pylint: disable=wrong-import-order
# pylint: disable=protected-access

from functools import wraps
from typing import Callable
import jwt
from datetime import datetime, timedelta
from flask import Blueprint, g, jsonify, request
from app import consts, services

router = Blueprint("auth", __name__)

def authentication_required(f: Callable):
    @wraps(f)
    def w(*args, **kwargs):
        if not (auth_token := request.headers.get("Authorization")):
            return jsonify(error="Authorization header invalid or not found"), 403

        payload = jwt.decode(auth_token, consts.SECRET_KEY, algorithms=["HS256"])

        if not (user := services.get_user(payload.get("user_id"))):
            return jsonify(error="User not found"), 401

        g.user = user
        return f(*args, **kwargs)

    return w

@router.get("/token")
def token_route():
    consumer_token = request.args.get("consumerToken")
    email = request.args.get("email")
    password = request.args.get("password")

    if not services.get_api_consumer(consumer_id=consumer_token):
        return jsonify(error="Invalid consumer token"), 401

    if not (user := services.find_user(email, password)):
        return jsonify(error="Invalid email/password"), 400

    return jwt.encode(
        {
            "exp": datetime.utcnow() + timedelta(days=7),
            "user_id": user._id,
        },
        consts.SECRET_KEY,
        algorithm="HS256"
    )
