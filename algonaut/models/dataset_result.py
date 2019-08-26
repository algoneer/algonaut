from .base import Base, PkType

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship, backref


class DatasetResult(Base):

    __tablename__ = "dataset_result"

    """
    Describes a data set version mapped to a result.
    """

    dataset_id = Column(PkType, ForeignKey("dataset.id"), nullable=False)
    result_id = Column(PkType, ForeignKey("result.id"), nullable=False)

    dataset = relationship(
        "Dataset",
        backref=backref("results", cascade="all,delete,delete-orphan"),
        innerjoin=True,
    )
    result = relationship(
        "Result",
        backref=backref("datasets", cascade="all,delete,delete-orphan"),
        innerjoin=True,
    )
