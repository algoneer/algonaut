from .base import Base, PkType

from sqlalchemy import Column, ForeignKey, Unicode
from sqlalchemy.orm import relationship, backref

import sqlalchemy


class AlgorithmResult(Base):

    __tablename__ = "algorithm_result"

    """
    Describes an algorithm version mapped to a result.
    """

    algorithm_id = Column(PkType, ForeignKey("algorithm.id"), nullable=False)
    name = Column(Unicode, nullable=False, default="")
    version = Column(Unicode, nullable=False, default="")

    algorithm = relationship(
        "Algorithm",
        backref=backref("results", cascade="all,delete,delete-orphan"),
        innerjoin=True,
    )

    def export_fields(self):
        return {"name": self.name, "version": self.version}

    def get_existing(self, session: sqlalchemy.orm.session.Session):
        return (
            session.query(AlgorithmResult)
            .filter(
                AlgorithmResult.algorithm == self.algorithm,
                AlgorithmResult.name == self.name,
                AlgorithmResult.deleted_at == None,
            )
            .one_or_none()
        )
