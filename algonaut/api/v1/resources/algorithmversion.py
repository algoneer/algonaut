from algonaut.models import AlgorithmVersion
from ..forms import AlgorithmVersionForm
from .object import Objects, ObjectDetails

AlgorithmVersions = Objects(AlgorithmVersion, AlgorithmVersionForm)
AlgorithmVersionDetails = ObjectDetails(AlgorithmVersion, AlgorithmVersionForm)
