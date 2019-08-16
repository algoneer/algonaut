from .base import Base

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import BYTEA


class DataSchema(Base):

    __tablename__ = "dataschema"

    """
    Describes a data schema.
    """

    hash = Column(BYTEA, nullable=False)
