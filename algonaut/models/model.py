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

    algorithm_id = Column(PkType, ForeignKey("algorithm.id"), nullable=False)
    datasetversion_id = Column(PkType, ForeignKey("datasetversion.id"), nullable=False)

    algorithm = relationship(
        "Algorithm",
        backref=backref("models", cascade="all,delete,delete-orphan"),
        innerjoin=True,
    )
    datasetversion = relationship(
        "DatasetVersion",
        backref=backref("models", cascade="all,delete,delete-orphan"),
        innerjoin=True,
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.hash is None:
            self.hash = b"foo"
