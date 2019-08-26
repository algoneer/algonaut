from algonaut.models import DataSchema, DatasetDataSchema, Dataset, Project
from ..forms import DataSchemaForm
from .object import Objects, ObjectDetails

DataSchemas = Objects(DataSchema, DataSchemaForm, [Dataset, Project], DatasetDataSchema)
DataSchemaDetails = ObjectDetails(
    DataSchema, DataSchemaForm, [Dataset, Project], DatasetDataSchema
)
