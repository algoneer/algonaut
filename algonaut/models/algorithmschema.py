from .base import Base, PkType, ExtPkType

from sqlalchemy import Column, DateTime, Unicode, BigInteger, Integer
from sqlalchemy.dialects.postgresql import BYTEA


class AlgorithmSchema(Base):

    __tablename__ = "algorithmschema"

    """
    Describes an algorithm schema.
    """

    hash = Column(BYTEA, nullable=False)
