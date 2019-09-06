from .base import Base, PkType
from .hashable import Hashable

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import BYTEA


class Model(Hashable, Base):

    __tablename__ = "model"

    """
    Describes a model.
    """

    hash = Column(BYTEA, nullable=False)

    algorithm_id = Column(PkType, ForeignKey("algorithm.id"), nullable=False)
    dataset_id = Column(PkType, ForeignKey("dataset.id"), nullable=False)

    algorithm = relationship(
        "Algorithm",
        backref=backref("models", cascade="all,delete,delete-orphan"),
        innerjoin=True,
    )
    dataset = relationship(
        "Dataset",
        backref=backref("models", cascade="all,delete,delete-orphan"),
        innerjoin=True,
    )


    def export_fields(self):
        return {
            "hash": self.hash,
            "algorithm": self.algorithm.export(),
            "dataset": self.dataset.export(),
        }
