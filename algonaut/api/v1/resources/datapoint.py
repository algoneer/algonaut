from algonaut.models import Datapoint, DatasetVersion, Dataset, DatasetVersionDatapoint
from ..forms import DatapointForm
from .object import Objects, ObjectDetails

Datapoints = Objects(
    Datapoint, DatapointForm, [DatasetVersion, Dataset], DatasetVersionDatapoint
)
DatapointDetails = ObjectDetails(
    Datapoint, DatapointForm, [DatasetVersion, Dataset], DatasetVersionDatapoint
)
