class AccessToken:
    def __init__(self, token: str) -> None:
        self._token = token

    @property
    def token(self) -> str:
        return self._token
