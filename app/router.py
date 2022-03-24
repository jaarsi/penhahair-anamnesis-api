from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from . import services

router = Blueprint("api", __name__)

@router.get("/show_database_info")
def show_database_info_route():
    try:
        return jsonify(database_info=services.get_database_info())
    except Exception as error:
        return jsonify(error=str(error)), 500

@router.get("/list_customers")
def list_customers_route():
    try:
        return jsonify(customers=services.get_customers())
    except Exception as error:
        return jsonify(error=str(error)), 500

@router.get("/list_anamnese_fields")
def list_anamnese_fields_route():
    try:
        return jsonify(anamnese_fields=services.get_anamnese_fields())
    except Exception as error:
        return jsonify(error=str(error)), 500

@router.post("/create_anamnese")
def create_anamnese_route():
    try:
        response = services.create_anamnese(request.get_json())
        return jsonify(anamnese=response), 201
    except ValidationError as error:
        return jsonify(errors=error.messages), 400
    except Exception as error:
        return jsonify(error=str(error)), 500

@router.post("/create_anamnese_field")
def create_anamnese_field_route():
    try:
        response = services.create_anamnese_field(request.get_json())
        return jsonify(anamnese_field=response), 201
    except ValidationError as error:
        return jsonify(errors=error.messages), 400
    except Exception as error:
        return jsonify(error=str(error)), 500
