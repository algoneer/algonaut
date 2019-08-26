from algonaut.settings import settings
from algonaut.models import (
    Dataset,
    DatasetVersion,
    DataSchema,
    Datapoint,
    DatasetVersionDatapoint,
    DatasetVersionDataSchema,
)
from ..helpers import DatabaseTest

from typing import Any, Dict, Type
import unittest


def dataset(
    test: Type[unittest.TestCase],
    fixtures: Dict[str, Any],
    path: str,
    organization: str = "organization",
) -> Any:
    assert issubclass(test, DatabaseTest)
    org = fixtures[organization]
    dataset = Dataset(path=path, organization=org)
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


def datasetversion_dataschema(
    test: Type[unittest.TestCase],
    fixtures: Dict[str, Any],
    dsschema: str = "dataschema",
    dsversion: str = "datasetversion",
) -> Any:
    assert issubclass(test, DatabaseTest)
    dataschema = fixtures[dsschema]
    datasetversion = fixtures[dsversion]
    datasetversion_dataschema = DatasetVersionDataSchema(
        dataschema=dataschema, datasetversion=datasetversion
    )
    test.session.add(datasetversion_dataschema)
    test.session.commit()
    return datasetversion_dataschema


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
