from algonaut.models import Dataset
from ..forms import DatasetForm
from .object import Objects, ObjectDetails

args = [Dataset, DatasetForm]

Datasets = Objects(*args)
DatasetDetails = ObjectDetails(*args)
