from typing import List, Dict, Tuple, Any, Type
from ..resource import Resource

from .resources.algorithm import Algorithms

routes: List[Dict[str, Tuple[Type[Resource], Dict[str, Any]]]] = [
    {"/algorithms": (Algorithms, {"methods": ["GET"]})}
]
