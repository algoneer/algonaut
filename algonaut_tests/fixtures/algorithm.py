from algonaut.settings import settings
from algonaut.models import Algorithm
from ..auth_client import PlainAuthClient, PlainUser, PlainAccessToken
from ..helpers import DatabaseTest

from typing import Any, Dict

def algorithm(test : DatabaseTest, fixtures : Dict[str, Any], path: str) -> Any:
    algorithm = Algorithm(path=path)
    test.session.add(algorithm)
    test.session.commit()
    return algorithm
