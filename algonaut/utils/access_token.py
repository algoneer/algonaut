import abc


class AccessToken(abc.ABC):
    @abc.abstractproperty
    def token(self) -> str:
        pass
