from .base import Base, PkType, ExtPkType

from sqlalchemy import Column, DateTime, Unicode, BigInteger, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref


class DataSetVersionDataPoint(Base):

    __tablename__ = "datasetversion_datapoint"

    """
    Describes a data set version mapped to a data point.
    """

    datasetversion_id = Column(
        PkType, ForeignKey("datasetversion.id"), index=True, nullable=False
    )
    datapoint_id = Column(
        PkType, ForeignKey("datapoint.id"), index=True, nullable=False
    )

    datasetversion = relationship(
        "DataSetVersion",
        backref=backref("datapoints", cascade="all,delete,delete-orphan"),
    )
    datapoint = relationship(
        "DataPoint", backref=backref("datasets", cascade="all,delete,delete-orphan")
    )
