from algonaut.models import (
    DataSchema,
    DatasetVersionDataSchema,
    DatasetVersion,
    Dataset,
)
from ..forms import DataSchemaForm
from .object import Objects, ObjectDetails

DataSchemas = Objects(
    DataSchema, DataSchemaForm, [DatasetVersion, Dataset], DatasetVersionDataSchema
)
DataSchemaDetails = ObjectDetails(
    DataSchema, DataSchemaForm, [DatasetVersion, Dataset], DatasetVersionDataSchema
)
