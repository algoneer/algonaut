from .base import Base, PkType

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship, backref


class AlgorithmVersionResult(Base):

    __tablename__ = "algorithmversion_result"

    """
    Describes an algorithm version mapped to a result.
    """

    algorithmversion_id = Column(
        PkType, ForeignKey("algorithmversion.id"), nullable=False
    )
    result_id = Column(PkType, ForeignKey("result.id"), nullable=False)

    algorithmversion = relationship(
        "AlgorithmVersion",
        backref=backref("results", cascade="all,delete,delete-orphan"),
    )
    result = relationship(
        "Result", backref=backref("algorithms", cascade="all,delete,delete-orphan")
    )
