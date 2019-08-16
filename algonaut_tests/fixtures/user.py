from algonaut.settings import settings
from ..auth import (
    PlainAuthClient,
    PlainUser,
    PlainAccessToken,
    PlainOrganization,
    PlainOrganizationRoles,
)

from typing import Any, Dict, Iterable, Type

import uuid
import unittest


def auth_client(test: Type[unittest.TestCase], fixtures: Dict[str, Any]) -> Any:
    settings.auth_client = PlainAuthClient([])
    return settings.auth_client


def organization(
    test: Type[unittest.TestCase], fixtures: Dict[str, Any], name="ACME"
) -> Any:
    return PlainOrganization(name=name, id=uuid.uuid4().bytes)


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
    token = PlainAccessToken("test")
    org_roles = PlainOrganizationRoles(org, roles)
    user = PlainUser(email, org_roles, token)
    auth_client.users.append(user)
    return user
