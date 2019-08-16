from .base import Base, PkType

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship, backref


class ModelResult(Base):

    __tablename__ = "model_result"

    """
    Describes a model result.
    """

    model_id = Column(PkType, ForeignKey("model.id"), nullable=False)
    result_id = Column(PkType, ForeignKey("result.id"), nullable=False)

    model = relationship(
        "Model", backref=backref("results", cascade="all,delete,delete-orphan")
    )
    result = relationship(
        "Result", backref=backref("models", cascade="all,delete,delete-orphan")
    )
