from algonaut.models import Datapoint, Dataset
from ..forms import DatapointForm
from .object import Objects, ObjectDetails

args = [Datapoint, DatapointForm, Dataset]

Datapoints = Objects(*args)
DatapointDetails = ObjectDetails(*args)
