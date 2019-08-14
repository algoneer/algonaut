import requests
import algonaut.settings
from .user import User
from .access_token import AccessToken
import flask

from ..auth_client import AuthClient as BaseAuthClient, get_access_token

from typing import Callable, Optional


class AuthClient(BaseAuthClient):
    def __init__(self, settings: "algonaut.settings.Settings") -> None:
        self.base_url = settings.get("worf.base_url")
        self.version = settings.get("worf.version")

    def _request(
        self, method: Callable, access_token: str, url: str, **kwargs
    ) -> requests.Response:
        if not "headers" in kwargs:
            kwargs["headers"] = {}
        headers = kwargs["headers"]
        headers["Authorization"] = f"bearer {access_token}"
        full_url = f"{self.base_url}/{self.version}/{url}"
        return method(url=full_url, **kwargs)

    def _get(self, access_token: str, url: str, **kwargs) -> requests.Response:
        return self._request(requests.get, url, **kwargs)

    def get_user(self, request: flask.Request) -> Optional[User]:
        token = get_access_token(request)
        if not token:
            return None
        response = self._get(token, "user")
        data = response.json()
        access_token = AccessToken(data["access_token"])
        return User(data["user"], access_token)
