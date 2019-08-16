from .base import Base, PkType, ExtPkType

from sqlalchemy import Column, DateTime, Unicode, BigInteger, Integer
from sqlalchemy.dialects.postgresql import BYTEA


class DataSchema(Base):

    __tablename__ = "dataschema"

    """
    Describes a data schema.
    """

    hash = Column(BYTEA, nullable=False)
