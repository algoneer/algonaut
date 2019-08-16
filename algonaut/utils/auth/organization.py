import abc

from typing import Iterable


class Organization(abc.ABC):
    @abc.abstractproperty
    def name(self) -> str:
        pass

    @abc.abstractproperty
    def id(self) -> bytes:
        pass
