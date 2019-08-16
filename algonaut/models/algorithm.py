from .base import Base

from sqlalchemy import Column, Unicode
from sqlalchemy.dialects.postgresql import ARRAY


class Algorithm(Base):

    __tablename__ = "algorithm"

    """
    Describes an algorithm.
    """
    path = Column(Unicode, nullable=False)
    description = Column(Unicode, nullable=False, default="")
    tags = Column(ARRAY(Unicode, dimensions=1))
