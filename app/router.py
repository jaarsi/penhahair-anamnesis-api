from urllib.parse import urljoin, urlencode, urlparse
from functools import wraps
from flask import Blueprint, jsonify, request, redirect, session, url_for
from marshmallow import ValidationError
from . import services, auth

router = Blueprint("api", __name__)

@router.errorhandler(Exception)
def handle_general_error(error: Exception):
    return jsonify(error=str(error)), 500

@router.errorhandler(ValidationError)
def handle_validation_error(error: ValidationError):
    return jsonify(errors=error.messages), 400


def authentication_required(f):
    # pylint: disable=invalid-name
    @wraps(f)
    def g(*args, **kwargs):
        state, token = session.get("state", None), session.get("token", None)

        if not auth.google_userinfo(token=token, state=state):
            session["next"] = request.endpoint
            return redirect(url_for("api.authentication_route"))

        return f(*args, **kwargs)

    return g

# Authentication
@router.get("/auth")
def authentication_route():
    state, token = session.get("state", None), session.get("token", None)
    redirect_uri = urljoin(request.host_url, url_for("api.authentication_callback_route"))
    authorization_url, state = auth.google_authorization(
        token=token,
        state=state,
        redirect_uri=redirect_uri,
    )
    session["state"] = state
    return redirect(authorization_url)

@router.get("/auth/callback")
def authentication_callback_route():
    state, token = session.get("state", None), session.get("token", None)
    redirect_uri = urljoin(request.host_url, url_for("api.authentication_callback_route"))
    token = auth.google_token(request.url, token=token, state=state, redirect_uri=redirect_uri)
    session["token"] = token
    session["user_info"] = auth.google_userinfo(token=token, state=state)
    target_url = session.get("next", None)
    return redirect(url_for(target_url))

# General
@router.get("/database_info")
@authentication_required
def get_database_info_route():
    return jsonify(database_info=services.get_database_info())

# Customers
@router.get("/customers")
@authentication_required
def list_customers_route():
    return jsonify(customers=services.get_customers())

# Anamnesis Fields
@router.get("/anamnesis_fields")
@authentication_required
def list_anamnesis_fields_route():
    return jsonify(anamnesis_fields=services.get_anamnesis_fields_list())

@router.post("/anamnesis_field")
@authentication_required
def create_anamnesis_field_route():
    response = services.create_anamnesis_field(request.get_json())
    return jsonify(anamnesis_field=response), 201

@router.put("/anamnesis_field/<anamnesis_field_id>")
@authentication_required
def update_anamnesis_field_route(anamnesis_field_id: str):
    response = services.update_anamnesis_field(anamnesis_field_id, request.get_json())
    return jsonify(anamnesis_field=response), 200

# Anamnesis
@router.get("/anamnesis/<anamnesis_id>")
@authentication_required
def get_anamnesis_route(anamnesis_id: str):
    response = services.get_anamnesis(anamnesis_id)
    return jsonify(anamnesis=response), 200

@router.post("/anamnesis")
@authentication_required
def create_anamnesis_route():
    response = services.create_anamnesis(request.get_json())
    return jsonify(anamnesis=response), 201

@router.put("/anamnesis/<anamnesis_id>")
@authentication_required
def update_anamnesis_route(anamnesis_id: str):
    response = services.update_anamnesis(anamnesis_id, request.get_json())
    return jsonify(anamnesis=response), 200

@router.get("/customer/<customer_id>/anamnesis")
@authentication_required
def list_customer_anamnesis_route(customer_id: str):
    return jsonify(anamnesis=services.get_customer_anamnesis_list(customer_id))
