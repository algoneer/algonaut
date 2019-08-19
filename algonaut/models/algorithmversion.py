from .base import Base, PkType

from sqlalchemy import Column, ForeignKey, Unicode
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.dialects.postgresql import ARRAY


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
    tags = Column(ARRAY(Unicode, dimensions=1))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.hash is None:
            self.hash = b"foo"
