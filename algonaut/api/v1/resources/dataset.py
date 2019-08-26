from algonaut.models import Dataset, Project
from ..forms import DatasetForm
from .object import Objects, ObjectDetails

joins = [[Dataset.project, Project.organization]]

Datasets = Objects(Dataset, DatasetForm, [Project], Joins=joins)
DatasetDetails = ObjectDetails(Dataset, DatasetForm, [Project], Joins=joins)
