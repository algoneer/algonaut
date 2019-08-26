from .base import Base, PkType

from sqlalchemy import Column, Unicode, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import ARRAY


class Algorithm(Base):

    __tablename__ = "algorithm"

    """
    Describes an algorithm.
    """
    path = Column(Unicode, nullable=False)
    name = Column(Unicode, nullable=False, default="")
    description = Column(Unicode, nullable=False, default="")
    tags = Column(ARRAY(Unicode, dimensions=1))
    organization_id = Column(PkType, ForeignKey("organization.id"), nullable=False)
    organization = relationship(
        "Organization",
        backref=backref("algorithms", cascade="all,delete,delete-orphan"),
        innerjoin=True,
    )

    def export(self):
        d = super().export()
        d.update(
            {
                "path": self.path,
                "description": self.description,
                "tags": [tag for tag in self.tags] if self.tags else None,
                "organization": self.organization.export(),
            }
        )
        return d
