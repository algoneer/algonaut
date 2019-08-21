from typing import Iterable

from .access_token import AccessToken
from .organization import Organization


class OrganizationRoles:
    def __init__(self, organization: Organization, roles: Iterable[str]):
        self._organization = organization
        self._roles = roles

    @property
    def organization(self) -> Organization:
        return self._organization

    @property
    def roles(self) -> Iterable[str]:
        return self._roles


class User:
    def __init__(
        self, access_token: AccessToken, organization_roles: OrganizationRoles
    ) -> None:
        self._access_token = access_token
        self._organization_roles = organization_roles

    @property
    def roles(self) -> OrganizationRoles:
        return self._organization_roles

    @property
    def access_token(self) -> AccessToken:
        return self._access_token
