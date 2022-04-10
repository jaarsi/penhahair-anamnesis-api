# pylint: disable=protected-access

from flask import Blueprint, jsonify, request, g
from marshmallow import ValidationError
from .. import services
from . import auth

router = Blueprint("api", __name__)

@router.errorhandler(ValidationError)
def handle_validation_error(error: ValidationError):
    return jsonify(errors=error.messages), 400

@router.before_request
@auth.authentication_required
def _():
    pass

# Customers
@router.get("/customers")
def list_customers_route():
    return jsonify(customers=services.get_customers(g.user._id))

@router.post("/customer")
def create_customer_route():
    response = services.create_customer(g.user._id, request.get_json())
    return jsonify(customer=response), 201

@router.put("/customer/<customer_id>")
def update_customer_route(customer_id: str):
    response = services.update_customer(g.user._id, customer_id, request.get_json())
    return jsonify(customer=response)

# Anamnesis Fields
@router.get("/anamnesis_fields")
def list_anamnesis_fields_route():
    return jsonify(anamnesis_fields=services.get_anamnesis_fields_list(g.user._id))

@router.post("/anamnesis_field")
def create_anamnesis_field_route():
    response = services.create_anamnesis_field(g.user._id, request.get_json())
    return jsonify(anamnesis_field=response), 201

@router.put("/anamnesis_field/<anamnesis_field_id>")
def update_anamnesis_field_route(anamnesis_field_id: str):
    response = services.update_anamnesis_field(g.user._id, anamnesis_field_id, request.get_json())
    return jsonify(anamnesis_field=response)

# Anamnesis
@router.get("/anamnesis/<anamnesis_id>")
def get_anamnesis_route(anamnesis_id: str):
    response = services.get_anamnesis(g.user._id, anamnesis_id)
    return jsonify(anamnesis=response)

@router.post("/anamnesis")
def create_anamnesis_route():
    response = services.create_anamnesis(g.user._id, request.get_json())
    return jsonify(anamnesis=response), 201

@router.put("/anamnesis/<anamnesis_id>")
def update_anamnesis_route(anamnesis_id: str):
    response = services.update_anamnesis(g.user._id, anamnesis_id, request.get_json())
    return jsonify(anamnesis=response)

@router.get("/customer/<customer_id>/anamnesis")
def list_customer_anamnesis_route(customer_id: str):
    return jsonify(anamnesis=services.get_customer_anamnesis_list(g.user._id, customer_id))
