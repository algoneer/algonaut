from .base import Base
from .hashable import Hashable

from sqlalchemy import Column, Unicode, UniqueConstraint
from sqlalchemy.dialects.postgresql import BYTEA


class Result(Hashable, Base):

    """
    Describes a result.
    """

    __tablename__ = "result"

    __table_args__ = (UniqueConstraint("hash"),)

    hash = Column(BYTEA, nullable=False)
    name = Column(Unicode, nullable=False)

    def export(self):
        d = super().export()
        d.update({"name": self.name, "hash": self.hash.hex()})
        return d
