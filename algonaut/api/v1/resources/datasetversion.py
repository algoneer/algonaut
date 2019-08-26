from algonaut.models import DatasetVersion, Dataset
from ..forms import DatasetVersionForm
from .object import Objects, ObjectDetails

joins = [[DatasetVersion.dataset, Dataset.organization]]

DatasetVersions = Objects(DatasetVersion, DatasetVersionForm, [Dataset], Joins=joins)
DatasetVersionDetails = ObjectDetails(
    DatasetVersion, DatasetVersionForm, [Dataset], Joins=joins
)
