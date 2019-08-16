from .. import User as BaseUser, OrganizationRoles as BaseOrganizationRoles
from .access_token import AccessToken


class OrganizationRoles(BaseOrganizationRoles):
    def __init__(self):
        pass


class User(BaseUser):
    def __init__(self, d, access_token: AccessToken):
        self.d = d
        self._access_token = access_token

    @property
    def access_token(self):
        return self._access_token

    @property
    def roles(self) -> BaseOrganizationRoles:
        return self.d.get("roles", [])
