from .base import Base, PkType

from sqlalchemy import Column, ForeignKey, Unicode
from sqlalchemy.orm import relationship, backref

import sqlalchemy


class DatapointModelResult(Base):

    __tablename__ = "datapoint_model_result"

    """
    Describes a result tied to a datapoint and a given model.
    """

    model_id = Column(PkType, ForeignKey("model.id"), nullable=False)
    datapoint_id = Column(PkType, ForeignKey("datapoint.id"), nullable=False)
    name = Column(Unicode, nullable=False, default="")
    version = Column(Unicode, nullable=False, default="")

    model = relationship(
        "Model",
        backref=backref("datapoint_results", cascade="all,delete,delete-orphan"),
        innerjoin=True,
    )
    datapoint = relationship(
        "Datapoint",
        backref=backref("results", cascade="all,delete,delete-orphan"),
        innerjoin=True,
    )

    def export_fields(self):
        return {"name": self.name, "version": self.version}

    def get_existing(self, session: sqlalchemy.orm.session.Session):
        return (
            session.query(DatapointModelResult)
            .filter(
                DatapointModelResult.datapoint == self.datapoint,
                DatapointModelResult.model == self.model,
                DatapointModelResult.name == self.name,
                DatapointModelResult.deleted_at == None,
            )
            .one_or_none()
        )
