from .base import Base, PkType

from sqlalchemy import Column, ForeignKey, Unicode
from sqlalchemy.orm import relationship, backref

import sqlalchemy


class DatasetModelResult(Base):

    __tablename__ = "dataset_model_result"

    """
    Describes a result tied to a dataset and a given model.
    """

    model_id = Column(PkType, ForeignKey("model.id"), nullable=False)
    dataset_id = Column(PkType, ForeignKey("dataset.id"), nullable=False)
    name = Column(Unicode, nullable=False, default="")
    version = Column(Unicode, nullable=False, default="")

    model = relationship(
        "Model",
        backref=backref("dataset_results", cascade="all,delete,delete-orphan"),
        innerjoin=True,
    )
    dataset = relationship(
        "Dataset",
        backref=backref("model_results", cascade="all,delete,delete-orphan"),
        innerjoin=True,
    )

    def export_fields(self):
        return {"name": self.name, "version": self.version}

    def get_existing(self, session: sqlalchemy.orm.session.Session):
        return (
            session.query(DatasetModelResult)
            .filter(
                DatasetModelResult.dataset == self.dataset,
                DatasetModelResult.model == self.model,
                DatasetModelResult.name == self.name,
                DatasetModelResult.deleted_at == None,
            )
            .one_or_none()
        )
