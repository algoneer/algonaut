from .base import Base, PkType

from sqlalchemy import Column, ForeignKey, Unicode
from sqlalchemy.orm import relationship, backref

import sqlalchemy


class ModelResult(Base):

    __tablename__ = "model_result"

    """
    Describes a model result.
    """

    model_id = Column(PkType, ForeignKey("model.id"), nullable=False)
    name = Column(Unicode, nullable=False, default="")
    version = Column(Unicode, nullable=False, default="")

    model = relationship(
        "Model",
        backref=backref("results", cascade="all,delete,delete-orphan"),
        innerjoin=True,
    )

    def export_fields(self):
        return {"name": self.name, "version": self.version}

    def get_existing(self, session: sqlalchemy.orm.session.Session):
        return (
            session.query(ModelResult)
            .filter(
                ModelResult.model == self.model,
                ModelResult.name == self.name,
                ModelResult.deleted_at == None,
            )
            .one_or_none()
        )
