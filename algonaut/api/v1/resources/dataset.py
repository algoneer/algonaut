from algonaut.models import Dataset
from ..forms import DatasetForm
from .object import Objects, ObjectDetails

Datasets = Objects(Dataset, DatasetForm)
DatasetDetails = ObjectDetails(Dataset, DatasetForm)
