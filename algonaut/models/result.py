from .base import Base
from .hashable import Hashable

from sqlalchemy import Column, Unicode
from sqlalchemy.dialects.postgresql import BYTEA


class Result(Hashable, Base):

    """
    Describes a result.
    """

    __tablename__ = "result"

    hash = Column(BYTEA, nullable=False)
    name = Column(Unicode, nullable=False, default="")
    version = Column(Unicode, nullable=False, default="")

    def export_fields(self):
        return {"name": self.name, "hash": self.hash, "version": self.version}
