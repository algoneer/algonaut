import abc

from typing import Iterable

from .access_token import AccessToken
from .organization import Organization


class User(abc.ABC):
    @abc.abstractproperty
    def roles(self) -> "OrganizationRoles":
        pass

    @abc.abstractproperty
    def access_token(self) -> AccessToken:
        pass


class OrganizationRoles(abc.ABC):
    @abc.abstractproperty
    def organization(self) -> Organization:
        pass

    @abc.abstractproperty
    def roles(self) -> Iterable[str]:
        pass
