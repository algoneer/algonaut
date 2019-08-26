from algonaut.models import (
    Result,
    ModelResult,
    DatapointModelResult,
    DatasetResult,
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


def dataset_result(
    test: Type[unittest.TestCase],
    fixtures: Dict[str, Any],
    dataset: str = "dataset",
    result: str = "result",
) -> Any:
    assert issubclass(test, DatabaseTest)
    ds = fixtures[dataset]
    rs = fixtures[result]
    dataset_result = DatasetResult(dataset=ds, result=rs)
    test.session.add(dataset_result)
    test.session.commit()
    return dataset_result


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
