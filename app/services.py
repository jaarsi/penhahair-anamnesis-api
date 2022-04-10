# pylint: disable=invalid-name

from typing import List
from marshmallow import ValidationError
from bson import ObjectId
from .data import get_database
from . import types

user_schema = types.UserSchema()
customer_schema = types.CustomerSchema()
anamnesis_field_schema = types.AnamnesisFieldSchema()
anamnesis_schema = types.AnamnesisSchema()

# def create_anamnesis_schema() -> types.mm.Schema:
#     fields = get_anamnesis_fields()
#     return fields

def get_api_consumer(consumer_id: str) -> types.APIConsumer:
    with get_database() as db:
        result = db.get_collection("consumers_api").find_one(ObjectId(consumer_id))
        return types.APIConsumerSchema().load(data=result)

# Users
def find_user(email: str, password: str) -> types.User:
    with get_database() as db:
        result = db.get_collection("users").find_one({
            "email": email,
            "password": password
        })
        return user_schema.load(data=result)

def get_user(user_id: str) -> types.User:
    with get_database() as db:
        result = db.get_collection("users").find_one(ObjectId(user_id))
        return user_schema.load(data=result)

# Customers
def get_customers(user_id: str) -> List[types.Customer]:
    with get_database() as db:
        results = list(db.get_collection("customers").find({
            "user_id": ObjectId(user_id)
        }))
        return customer_schema.load(data=results, many=True)

def create_customer(user_id: str, customer: dict) -> types.Customer:
    if errors := customer_schema.validate(data=customer, partial=("_id",)):
        raise ValidationError(errors)

    with get_database() as db:
        db.get_collection("customers").insert_one({
            **customer,
            "user_id": user_id
        })
        return anamnesis_schema.load(data=customer)

def update_customer(user_id: str, customer_id: str, customer: dict) -> types.Customer:
    if errors := customer_schema.validate(data=customer, partial=("_id",)):
        raise ValidationError(errors)

    with get_database() as db:
        db.get_collection("customers").find_one_and_replace(
            {
                "_id": ObjectId(customer_id),
                "user_id": ObjectId(user_id)
            },
            customer
        )
        return anamnesis_schema.load(data=customer)

# Anamnesis Fields
def get_anamnesis_fields_list(user_id: str) -> List[types.AnamnesisField]:
    with get_database() as db:
        results = list(db.get_collection("anamnesis_fields").find({
            "user_id": ObjectId(user_id),
            "enabled": True
        }))
        return anamnesis_field_schema.load(data=results, many=True)

def create_anamnesis_field(user_id: str, anamnesis_field: dict) -> types.AnamnesisField:
    if errors := anamnesis_field_schema.validate(data=anamnesis_field, partial=("_id",)):
        raise ValidationError(errors)

    with get_database() as db:
        db.get_collection("anamnesis_field").insert_one({
            **anamnesis_field,
            "user_id": user_id
        })
        return anamnesis_field_schema.load(data=anamnesis_field)

def update_anamnesis_field(
    user_id: str,
    anamnesis_field_id: str,
    anamnesis_field: dict
) -> types.AnamnesisField:
    if errors := anamnesis_field_schema.validate(data=anamnesis_field, partial=("_id",)):
        raise ValidationError(errors)

    with get_database() as db:
        db.get_collection("anamnesis_field").find_one_and_replace(
            {
                "_id": ObjectId(anamnesis_field_id),
                "user_id": ObjectId(user_id)
            },
            anamnesis_field
        )
        return anamnesis_field_schema.load(data=anamnesis_field)

# Anamnesis
def get_anamnesis(user_id: str, anamnesis_id: str) -> List[types.Anamnesis]:
    with get_database() as db:
        result = db.get_collection("anamnesis").find_one({
            "_id": ObjectId(anamnesis_id),
            "user_id": ObjectId(user_id)
        })
        return anamnesis_schema.load(data=result)

def create_anamnesis(user_id: str, anamnesis: dict) -> types.Anamnesis:
    if errors := anamnesis_schema.validate(data=anamnesis, partial=("_id",)):
        raise ValidationError(errors)

    with get_database() as db:
        db.get_collection("anamnesis").insert_one({
            **anamnesis,
            "user_id": user_id
        })
        return anamnesis_schema.load(data=anamnesis)

def update_anamnesis(user_id: str, anamnesis_id: str, anamnesis: dict) -> types.Anamnesis:
    if errors := anamnesis_schema.validate(data=anamnesis, partial=("_id",)):
        raise ValidationError(errors)

    with get_database() as db:
        db.get_collection("anamnesis").find_one_and_replace(
            {
                "_id": ObjectId(anamnesis_id),
                "user_id": ObjectId(user_id)
            },
            anamnesis
        )
        return anamnesis_schema.load(data=anamnesis)

def get_customer_anamnesis_list(user_id: str, customer_id: str) -> List[types.Anamnesis]:
    with get_database() as db:
        results = list(db.get_collection("anamnesis").find({
            "customer_id": customer_id,
            "user_id": ObjectId(user_id)
        }))
        return anamnesis_schema.load(data=results, many=True)
