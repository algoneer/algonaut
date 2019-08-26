from .base import Base, PkType

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship, backref


class AlgorithmAlgorithmSchema(Base):

    __tablename__ = "algorithm_algorithmschema"

    """
    Describes an algorithm version mapped to an algorithm schema.
    """

    algorithm_id = Column(PkType, ForeignKey("algorithm.id"), nullable=False)
    algorithmschema_id = Column(
        PkType, ForeignKey("algorithmschema.id"), nullable=False
    )

    algorithm = relationship(
        "Algorithm",
        backref=backref("schemas", cascade="all,delete,delete-orphan"),
        innerjoin=True,
    )
    algorithmschema = relationship(
        "AlgorithmSchema",
        backref=backref("versions", cascade="all,delete,delete-orphan"),
        innerjoin=True,
    )
