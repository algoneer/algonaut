from .base import Base, PkType
from .hashable import Hashable

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import BYTEA

import sqlalchemy


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

    def get_existing(self, session: sqlalchemy.orm.session.Session):
        return (
            session.query(Model)
            .filter(
                Model.hash == self.hash,
                Model.algorithm == self.algorithm,
                Model.dataset == self.dataset,
                Model.deleted_at == None,
            )
            .one_or_none()
        )

    @classmethod
    def hash_data(cls, data):
        return {"data": data.get("data")}
