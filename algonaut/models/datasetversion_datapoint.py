from .base import Base, PkType

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship, backref


class DatasetVersionDatapoint(Base):

    __tablename__ = "datasetversion_datapoint"

    """
    Describes a data set version mapped to a data point.
    """

    datasetversion_id = Column(PkType, ForeignKey("datasetversion.id"), nullable=False)
    datapoint_id = Column(PkType, ForeignKey("datapoint.id"), nullable=False)

    datasetversion = relationship(
        "DatasetVersion",
        backref=backref("datapoints", cascade="all,delete,delete-orphan"),
        innerjoin=True,
    )
    datapoint = relationship(
        "Datapoint",
        backref=backref("datasets", cascade="all,delete,delete-orphan"),
        innerjoin=True,
    )
