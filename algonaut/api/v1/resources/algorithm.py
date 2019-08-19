from algonaut.models import Algorithm
from ..forms import AlgorithmForm
from .object import Objects, ObjectDetails

Algorithms = Objects(Algorithm, AlgorithmForm)
AlgorithmDetails = ObjectDetails(Algorithm, AlgorithmForm)
