from algonaut.models import (
    Result,
    ModelResult,
    DatasetVersionResult,
    AlgorithmVersionResult,
)
from ..helpers import DatabaseTest

from typing import Any, Dict, Type
import unittest


def result(test: Type[unittest.TestCase], fixtures: Dict[str, Any], name: str) -> Any:
    assert issubclass(test, DatabaseTest)
    result = Result(name=name)
    test.session.add(result)
    test.session.commit()
    return result


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


def datasetversion_result(
    test: Type[unittest.TestCase],
    fixtures: Dict[str, Any],
    datasetversion: str = "datasetversion",
    result: str = "result",
) -> Any:
    assert issubclass(test, DatabaseTest)
    dsv = fixtures[datasetversion]
    rs = fixtures[result]
    datasetversion_result = DatasetVersionResult(datasetversion=dsv, result=rs)
    test.session.add(datasetversion_result)
    test.session.commit()
    return datasetversion_result


def algorithmversion_result(
    test: Type[unittest.TestCase],
    fixtures: Dict[str, Any],
    algorithmversion: str = "algorithmversion",
    result: str = "result",
) -> Any:
    assert issubclass(test, DatabaseTest)
    av = fixtures[algorithmversion]
    rs = fixtures[result]
    algorithmversion_result = AlgorithmVersionResult(algorithmversion=av, result=rs)
    test.session.add(algorithmversion_result)
    test.session.commit()
    return algorithmversion_result
