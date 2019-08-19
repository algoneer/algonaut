from algonaut.models import AlgorithmSchema
from ..forms import AlgorithmSchemaForm
from .object import Objects, ObjectDetails

args = [AlgorithmSchema, AlgorithmSchemaForm]

AlgorithmSchemas = Objects(*args)
AlgorithmSchemaDetails = ObjectDetails(*args)
