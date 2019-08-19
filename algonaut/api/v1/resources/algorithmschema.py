from algonaut.models import AlgorithmSchema
from ..forms import AlgorithmSchemaForm
from .object import Objects, ObjectDetails

AlgorithmSchemas = Objects(AlgorithmSchema, AlgorithmSchemaForm)
AlgorithmSchemaDetails = ObjectDetails(AlgorithmSchema, AlgorithmSchemaForm)
