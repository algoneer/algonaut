from algonaut.models import DataSchema
from ..forms import DataSchemaForm
from .object import Objects, ObjectDetails

args = [DataSchema, DataSchemaForm]

DataSchemas = Objects(*args)
DataSchemaDetails = ObjectDetails(*args)
