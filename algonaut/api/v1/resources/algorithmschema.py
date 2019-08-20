from algonaut.models import (
    AlgorithmSchema,
    AlgorithmVersionAlgorithmSchema,
    AlgorithmVersion,
    Algorithm,
)
from ..forms import AlgorithmSchemaForm
from .object import Objects, ObjectDetails

AlgorithmSchemas = Objects(
    AlgorithmSchema,
    AlgorithmSchemaForm,
    [AlgorithmVersion, Algorithm],
    AlgorithmVersionAlgorithmSchema,
)
AlgorithmSchemaDetails = ObjectDetails(
    AlgorithmSchema,
    AlgorithmSchemaForm,
    [AlgorithmVersion, Algorithm],
    AlgorithmVersionAlgorithmSchema,
)
