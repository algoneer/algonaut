from algonaut.models import Model, AlgorithmVersion, DatasetVersion
from ..forms import ModelForm
from .object import Objects, ObjectDetails

# Returns models for a given dataset version
DatasetModels = Objects(Model, ModelForm, DatasetVersion)
DatasetModelDetails = ObjectDetails(Model, ModelForm, DatasetVersion)

# Returns models for a given algorithm version
AlgorithmModels = Objects(Model, ModelForm, AlgorithmVersion)
AlgorithmModelDetails = ObjectDetails(Model, ModelForm, AlgorithmVersion)
