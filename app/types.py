# pylint: disable=invalid-name

from dataclasses import dataclass
from bson import ObjectId
import marshmallow as mm
import marshmallow_dataclass as mmdc

class ObjectIdField(mm.fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        return ObjectId(value)

    def _deserialize(self, value, attr, data, **kwargs):
        return str(value)

ObjectIdType = mmdc.NewType("ObjectIdType", str, field=ObjectIdField)

@dataclass
class Customer:
    _id: ObjectIdType
    name: str

class CustomerSchema(mmdc.class_schema(Customer)):
    class Meta:
        unknown = mm.EXCLUDE

@dataclass
class AnamneseField:
    _id: ObjectIdType
    name: str
    description: str
    position: int
    enabled: bool

class AnamneseFieldSchema(mmdc.class_schema(AnamneseField)):
    class Meta:
        unknown = mm.EXCLUDE