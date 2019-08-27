from .base import Base
from .hashable import Hashable

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import BYTEA


class AlgorithmSchema(Hashable, Base):

    __tablename__ = "algorithmschema"

    """
    Describes an algorithm schema.
    """

    hash = Column(BYTEA, nullable=False)
