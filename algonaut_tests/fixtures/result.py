from algonaut.models import (
    Result,
    ModelResult,
    DatapointModelResult,
    DatasetVersionResult,
    AlgorithmResult,
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


def datapoint_model_result(
    test: Type[unittest.TestCase],
    fixtures: Dict[str, Any],
    model: str = "model",
    datapoint: str = "datapoint",
    result: str = "result",
) -> Any:
    assert issubclass(test, DatabaseTest)
    md = fixtures[model]
    rs = fixtures[result]
    dp = fixtures[datapoint]
    datapoint_model_result = DatapointModelResult(datapoint=dp, model=md, result=rs)
    test.session.add(datapoint_model_result)
    test.session.commit()
    return datapoint_model_result


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


def algorithm_result(
    test: Type[unittest.TestCase],
    fixtures: Dict[str, Any],
    algorithm: str = "algorithm",
    result: str = "result",
) -> Any:
    assert issubclass(test, DatabaseTest)
    algo = fixtures[algorithm]
    rs = fixtures[result]
    algorithm_result = AlgorithmResult(algorithm=algo, result=rs)
    test.session.add(algorithm_result)
    test.session.commit()
    return algorithm_result
