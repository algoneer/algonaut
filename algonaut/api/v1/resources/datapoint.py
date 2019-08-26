from algonaut.models import Datapoint, Dataset, Project, DatasetDatapoint
from ..forms import DatapointForm
from .object import Objects, ObjectDetails

Datapoints = Objects(Datapoint, DatapointForm, [Dataset, Project], DatasetDatapoint)
DatapointDetails = ObjectDetails(
    Datapoint, DatapointForm, [Dataset, Project], DatasetDatapoint
)
