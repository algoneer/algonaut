from .base import Base, PkType, ExtPkType

from sqlalchemy import Column, DateTime, Unicode, BigInteger, Integer
from sqlalchemy.dialects.postgresql import ARRAY


class Algorithm(Base):

    __tablename__ = "algorithm"

    """
    Describes an algorithm.
    """

    name = Column(Unicode, index=True, nullable=False)
    description = Column(Unicode, index=True, nullable=False)
    tags = Column(ARRAY(Unicode, dimensions=1))
