from .base import Base, PkType

from sqlalchemy import Column, Unicode, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import ARRAY


class Dataset(Base):

    __tablename__ = "dataset"

    """
    Describes a data set.
    """

    path = Column(Unicode, nullable=False)
    description = Column(Unicode, nullable=False, default="")
    tags = Column(ARRAY(Unicode, dimensions=1))
    organization_id = Column(PkType, ForeignKey("organization.id"), nullable=False)
    organization = relationship(
        "Organization",
        backref=backref("datasets", cascade="all,delete,delete-orphan"),
        innerjoin=True,
    )

    def export(self):
        d = super().export()
        d.update(
            {
                "path": self.path,
                "description": self.description,
                "tags": [tag for tag in self.tags] if self.tags else None,
            }
        )
        return d
