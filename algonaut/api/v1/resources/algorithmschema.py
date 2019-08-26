from algonaut.models import (
    AlgorithmSchema,
    AlgorithmAlgorithmSchema,
    Algorithm,
    Project,
)
from ..forms import AlgorithmSchemaForm
from .object import Objects, ObjectDetails

AlgorithmSchemas = Objects(
    AlgorithmSchema, AlgorithmSchemaForm, [Algorithm, Project], AlgorithmAlgorithmSchema
)
AlgorithmSchemaDetails = ObjectDetails(
    AlgorithmSchema, AlgorithmSchemaForm, [Algorithm, Project], AlgorithmAlgorithmSchema
)
