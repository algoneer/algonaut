from .base import Base, PkType, ExtPkType

from sqlalchemy import Column, DateTime, Unicode, BigInteger, Integer
from sqlalchemy.dialects.postgresql import ARRAY


class DataSet(Base):

    __tablename__ = "dataset"

    """
    Describes a data set.
    """

    name = Column(Unicode, nullable=False)
    description = Column(Unicode, nullable=False, default="")
    tags = Column(ARRAY(Unicode, dimensions=1))
