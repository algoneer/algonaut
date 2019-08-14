import abc
import re
import flask

from typing import Optional
from .user import User


def get_access_token(request: flask.Request) -> Optional[str]:

    auth = request.headers.get("Authorization")
    if not auth:
        return None
    match = re.match(r"bearer\s+([\d\w]+)$", auth, re.I)
    if not match:
        return None
    return match.group(1)


class AuthClient(abc.ABC):
    @abc.abstractmethod
    def get_user(self, request: flask.Request) -> Optional[User]:
        pass
