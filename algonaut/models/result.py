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
