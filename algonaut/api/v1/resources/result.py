from algonaut.models import Result
from ..forms import ResultForm
from .object import Objects, ObjectDetails

Results = Objects(Result, ResultForm)
ResultDetails = ObjectDetails(Result, ResultForm)
