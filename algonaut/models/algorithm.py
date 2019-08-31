from .base import Base, PkType
from .hashable import Hashable

from sqlalchemy import Column, ForeignKey, Unicode
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.dialects.postgresql import ARRAY


class Algorithm(Hashable, Base):

    __tablename__ = "algorithm"

    """
    Describes an algorithm version.
    """

    project_id = Column(PkType, ForeignKey("project.id"), nullable=False)
    name = Column(Unicode, nullable=False, default="")
    hash = Column(BYTEA, nullable=False)
    project = relationship(
        "Project",
        backref=backref("algorithms", cascade="all,delete,delete-orphan"),
        innerjoin=True,
    )
    tags = Column(ARRAY(Unicode, dimensions=1))

    def export_fields(self):
        return {
            "name": self.name,
            "hash": self.hash,
            "tags": [tag for tag in self.tags] if self.tags else None,
            "project": self.project.export(),
        }
