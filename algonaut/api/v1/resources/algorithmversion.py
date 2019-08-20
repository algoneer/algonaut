from algonaut.models import AlgorithmVersion, Algorithm
from ..forms import AlgorithmVersionForm
from .object import Objects, ObjectDetails

AlgorithmVersions = Objects(AlgorithmVersion, AlgorithmVersionForm, [Algorithm])
AlgorithmVersionDetails = ObjectDetails(
    AlgorithmVersion, AlgorithmVersionForm, [Algorithm]
)
