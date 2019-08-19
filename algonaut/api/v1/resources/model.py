from algonaut.models import Model, AlgorithmVersion, DatasetVersion
from ..forms import ModelForm
from .object import Objects, ObjectDetails

DatasetModels = Objects(Model, ModelForm, DatasetVersion)
DatasetModelDetails = ObjectDetails(Model, ModelForm, DatasetVersion)

AlgorithmModels = Objects(Model, ModelForm, AlgorithmVersion)
AlgorithmModelDetails = ObjectDetails(Model, ModelForm, AlgorithmVersion)
