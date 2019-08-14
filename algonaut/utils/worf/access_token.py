from ..access_token import AccessToken as BaseAccessToken

from typing import Dict, Any


class AccessToken(BaseAccessToken):
    def __init__(self, d: Dict[str, Any]):
        self.d = d

    @property
    def token(self):
        return self.d.get("token")
