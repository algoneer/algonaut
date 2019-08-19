from algonaut.settings import settings
from algonaut.models import ObjectRole, Base
from algonaut.utils.auth import Organization
from ..helpers import DatabaseTest

import unittest

from typing import Any, Dict, Type


def object_role(
    test: Type[unittest.TestCase],
    fixtures: Dict[str, Any],
    organization_role: str,
    object_role: str,
    organization: str,
    object: str,
) -> Any:
    assert issubclass(test, DatabaseTest)
    org = fixtures[organization]
    obj = fixtures[object]
    assert isinstance(obj, Base)
    assert isinstance(org, Organization)
    object_role = ObjectRole(
        organization_id=org.id,
        object_role=object_role,
        organization_role=organization_role,
        object_id=obj.ext_id,
        object_type=obj.type,
    )
    test.session.add(object_role)
    test.session.commit()
    return object_role
