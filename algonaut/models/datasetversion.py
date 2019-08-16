from .base import Base, PkType, ExtPkType

from sqlalchemy import Column, DateTime, Unicode, BigInteger, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.dialects.postgresql import ARRAY


class DataSetVersion(Base):

    __tablename__ = "datasetversion"

    """
    Describes a data set version.
    """

    dataset_id = Column(PkType, ForeignKey("dataset.id"), nullable=False)
    hash = Column(BYTEA, nullable=False)
    dataset = relationship(
        "DataSet", backref=backref("versions", cascade="all,delete,delete-orphan")
    )
    tags = Column(ARRAY(Unicode, dimensions=1))
