from algonaut.utils.settings import Settings as BaseSettings, load_settings
from algonaut.utils.auth import auth_clients
from algonaut.utils.auth import AuthClient
import os

from typing import List, Optional

settings_filenames: List[str] = []

# finally we load custom settings...
_algonaut_settings_d = os.environ.get("ALGONAUT_SETTINGS_D", "").split(":")
if _algonaut_settings_d:
    for s in _algonaut_settings_d:
        settings_directory = os.path.abspath(s)
        if not os.path.exists(settings_directory):
            continue
        settings_filenames += [
            os.path.join(settings_directory, fn)
            for fn in sorted(os.listdir(settings_directory))
            if fn.endswith(".yml") and not fn.startswith(".")
        ]


class Settings(BaseSettings):
    def __init__(self, d):
        super().__init__(d)
        self._auth_client: Optional[AuthClient] = None

    def _get_auth_client(self):
        client_type = settings.get("auth.type")
        client_config = settings.get("auth.config")
        ClientClass = auth_clients[client_type]
        self._auth_client = ClientClass(client_config)

    @property
    def auth_client(self):
        if self._auth_client is None:
            self._get_auth_client()
        return self._auth_client

    @auth_client.setter
    def auth_client(self, client: AuthClient):
        self._auth_client = client


settings = Settings(load_settings(settings_filenames))
