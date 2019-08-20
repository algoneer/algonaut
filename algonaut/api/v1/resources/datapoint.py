from algonaut.models import Datapoint, Dataset
from ..forms import DatapointForm
from .object import Objects, ObjectDetails

Datapoints = Objects(Datapoint, DatapointForm, [Dataset])
DatapointDetails = ObjectDetails(Datapoint, DatapointForm, [Dataset])
