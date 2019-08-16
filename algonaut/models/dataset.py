from .base import Base

from sqlalchemy import Column, Unicode
from sqlalchemy.dialects.postgresql import ARRAY


class DataSet(Base):

    __tablename__ = "dataset"

    """
    Describes a data set.
    """

    name = Column(Unicode, nullable=False)
    description = Column(Unicode, nullable=False, default="")
    tags = Column(ARRAY(Unicode, dimensions=1))
