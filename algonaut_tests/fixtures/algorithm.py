from algonaut.settings import settings
from algonaut.models import (
    Algorithm,
    AlgorithmVersion,
    AlgorithmSchema,
    AlgorithmVersionAlgorithmSchema,
)
from ..auth import PlainAuthClient
from ..helpers import DatabaseTest

from typing import Any, Dict, Type
import unittest


def algorithm(
    test: Type[unittest.TestCase],
    fixtures: Dict[str, Any],
    path: str,
    organization: str = "organization",
) -> Any:
    assert issubclass(test, DatabaseTest)
    org = fixtures[organization]
    algorithm = Algorithm(path=path, organization=org)
    test.session.add(algorithm)
    test.session.commit()
    return algorithm


def algorithmversion(
    test: Type[unittest.TestCase], fixtures: Dict[str, Any], algo: str = "algorithm"
) -> Any:
    assert issubclass(test, DatabaseTest)
    algorithm = fixtures[algo]
    algorithmversion = AlgorithmVersion(algorithm=algorithm, hash=b"foo")
    test.session.add(algorithmversion)
    test.session.commit()
    return algorithmversion


def algorithmschema(test: Type[unittest.TestCase], fixtures: Dict[str, Any]) -> Any:
    assert issubclass(test, DatabaseTest)
    algorithmschema = AlgorithmSchema(hash=b"foo")
    test.session.add(algorithmschema)
    test.session.commit()
    return algorithmschema


def algorithmversion_algorithmschema(
    test: Type[unittest.TestCase],
    fixtures: Dict[str, Any],
    algoschema: str = "algorithmschema",
    algoversion: str = "algorithmversion",
) -> Any:
    assert issubclass(test, DatabaseTest)
    algorithmschema = fixtures[algoschema]
    algorithmversion = fixtures[algoversion]
    algorithmversion_algorithmschema = AlgorithmVersionAlgorithmSchema(
        algorithmschema=algorithmschema, algorithmversion=algorithmversion
    )
    test.session.add(algorithmversion_algorithmschema)
    test.session.commit()
    return algorithmversion_algorithmschema
