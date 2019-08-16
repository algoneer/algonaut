from .base import Base, PkType, ExtPkType

from sqlalchemy import Column, DateTime, Unicode, BigInteger, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref


class Model(Base):

    __tablename__ = "model"

    """
    Describes a model.
    """

    algorithmversion_id = Column(
        PkType, ForeignKey("algorithmversion.id"), nullable=False
    )
    datasetversion_id = Column(PkType, ForeignKey("datasetversion.id"), nullable=False)

    algorithmversion = relationship(
        "AlgorithmVersion",
        backref=backref("models", cascade="all,delete,delete-orphan"),
    )
    datasetversion = relationship(
        "DataSetVersion", backref=backref("models", cascade="all,delete,delete-orphan")
    )
