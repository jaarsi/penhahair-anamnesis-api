# pylint: disable=invalid-name

from typing import List
from marshmallow import ValidationError
from bson import ObjectId
from .data import get_database
from . import types

customer_schema = types.CustomerSchema()
anamnesis_field_schema = types.AnamnesisFieldSchema()
anamnesis_schema = types.AnamnesisSchema()

# def create_anamnesis_schema() -> types.mm.Schema:
#     fields = get_anamnesis_fields()
#     return fields

# General
def get_database_info() -> dict:
    with get_database() as db:
        return db.client.server_info()

# Customers
def get_customers() -> List[types.Customer]:
    with get_database() as db:
        results = list(db.get_collection("customers").find())
        return customer_schema.load(data=results, many=True)

# Anamnesis Fields
def get_anamnesis_fields_list() -> List[types.AnamnesisField]:
    with get_database() as db:
        results = list(db.get_collection("anamnesis_fields").find({ "enabled": True }))
        return anamnesis_field_schema.load(data=results, many=True)

def create_anamnesis_field(anamnesis_field: dict) -> types.AnamnesisField:
    if errors := anamnesis_field_schema.validate(data=anamnesis_field, partial=("_id",)):
        raise ValidationError(errors)

    with get_database() as db:
        db.get_collection("anamnesis_field").insert_one(anamnesis_field)
        return anamnesis_field_schema.load(data=anamnesis_field)

def update_anamnesis_field(anamnesis_field_id: str, anamnesis_field: dict) -> types.AnamnesisField:
    if errors := anamnesis_field_schema.validate(data=anamnesis_field, partial=("_id",)):
        raise ValidationError(errors)

    with get_database() as db:
        db.get_collection("anamnesis_field").find_one_and_replace(
            ObjectId(anamnesis_field_id), anamnesis_field
        )
        return anamnesis_field_schema.load(data=anamnesis_field)

# Anamnesis
def get_anamnesis(anamnesis_id: str) -> List[types.Anamnesis]:
    with get_database() as db:
        result = db.get_collection("anamnesis").find_one(ObjectId(anamnesis_id))
        return anamnesis_schema.load(data=result)

def create_anamnesis(anamnesis: dict) -> types.Anamnesis:
    if errors := anamnesis_schema.validate(data=anamnesis, partial=("_id",)):
        raise ValidationError(errors)

    with get_database() as db:
        db.get_collection("anamnesis").insert_one(anamnesis)
        return anamnesis_schema.load(data=anamnesis)

def update_anamnesis(anamnesis_id: str, anamnesis: dict) -> types.Anamnesis:
    if errors := anamnesis_schema.validate(data=anamnesis, partial=("_id",)):
        raise ValidationError(errors)

    with get_database() as db:
        db.get_collection("anamnesis").find_one_and_replace(
            ObjectId(anamnesis_id), anamnesis
        )
        return anamnesis_schema.load(data=anamnesis)

def get_customer_anamnesis_list(customer_id: str) -> List[types.Anamnesis]:
    with get_database() as db:
        results = list(db.get_collection("anamnesis").find({ "customer_id": customer_id }))
        return anamnesis_schema.load(data=results, many=True)
