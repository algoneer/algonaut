from algonaut.models import Dataset
from ..forms import DatasetForm
from .object import Objects, ObjectDetails

joins = [[Dataset.organization]]

Datasets = Objects(Dataset, DatasetForm, Joins=joins)
DatasetDetails = ObjectDetails(Dataset, DatasetForm, Joins=joins)
