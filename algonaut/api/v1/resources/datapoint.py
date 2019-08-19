from algonaut.models import Datapoint
from ..forms import DatapointForm
from .object import Objects, ObjectDetails

Datapoints = Objects(Datapoint, DatapointForm)
DatapointDetails = ObjectDetails(Datapoint, DatapointForm)
