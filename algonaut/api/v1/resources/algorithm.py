from algonaut.models import Algorithm
from ..forms import AlgorithmForm
from .object import Objects, ObjectDetails

joins = [[Algorithm.organization]]

Algorithms = Objects(Algorithm, AlgorithmForm, Joins=joins)
AlgorithmDetails = ObjectDetails(Algorithm, AlgorithmForm, Joins=joins)
