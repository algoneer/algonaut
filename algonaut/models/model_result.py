from .base import Base, PkType, ExtPkType

from sqlalchemy import Column, DateTime, Unicode, BigInteger, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref


class ModelResult(Base):

    __tablename__ = "model_result"

    """
    Describes a model result.
    """

    model_id = Column(PkType, ForeignKey("model.id"), index=True, nullable=False)
    result_id = Column(PkType, ForeignKey("result.id"), index=True, nullable=False)

    model = relationship(
        "Model", backref=backref("results", cascade="all,delete,delete-orphan")
    )
    result = relationship(
        "Result", backref=backref("models", cascade="all,delete,delete-orphan")
    )
