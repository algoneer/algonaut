from .base import Base, PkType

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship, backref


class DatasetModelResult(Base):

    __tablename__ = "dataset_model_result"

    """
    Describes a result tied to a dataset and a given model.
    """

    model_id = Column(PkType, ForeignKey("model.id"), nullable=False)
    dataset_id = Column(PkType, ForeignKey("dataset.id"), nullable=False)
    result_id = Column(PkType, ForeignKey("result.id"), nullable=False)

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
    result = relationship(
        "Result",
        backref=backref("dataset_models", cascade="all,delete,delete-orphan"),
        innerjoin=True,
    )
