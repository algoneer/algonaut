from algonaut.models import AlgorithmVersion, Algorithm
from ..forms import AlgorithmVersionForm
from .object import Objects, ObjectDetails

joins = [[AlgorithmVersion.algorithm, Algorithm.organization]]

AlgorithmVersions = Objects(
    AlgorithmVersion, AlgorithmVersionForm, [Algorithm], Joins=joins
)
AlgorithmVersionDetails = ObjectDetails(
    AlgorithmVersion, AlgorithmVersionForm, [Algorithm], Joins=joins
)
