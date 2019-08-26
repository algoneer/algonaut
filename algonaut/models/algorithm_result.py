from .base import Base, PkType

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship, backref


class AlgorithmResult(Base):

    __tablename__ = "algorithm_result"

    """
    Describes an algorithm version mapped to a result.
    """

    algorithm_id = Column(PkType, ForeignKey("algorithm.id"), nullable=False)
    result_id = Column(PkType, ForeignKey("result.id"), nullable=False)

    algorithm = relationship(
        "Algorithm",
        backref=backref("results", cascade="all,delete,delete-orphan"),
        innerjoin=True,
    )
    result = relationship(
        "Result",
        backref=backref("algorithms", cascade="all,delete,delete-orphan"),
        innerjoin=True,
    )
