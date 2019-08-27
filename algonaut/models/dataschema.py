from .base import Base
from .hashable import Hashable

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import BYTEA


class DataSchema(Hashable, Base):

    __tablename__ = "dataschema"

    """
    Describes a data schema.
    """

    hash = Column(BYTEA, nullable=False)
