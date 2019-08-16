import flask
from algonaut.utils.auth_client import AuthClient as BaseAuthClient, get_access_token
from algonaut.utils.user import User
from algonaut.utils.access_token import AccessToken

from typing import Dict, Any, Optional, List


class PlainAccessToken(AccessToken):
    def __init__(self, d: Dict[str, Any]):
        self.d = d

    @property
    def token(self):
        return self.d.get("token")


class PlainUser(User):
    def __init__(self, d: Dict[str, Any], token: PlainAccessToken):
        self.d = d
        self._access_token = token

    @property
    def access_token(self) -> AccessToken:
        return self._access_token

    @property
    def roles(self) -> List[str]:
        return self.d["roles"]


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
