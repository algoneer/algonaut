from algonaut.models import Algorithm, Project
from ..forms import AlgorithmForm
from .object import Objects, ObjectDetails

joins = [[Algorithm.project, Project.organization]]

Algorithms = Objects(Algorithm, AlgorithmForm, [Project], Joins=joins)
AlgorithmDetails = ObjectDetails(Algorithm, AlgorithmForm, [Project], Joins=joins)
