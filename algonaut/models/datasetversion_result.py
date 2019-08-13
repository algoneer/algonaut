from .base import Base, PkType, ExtPkType

from sqlalchemy import Column, DateTime, Unicode, BigInteger, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref


class DataSetVersionResult(Base):

    __tablename__ = "datasetversion_result"

    """
    Describes a data set version mapped to a result.
    """

    datasetversion_id = Column(
        PkType, ForeignKey("datasetversion.id"), index=True, nullable=False
    )
    result_id = Column(PkType, ForeignKey("result.id"), index=True, nullable=False)

    datasetversion = relationship(
        "DataSetVersion", backref=backref("results", cascade="all,delete,delete-orphan")
    )
    result = relationship(
        "Result", backref=backref("datasets", cascade="all,delete,delete-orphan")
    )
