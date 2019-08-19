from algonaut.models import AlgorithmVersion, Algorithm
from ..forms import AlgorithmVersionForm
from .object import Objects, ObjectDetails

args = [AlgorithmVersion, AlgorithmVersionForm, Algorithm]

AlgorithmVersions = Objects(*args)
AlgorithmVersionDetails = ObjectDetails(*args)
