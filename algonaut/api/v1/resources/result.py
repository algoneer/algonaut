from algonaut.models import (
    Result,
    Model,
    ModelResult,
    AlgorithmVersionResult,
    DatasetVersionResult,
    AlgorithmVersion,
    DatasetVersion,
    Dataset,
    Algorithm,
)
from ..forms import ResultForm
from .object import Objects, ObjectDetails

# Returns results for a given dataset version
DatasetVersionResults = Objects(
    Result, ResultForm, [DatasetVersion, Dataset], DatasetVersionResult
)
DatasetVersionResultDetails = ObjectDetails(
    Result, ResultForm, [DatasetVersion, Dataset], DatasetVersionResult
)

# Returns results for a given algorithm version
AlgorithmVersionResults = Objects(
    Result, ResultForm, [AlgorithmVersion, Algorithm], AlgorithmVersionResult
)
AlgorithmVersionResultDetails = ObjectDetails(
    Result, ResultForm, [AlgorithmVersion, Algorithm], AlgorithmVersionResult
)

# Returns results for a given model version
ModelResults = Objects(
    Result, ResultForm, [Model, AlgorithmVersion, Algorithm], ModelResult
)
ModelResultDetails = ObjectDetails(
    Result, ResultForm, [Model, AlgorithmVersion, Algorithm], ModelResult
)
