import flask
from algonaut.utils.auth import (
    AuthClient as BaseAuthClient,
    get_access_token,
    AccessToken,
    User,
    Organization,
    OrganizationRoles,
)

from typing import Optional, List


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
