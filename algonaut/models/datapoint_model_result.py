from .base import Base, PkType

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship, backref


class DatapointModelResult(Base):

    __tablename__ = "datapoint_model_result"

    """
    Describes a result tied to a datapoint and a given model.
    """

    model_id = Column(PkType, ForeignKey("model.id"), nullable=False)
    datapoint_id = Column(PkType, ForeignKey("datapoint.id"), nullable=False)
    result_id = Column(PkType, ForeignKey("result.id"), nullable=False)

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
    result = relationship(
        "Result",
        backref=backref("datapoint_models", cascade="all,delete,delete-orphan"),
        innerjoin=True,
    )
