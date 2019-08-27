from algonaut.settings import settings
from algonaut.models import (
    Project,
    Algorithm,
    AlgorithmSchema,
    AlgorithmAlgorithmSchema,
)
from ..auth import PlainAuthClient
from ..helpers import DatabaseTest

from typing import Any, Dict, Type
import unittest


def project(
    test: Type[unittest.TestCase],
    fixtures: Dict[str, Any],
    path: str = "project",
    organization: str = "organization",
) -> Any:
    assert issubclass(test, DatabaseTest)
    org = fixtures[organization]
    project = Project(path=path, organization=org)
    test.session.add(project)
    test.session.commit()
    return project


def algorithm(
    test: Type[unittest.TestCase], fixtures: Dict[str, Any], proj: str = "project"
) -> Any:
    assert issubclass(test, DatabaseTest)
    project = fixtures[proj]
    algorithm = Algorithm(project=project)
    test.session.add(algorithm)
    test.session.commit()
    return algorithm


def algorithmschema(test: Type[unittest.TestCase], fixtures: Dict[str, Any]) -> Any:
    assert issubclass(test, DatabaseTest)
    algorithmschema = AlgorithmSchema()
    test.session.add(algorithmschema)
    test.session.commit()
    return algorithmschema


def algorithm_algorithmschema(
    test: Type[unittest.TestCase],
    fixtures: Dict[str, Any],
    algoschema: str = "algorithmschema",
    algorithm: str = "algorithm",
) -> Any:
    assert issubclass(test, DatabaseTest)
    algorithmschema = fixtures[algoschema]
    algo = fixtures[algorithm]
    algo_algorithmschema = AlgorithmAlgorithmSchema(
        algorithmschema=algorithmschema, algorithm=algo
    )
    test.session.add(algo_algorithmschema)
    test.session.commit()
    return algo_algorithmschema
