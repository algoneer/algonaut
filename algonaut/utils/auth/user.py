from typing import List

from .access_token import AccessToken
from .organization import Organization


class OrganizationRoles:
    def __init__(self, organization: Organization, roles: List[str]):
        self._organization = organization
        self._roles = roles

    @property
    def organization(self) -> Organization:
        return self._organization

    @property
    def roles(self) -> List[str]:
        return self._roles

    def export(self):
        return {"roles": self.roles, "organization": self.organization.export()}


class User:
    def __init__(
        self, access_token: AccessToken, organization_roles: List[OrganizationRoles]
    ) -> None:
        self._access_token = access_token
        self._organization_roles = organization_roles

    @property
    def roles(self) -> List[OrganizationRoles]:
        return self._organization_roles

    @property
    def access_token(self) -> AccessToken:
        return self._access_token
