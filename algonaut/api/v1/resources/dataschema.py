from algonaut.models import DataSchema
from ..forms import DataSchemaForm
from .object import Objects, ObjectDetails

DataSchemas = Objects(DataSchema, DataSchemaForm)
DataSchemaDetails = ObjectDetails(DataSchema, DataSchemaForm)
