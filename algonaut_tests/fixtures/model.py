from algonaut.settings import settings
from algonaut.models import Model
from ..helpers import DatabaseTest

from typing import Any, Dict, Type
import unittest


def model(
    test: Type[unittest.TestCase],
    fixtures: Dict[str, Any],
    algorithmversion: str = "algorithmversion",
    datasetversion: str = "datasetversion",
) -> Any:
    assert issubclass(test, DatabaseTest)
    algoversion = fixtures[algorithmversion]
    dsversion = fixtures[datasetversion]
    model = Model(algorithmversion=algoversion, datasetversion=dsversion)
    test.session.add(model)
    test.session.commit()
    return model
