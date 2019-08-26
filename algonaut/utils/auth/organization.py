from typing import Iterable, Optional


class Organization:
    def __init__(
        self,
        name: str,
        source: str,
        id: bytes,
        description: str = "",
        title: Optional[str] = None,
    ) -> None:
        self._name = name
        self._source = source
        self._id = id
        if title is None:
            title = name
        self._title = title
        self._description = description

    @property
    def name(self) -> str:
        return self._name

    @property
    def id(self) -> bytes:
        return self._id

    @property
    def source(self) -> str:
        return self._source

    @property
    def description(self) -> str:
        return self._description

    @property
    def title(self) -> str:
        return self._title
