from algonaut.models import Result, Model, AlgorithmVersion, DatasetVersion
from ..forms import ResultForm
from .object import Objects, ObjectDetails

# Returns results for a given dataset version
DatasetResults = Objects(Result, ResultForm, DatasetVersion)
DatasetResultDetails = ObjectDetails(Result, ResultForm, DatasetVersion)

# Returns results for a given algorithm version
AlgorithmResults = Objects(Result, ResultForm, AlgorithmVersion)
AlgorithmResultDetails = ObjectDetails(Result, ResultForm, AlgorithmVersion)

# Returns results for a given model version
ModelResults = Objects(Result, ResultForm, Model)
ModelResultDetails = ObjectDetails(Result, ResultForm, Model)
