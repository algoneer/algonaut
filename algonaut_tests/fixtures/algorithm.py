from algonaut.settings import settings
from algonaut.models import Algorithm, AlgorithmVersion
from ..auth_client import PlainAuthClient, PlainUser, PlainAccessToken
from ..helpers import DatabaseTest

from typing import Any, Dict

def algorithm(test : DatabaseTest, fixtures : Dict[str, Any], path: str) -> Any:
    algorithm = Algorithm(path=path)
    test.session.add(algorithm)
    test.session.commit()
    return algorithm

def algorithmversion(test : DatabaseTest, fixtures : Dict[str, Any], algo: str = "algorithm") -> Any:
    algorithm = fixtures[algo]
    algorithmversion = AlgorithmVersion(algorithm=algorithm, hash=b"foo")
    test.session.add(algorithmversion)
    test.session.commit()
    return algorithmversion