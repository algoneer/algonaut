from .base import Base, PkType, ExtPkType

from sqlalchemy import Column, DateTime, Unicode, BigInteger, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import BYTEA


class AlgorithmVersion(Base):

    __tablename__ = "algorithmversion"

    """
    Describes an algorithm version.
    """

    algorithm_id = Column(PkType, ForeignKey("algorithm.id"), nullable=False)
    hash = Column(BYTEA, nullable=False)
    algorithm = relationship(
        "Algorithm", backref=backref("versions", cascade="all,delete,delete-orphan")
    )