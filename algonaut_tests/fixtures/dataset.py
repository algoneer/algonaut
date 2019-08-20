from algonaut.settings import settings
from algonaut.models import (
    Dataset,
    DatasetVersion,
    DataSchema,
    Datapoint,
    DatasetVersionDatapoint,
    DatasetVersionDataSchema,
)
from ..auth import PlainAuthClient, PlainUser, PlainAccessToken
from ..helpers import DatabaseTest

from typing import Any, Dict, Type
import unittest


def dataset(test: Type[unittest.TestCase], fixtures: Dict[str, Any], path: str) -> Any:
    assert issubclass(test, DatabaseTest)
    dataset = Dataset(path=path)
    test.session.add(dataset)
    test.session.commit()
    return dataset


def datasetversion(
    test: Type[unittest.TestCase], fixtures: Dict[str, Any], algo: str = "dataset"
) -> Any:
    assert issubclass(test, DatabaseTest)
    dataset = fixtures[algo]
    datasetversion = DatasetVersion(dataset=dataset, hash=b"foo")
    test.session.add(datasetversion)
    test.session.commit()
    return datasetversion


def dataschema(test: Type[unittest.TestCase], fixtures: Dict[str, Any]) -> Any:
    assert issubclass(test, DatabaseTest)
    dataschema = DataSchema(hash=b"foo")
    test.session.add(dataschema)
    test.session.commit()
    return dataschema


def datapoint(test: Type[unittest.TestCase], fixtures: Dict[str, Any]) -> Any:
    assert issubclass(test, DatabaseTest)
    datapoint = Datapoint(hash=b"foo")
    test.session.add(datapoint)
    test.session.commit()
    return datapoint


def datasetversion_datapoint(
    test: Type[unittest.TestCase],
    fixtures: Dict[str, Any],
    datasetversion: str = "datasetversion",
    datapoint: str = "datapoint",
) -> Any:
    assert issubclass(test, DatabaseTest)
    dp = fixtures[datapoint]
    dsv = fixtures[datasetversion]
    datasetversion_datapoint = DatasetVersionDatapoint(datapoint=dp, datasetversion=dsv)
    test.session.add(datasetversion_datapoint)
    test.session.commit()
    return datasetversion_datapoint
