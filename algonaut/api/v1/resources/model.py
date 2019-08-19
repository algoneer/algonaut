from algonaut.models import Model
from ..forms import ModelForm
from .object import Objects, ObjectDetails

Models = Objects(Model, ModelForm)
ModelDetails = ObjectDetails(Model, ModelForm)
