from algonaut.settings import settings
from algonaut.utils.auth import User, Organization, OrganizationRoles, AccessToken
from ..auth import PlainAuthClient

from typing import Any, Dict, Iterable, Type

import uuid
import unittest


def auth_client(test: Type[unittest.TestCase], fixtures: Dict[str, Any]) -> Any:
    settings.auth_client = PlainAuthClient([])
    return settings.auth_client


def organization(
    test: Type[unittest.TestCase], fixtures: Dict[str, Any], name="ACME"
) -> Any:
    return Organization(name=name, id=uuid.uuid4().bytes)


def user(
    test: Type[unittest.TestCase],
    fixtures: Dict[str, Any],
    email: str = "max@mustermann.de",
    organization: str = "organization",
    roles: Iterable[str] = ["admin"],
) -> Any:
    auth_client = fixtures["auth_client"]
    assert isinstance(auth_client, PlainAuthClient)
    org = fixtures[organization]
    token = AccessToken("test")
    org_roles = OrganizationRoles(org, roles)
    user = User(token, org_roles)
    auth_client.users.append(user)
    return user
