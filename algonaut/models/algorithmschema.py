from .base import Base

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import BYTEA


class AlgorithmSchema(Base):

    __tablename__ = "algorithmschema"

    """
    Describes an algorithm schema.
    """

    hash = Column(BYTEA, nullable=False)
