from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from . import services

router = Blueprint("api", __name__)

@router.errorhandler(Exception)
def handle_general_error(error: Exception):
    return jsonify(error=str(error)), 500

@router.errorhandler(ValidationError)
def handle_validation_error(error: ValidationError):
    return jsonify(errors=error.messages), 400

@router.get("/database_info")
def get_database_info_route():
    return jsonify(database_info=services.get_database_info())

@router.get("/customers")
def list_customers_route():
    return jsonify(customers=services.get_customers())

@router.get("/anamnese_fields")
def list_anamnese_fields_route():
    return jsonify(anamnese_fields=services.get_anamnese_fields())

@router.post("/anamnese_field")
def create_anamnese_field_route():
    response = services.create_anamnese_field(request.get_json())
    return jsonify(anamnese_field=response), 201

@router.put("/anamnese_field/<str:id>")
def update_anamnese_field_route(id: str):
    response = services.create_anamnese_field(request.get_json())
    return jsonify(anamnese_field=response), 200

@router.post("/anamnese")
def create_anamnese_route():
    response = services.create_anamnese(request.get_json())
    return jsonify(anamnese=response), 201
