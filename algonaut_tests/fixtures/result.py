from algonaut.models import (
    ModelResult,
    DatasetModelResult,
    DatapointModelResult,
    DatasetResult,
    AlgorithmResult,
)
from ..helpers import DatabaseTest

from typing import Any, Dict, Type
import unittest


def datapoint_model_result(
    test: Type[unittest.TestCase],
    fixtures: Dict[str, Any],
    model: str = "model",
    datapoint: str = "datapoint",
    name: str = "result",
    data: Dict[str, Any] = {},
) -> Any:
    assert issubclass(test, DatabaseTest)
    md = fixtures[model]
    dp = fixtures[datapoint]
    datapoint_model_result = DatapointModelResult(
        datapoint=dp, model=md, name=name, data=data
    )
    test.session.add(datapoint_model_result)
    test.session.commit()
    return datapoint_model_result


def dataset_model_result(
    test: Type[unittest.TestCase],
    fixtures: Dict[str, Any],
    model: str = "model",
    dataset: str = "dataset",
    name: str = "result",
    data: Dict[str, Any] = {},
) -> Any:
    assert issubclass(test, DatabaseTest)
    md = fixtures[model]
    ds = fixtures[dataset]
    dataset_model_result = DatasetModelResult(
        dataset=ds, model=md, name=name, data=data
    )
    test.session.add(dataset_model_result)
    test.session.commit()
    return dataset_model_result


def model_result(
    test: Type[unittest.TestCase],
    fixtures: Dict[str, Any],
    model: str = "model",
    name: str = "result",
    data: Dict[str, Any] = {},
) -> Any:
    assert issubclass(test, DatabaseTest)
    md = fixtures[model]
    model_result = ModelResult(model=md, name=name, data=data)
    test.session.add(model_result)
    test.session.commit()
    return model_result


def dataset_result(
    test: Type[unittest.TestCase],
    fixtures: Dict[str, Any],
    dataset: str = "dataset",
    name: str = "result",
    data: Dict[str, Any] = {},
) -> Any:
    assert issubclass(test, DatabaseTest)
    ds = fixtures[dataset]
    dataset_result = DatasetResult(dataset=ds, name=name, data=data)
    test.session.add(dataset_result)
    test.session.commit()
    return dataset_result


def algorithm_result(
    test: Type[unittest.TestCase],
    fixtures: Dict[str, Any],
    algorithm: str = "algorithm",
    name: str = "result",
    data: Dict[str, Any] = {},
) -> Any:
    assert issubclass(test, DatabaseTest)
    algo = fixtures[algorithm]
    algorithm_result = AlgorithmResult(algorithm=algo, name=name, data=data)
    test.session.add(algorithm_result)
    test.session.commit()
    return algorithm_result
