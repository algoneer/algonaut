from .base import Base, PkType

from sqlalchemy import Column, ForeignKey, Unicode
from sqlalchemy.orm import relationship, backref

import sqlalchemy


class DatasetResult(Base):

    __tablename__ = "dataset_result"

    """
    Describes a data set version mapped to a result.
    """

    dataset_id = Column(PkType, ForeignKey("dataset.id"), nullable=False)
    name = Column(Unicode, nullable=False, default="")
    version = Column(Unicode, nullable=False, default="")

    dataset = relationship(
        "Dataset",
        backref=backref("results", cascade="all,delete,delete-orphan"),
        innerjoin=True,
    )

    def export_fields(self):
        return {"name": self.name, "version": self.version}

    def get_existing(self, session: sqlalchemy.orm.session.Session):
        return (
            session.query(DatasetResult)
            .filter(
                DatasetResult.dataset == self.dataset,
                DatasetResult.name == self.name,
                DatasetResult.deleted_at == None,
            )
            .one_or_none()
        )
