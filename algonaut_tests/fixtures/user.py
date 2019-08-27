from algonaut.settings import settings
from algonaut.utils.auth import (
    User,
    Organization as AuthOrganization,
    OrganizationRoles,
    AccessToken,
)
from algonaut.models import Organization
from ..auth import PlainAuthClient
from algonaut_tests.helpers import DatabaseTest

from typing import Any, Dict, List, Type

import uuid
import unittest


def auth_client(test: Type[unittest.TestCase], fixtures: Dict[str, Any]) -> Any:
    settings.auth_client = PlainAuthClient([])
    return settings.auth_client


def organization(
    test: Type[unittest.TestCase], fixtures: Dict[str, Any], name="ACME"
) -> Any:
    assert issubclass(test, DatabaseTest)
    org = Organization(name=name, source="test", source_id=uuid.uuid4().bytes)
    test.session.add(org)
    test.session.commit()
    return org


def user(
    test: Type[unittest.TestCase],
    fixtures: Dict[str, Any],
    email: str = "max@mustermann.de",
    organization: str = "organization",
    roles: List[str] = ["admin"],
) -> Any:
    auth_client = fixtures["auth_client"]
    assert isinstance(auth_client, PlainAuthClient)
    org = fixtures[organization]
    auth_org = AuthOrganization(name=org.name, id=org.source_id, source=org.source)
    token = AccessToken("test")
    org_roles = OrganizationRoles(auth_org, roles)
    user = User(token, [org_roles])
    auth_client.users.append(user)
    return user
