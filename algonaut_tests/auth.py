import flask
from algonaut.utils.auth import (
    AuthClient as BaseAuthClient,
    get_access_token,
    AccessToken,
    User,
    Organization,
    OrganizationRoles,
)

from typing import Dict, Any, Optional, List, Iterable


class PlainOrganization(Organization):
    def __init__(self, name: str, id: bytes) -> None:
        self._name = name
        self._id = id

    @property
    def name(self) -> str:
        return self._name

    @property
    def id(self) -> bytes:
        return self._id


class PlainAccessToken(AccessToken):
    def __init__(self, token: str):
        self._token = token

    @property
    def token(self) -> str:
        return self._token


class PlainUser(User):
    def __init__(
        self, email: str, roles: "PlainOrganizationRoles", token: PlainAccessToken
    ):
        self._email = email
        self._roles = roles
        self._access_token = token

    @property
    def roles(self) -> OrganizationRoles:
        return self._roles

    @property
    def access_token(self) -> AccessToken:
        return self._access_token


class PlainOrganizationRoles(OrganizationRoles):
    def __init__(self, organization: PlainOrganization, roles: Iterable[str]) -> None:
        self._organization = organization
        self._roles = roles

    @property
    def organization(self):
        return self._organization

    @property
    def roles(self):
        return self._roles


class PlainAuthClient(BaseAuthClient):

    """
    This is an auth client that contains a predefined list of users by access
    token for testing purposes.
    """

    def __init__(self, users: List[User]) -> None:
        self.users: List[User] = users

    def get_user(self, request: flask.Request) -> Optional[User]:
        access_token = get_access_token(request)
        if not access_token:
            return None
        for user in self.users:
            if user.access_token.token == access_token:
                return user
        return None
