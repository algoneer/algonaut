from algonaut.settings import settings
from algonaut.models import Model
from ..helpers import DatabaseTest

from typing import Any, Dict, Type
import unittest


def model(
    test: Type[unittest.TestCase],
    fixtures: Dict[str, Any],
    algorithm: str = "algorithm",
    datasetversion: str = "datasetversion",
) -> Any:
    assert issubclass(test, DatabaseTest)
    algo = fixtures[algorithm]
    dsversion = fixtures[datasetversion]
    model = Model(algorithm=algo, datasetversion=dsversion)
    test.session.add(model)
    test.session.commit()
    return model
