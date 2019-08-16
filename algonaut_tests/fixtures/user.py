from algonaut.settings import settings
from ..auth_client import PlainAuthClient, PlainUser, PlainAccessToken

from typing import Any


def auth_client(test, fixtures) -> Any:
    settings.auth_client = PlainAuthClient([])
    return settings.auth_client


def user(test, fixtures, roles=["admin"], email="max@mustermann.de") -> Any:
    auth_client = fixtures["auth_client"]
    assert isinstance(auth_client, PlainAuthClient)
    token = PlainAccessToken({"token": "test"})
    user = PlainUser({"email": email, "access_token": "test", "roles": roles}, token)
    auth_client.users.append(user)
    return user
