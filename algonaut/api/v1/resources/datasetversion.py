from algonaut.models import DatasetVersion, Dataset
from ..forms import DatasetVersionForm
from .object import Objects, ObjectDetails

DatasetVersions = Objects(DatasetVersion, DatasetVersionForm, [Dataset])
DatasetVersionDetails = ObjectDetails(DatasetVersion, DatasetVersionForm, [Dataset])
