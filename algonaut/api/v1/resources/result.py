from algonaut.models import Result, Model, AlgorithmVersion, DatasetVersion
from ..forms import ResultForm
from .object import Objects, ObjectDetails

DatasetResults = Objects(Result, ResultForm, DatasetVersion)
DatasetResultDetails = ObjectDetails(Result, ResultForm, DatasetVersion)

AlgorithmResults = Objects(Result, ResultForm, AlgorithmVersion)
AlgorithmResultDetails = ObjectDetails(Result, ResultForm, AlgorithmVersion)

ModelResults = Objects(Result, ResultForm, Model)
ModelResultDetails = ObjectDetails(Result, ResultForm, Model)
