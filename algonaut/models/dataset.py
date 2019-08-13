from .base import Base, PkType, ExtPkType

from sqlalchemy import Column, DateTime, Unicode, BigInteger, Integer
from sqlalchemy.dialects.postgresql import ARRAY


class DataSet(Base):

    __tablename__ = "dataset"

    """
    Describes a data set.
    """

    name = Column(Unicode, index=True, nullable=False)
    description = Column(Unicode, index=True, nullable=False)
    tags = Column(ARRAY(Unicode, dimensions=1))
