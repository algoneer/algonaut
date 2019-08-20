from algonaut.models import Result
from ..helpers import DatabaseTest

from typing import Any, Dict, Type
import unittest


def result(test: Type[unittest.TestCase], fixtures: Dict[str, Any], name: str) -> Any:
    assert issubclass(test, DatabaseTest)
    result = Result(name=name)
    test.session.add(result)
    test.session.commit()
    return result
