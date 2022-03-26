# pylint: disable=invalid-name

from dataclasses import dataclass
from datetime import datetime
from typing import List
from bson import ObjectId
import marshmallow as mm
import marshmallow_dataclass as mmdc

class ObjectIdField(mm.fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        return ObjectId(value)

    def _deserialize(self, value, attr, data, **kwargs):
        return str(value)

ObjectIdFieldType = mmdc.NewType("ObjectIdType", str, field=ObjectIdField)

@dataclass
class Customer:
    _id: ObjectIdFieldType
    name: str

class CustomerSchema(mmdc.class_schema(Customer)):
    class Meta:
        unknown = mm.EXCLUDE

@dataclass
class AnamnesisField:
    _id: ObjectIdFieldType
    name: str
    description: str
    position: int
    enabled: bool

class AnamnesisFieldSchema(mmdc.class_schema(AnamnesisField)):
    class Meta:
        unknown = mm.EXCLUDE

@dataclass
class Anamnesis:
    _id: ObjectIdFieldType
    customer_id: str
    time: datetime
    answers: List[dict]

class AnamnesisSchema(mmdc.class_schema(Anamnesis)):
    class Meta:
        unknown = mm.EXCLUDE
