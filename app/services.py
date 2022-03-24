# pylint: disable=invalid-name

from typing import List
from .data import get_database
from . import types

customer_schema = types.CustomerSchema()
anamnese_field_schema = types.AnamneseFieldSchema()

# def create_anamnese_schema() -> types.mm.Schema:
#     fields = get_anamnese_fields()
#     return fields

def get_database_info() -> dict:
    with get_database() as db:
        return db.client.server_info()

def get_customers() -> List[types.Customer]:
    with get_database() as db:
        results = list(db.get_collection("customers").find())
        return customer_schema.load(data=results, many=True)

def get_anamnese_fields() -> List[types.AnamneseField]:
    with get_database() as db:
        results = list(db.get_collection("anamnese_fields").find())
        return anamnese_field_schema.load(data=results, many=True)

def create_anamnese(anamnese: dict) -> None:
    with get_database() as db:
        db.get_collection("anamneses").insert_one(anamnese)