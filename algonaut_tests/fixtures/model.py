from algonaut.settings import settings
from algonaut.models import Model
from ..helpers import DatabaseTest

from typing import Any, Dict, Type
import unittest


def model(
    test: Type[unittest.TestCase],
    fixtures: Dict[str, Any],
    algorithm: str = "algorithm",
    dataset: str = "dataset",
) -> Any:
    assert issubclass(test, DatabaseTest)
    algo = fixtures[algorithm]
    ds = fixtures[dataset]
    model = Model(algorithm=algo, dataset=ds)
    test.session.add(model)
    test.session.commit()
    return model
