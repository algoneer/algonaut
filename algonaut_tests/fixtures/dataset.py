from algonaut.settings import settings
from algonaut.models import (
    Dataset,
    DataSchema,
    Datapoint,
    DatasetDatapoint,
    DatasetDataSchema,
)
from ..helpers import DatabaseTest

from typing import Any, Dict, Type
import unittest


def dataset(
    test: Type[unittest.TestCase],
    fixtures: Dict[str, Any],
    name: str = "dataset",
    project: str = "project",
) -> Any:
    assert issubclass(test, DatabaseTest)
    proj = fixtures[project]
    dataset = Dataset(name=name, project=proj)
    test.session.add(dataset)
    test.session.commit()
    return dataset


def dataschema(test: Type[unittest.TestCase], fixtures: Dict[str, Any]) -> Any:
    assert issubclass(test, DatabaseTest)
    dataschema = DataSchema()
    test.session.add(dataschema)
    test.session.commit()
    return dataschema


def dataset_dataschema(
    test: Type[unittest.TestCase],
    fixtures: Dict[str, Any],
    datasetschema: str = "dataschema",
    dataset: str = "dataset",
) -> Any:
    assert issubclass(test, DatabaseTest)
    dschema = fixtures[datasetschema]
    ds = fixtures[dataset]
    dataset_dataschema = DatasetDataSchema(dataschema=dschema, dataset=ds)
    test.session.add(dataset_dataschema)
    test.session.commit()
    return dataset_dataschema


def datapoint(test: Type[unittest.TestCase], fixtures: Dict[str, Any]) -> Any:
    assert issubclass(test, DatabaseTest)
    datapoint = Datapoint()
    test.session.add(datapoint)
    test.session.commit()
    return datapoint


def dataset_datapoint(
    test: Type[unittest.TestCase],
    fixtures: Dict[str, Any],
    dataset: str = "dataset",
    datapoint: str = "datapoint",
) -> Any:
    assert issubclass(test, DatabaseTest)
    dp = fixtures[datapoint]
    ds = fixtures[dataset]
    dataset_datapoint = DatasetDatapoint(datapoint=dp, dataset=ds)
    test.session.add(dataset_datapoint)
    test.session.commit()
    return dataset_datapoint
