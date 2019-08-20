from algonaut.models import (
    Result,
    Model,
    AlgorithmVersion,
    DatasetVersion,
    Dataset,
    Algorithm,
)
from ..forms import ResultForm
from .object import Objects, ObjectDetails

# Returns results for a given dataset version
DatasetResults = Objects(Result, ResultForm, [DatasetVersion, Dataset])
DatasetResultDetails = ObjectDetails(Result, ResultForm, [DatasetVersion, Dataset])

# Returns results for a given algorithm version
AlgorithmResults = Objects(Result, ResultForm, [AlgorithmVersion, Algorithm])
AlgorithmResultDetails = ObjectDetails(
    Result, ResultForm, [AlgorithmVersion, Algorithm]
)

# Returns results for a given model version
ModelResults = Objects(Result, ResultForm, [Model, AlgorithmVersion, Algorithm])
ModelResultDetails = ObjectDetails(
    Result, ResultForm, [Model, AlgorithmVersion, Algorithm]
)
