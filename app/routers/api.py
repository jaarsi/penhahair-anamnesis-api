from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from .auth import authentication_required
from .. import services

router = Blueprint("api", __name__)

@router.errorhandler(ValidationError)
def handle_validation_error(error: ValidationError):
    return jsonify(errors=error.messages), 400

# Customers
@router.get("/customers")
@authentication_required
def list_customers_route():
    return jsonify(customers=services.get_customers())

@router.post("/customer")
@authentication_required
def create_customer_route():
    response = services.create_customer(request.get_json())
    return jsonify(customer=response), 201

@router.put("/customer/<customer_id>")
@authentication_required
def update_customer_route(customer_id: str):
    response = services.update_customer(customer_id, request.get_json())
    return jsonify(customer=response)

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
    return jsonify(anamnesis_field=response)

# Anamnesis
@router.get("/anamnesis/<anamnesis_id>")
@authentication_required
def get_anamnesis_route(anamnesis_id: str):
    response = services.get_anamnesis(anamnesis_id)
    return jsonify(anamnesis=response)

@router.post("/anamnesis")
@authentication_required
def create_anamnesis_route():
    response = services.create_anamnesis(request.get_json())
    return jsonify(anamnesis=response), 201

@router.put("/anamnesis/<anamnesis_id>")
@authentication_required
def update_anamnesis_route(anamnesis_id: str):
    response = services.update_anamnesis(anamnesis_id, request.get_json())
    return jsonify(anamnesis=response)

@router.get("/customer/<customer_id>/anamnesis")
@authentication_required
def list_customer_anamnesis_route(customer_id: str):
    return jsonify(anamnesis=services.get_customer_anamnesis_list(customer_id))
