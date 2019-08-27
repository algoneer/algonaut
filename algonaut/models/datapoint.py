from .base import Base
from .hashable import Hashable
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import BYTEA


class Datapoint(Hashable, Base):

    __tablename__ = "datapoint"

    """
    Describes a datapoint.
    """

    hash = Column(BYTEA, nullable=False)
