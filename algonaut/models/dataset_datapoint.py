from .base import Base, PkType

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship, backref


class DatasetDatapoint(Base):

    __tablename__ = "dataset_datapoint"

    """
    Describes a data set version mapped to a data point.
    """

    dataset_id = Column(PkType, ForeignKey("dataset.id"), nullable=False)
    datapoint_id = Column(PkType, ForeignKey("datapoint.id"), nullable=False)

    dataset = relationship(
        "Dataset",
        backref=backref("datapoints", cascade="all,delete,delete-orphan"),
        innerjoin=True,
    )
    datapoint = relationship(
        "Datapoint",
        backref=backref("datasets", cascade="all,delete,delete-orphan"),
        innerjoin=True,
    )
