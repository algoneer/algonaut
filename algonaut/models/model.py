from .base import Base, PkType

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import BYTEA


class Model(Base):

    __tablename__ = "model"

    """
    Describes a model.
    """

    hash = Column(BYTEA, nullable=False)

    algorithmversion_id = Column(
        PkType, ForeignKey("algorithmversion.id"), nullable=False
    )
    datasetversion_id = Column(PkType, ForeignKey("datasetversion.id"), nullable=False)

    algorithmversion = relationship(
        "AlgorithmVersion",
        backref=backref("models", cascade="all,delete,delete-orphan"),
    )
    datasetversion = relationship(
        "DatasetVersion", backref=backref("models", cascade="all,delete,delete-orphan")
    )
