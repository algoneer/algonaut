import abc

from typing import Iterable

from .access_token import AccessToken


class User(abc.ABC):
    @abc.abstractproperty
    def roles(self) -> Iterable[str]:
        pass

    @abc.abstractproperty
    def access_token(self) -> AccessToken:
        pass
