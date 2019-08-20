from algonaut.settings import settings
from algonaut.models import Model, ModelResult
from ..auth import PlainAuthClient, PlainUser, PlainAccessToken
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


def model_result(
    test: Type[unittest.TestCase],
    fixtures: Dict[str, Any],
    model: str = "model",
    result: str = "result",
) -> Any:
    assert issubclass(test, DatabaseTest)
    md = fixtures[model]
    rs = fixtures[result]
    model_result = ModelResult(model=md, result=rs)
    test.session.add(model_result)
    test.session.commit()
    return model_result
