from algonaut.models import Model, AlgorithmVersion, DatasetVersion, Dataset, Algorithm
from ..forms import ModelForm
from .object import Objects, ObjectDetails

# Returns models for a given dataset version
DatasetModels = Objects(Model, ModelForm, [DatasetVersion, Dataset])
DatasetModelDetails = ObjectDetails(Model, ModelForm, [DatasetVersion, Dataset])

# Returns models for a given algorithm version
AlgorithmModels = Objects(Model, ModelForm, [AlgorithmVersion, Algorithm])
AlgorithmModelDetails = ObjectDetails(Model, ModelForm, [AlgorithmVersion, Algorithm])
