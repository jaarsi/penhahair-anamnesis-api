from flask import Blueprint, jsonify
from . import services

router = Blueprint("api", __name__)

@router.get("/show_database_info")
def show_database_info_route():
    return jsonify(services.get_database_info())

@router.get("/list_customers")
def list_customers_route():
    return jsonify(customers=services.get_customers())

@router.post("/create_anamnese")
def create_anamnese():
    pass