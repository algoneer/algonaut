from typing import Iterable


class Organization:
    def __init__(self, name: str, id: bytes) -> None:
        self._name = name
        self._id = id

    @property
    def name(self) -> str:
        return self._name

    @property
    def id(self) -> bytes:
        return self._id
