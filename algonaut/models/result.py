from .base import Base

from sqlalchemy import Column, Unicode
from sqlalchemy.dialects.postgresql import BYTEA


class Result(Base):

    __tablename__ = "result"

    """
    Describes a result.
    """

    hash = Column(BYTEA, nullable=False)
    name = Column(Unicode, nullable=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.hash is None:
            self.hash = b"foo"

    def export(self):
        d = super().export()
        d.update({"name": self.name, "hash": self.hash.hex()})
        return d
