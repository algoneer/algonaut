from algonaut.settings import settings
from algonaut.models import (
    Algorithm,
    AlgorithmVersion,
    AlgorithmSchema,
    AlgorithmVersionAlgorithmSchema,
)
from ..auth_client import PlainAuthClient, PlainUser, PlainAccessToken
from ..helpers import DatabaseTest

from typing import Any, Dict


def algorithm(test: DatabaseTest, fixtures: Dict[str, Any], path: str) -> Any:
    algorithm = Algorithm(path=path)
    test.session.add(algorithm)
    test.session.commit()
    return algorithm


def algorithmversion(
    test: DatabaseTest, fixtures: Dict[str, Any], algo: str = "algorithm"
) -> Any:
    algorithm = fixtures[algo]
    algorithmversion = AlgorithmVersion(algorithm=algorithm, hash=b"foo")
    test.session.add(algorithmversion)
    test.session.commit()
    return algorithmversion


def algorithmschema(test: DatabaseTest, fixtures: Dict[str, Any]) -> Any:
    algorithmschema = AlgorithmSchema(hash=b"foo")
    test.session.add(algorithmschema)
    test.session.commit()
    return algorithmschema


def algorithmversion_algorithmschema(
    test: DatabaseTest,
    fixtures: Dict[str, Any],
    algoschema: str = "algorithmschema",
    algoversion: str = "algorithmversion",
) -> Any:
    algorithmschema = fixtures[algoschema]
    algorithmversion = fixtures[algoversion]
    algorithmversion_algorithmschema = AlgorithmVersionAlgorithmSchema(
        algorithmschema=algorithmschema, algorithmversion=algorithmversion
    )
    test.session.add(algorithmversion_algorithmschema)
    test.session.commit()
    return algorithmversion_algorithmschema
