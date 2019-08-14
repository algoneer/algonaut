from ..user import User as BaseUser
from .access_token import AccessToken


class User(BaseUser):
    def __init__(self, d, access_token: AccessToken):
        self.d = d
        self._access_token = access_token

    @property
    def access_token(self):
        return self._access_token

    @property
    def roles(self):
        return self.d.get("roles", [])
