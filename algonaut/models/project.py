from .base import Base, PkType

from sqlalchemy import Column, Unicode, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import ARRAY


class Project(Base):

    __tablename__ = "project"

    """
    Describes a project.
    """
    path = Column(Unicode, nullable=False)
    name = Column(Unicode, nullable=False, default="")
    description = Column(Unicode, nullable=False, default="")
    tags = Column(ARRAY(Unicode, dimensions=1))
    organization_id = Column(PkType, ForeignKey("organization.id"), nullable=False)
    organization = relationship(
        "Organization",
        backref=backref("projects", cascade="all,delete,delete-orphan"),
        innerjoin=True,
    )

    def unique_check(self, session):
        existing_projects = session.query(Project).filter(
            Project.organization == self.organization,
            Project.path == self.path,
            Project.deleted_at == None,
        )
        if existing_projects.count() > 0:
            return False
        return True

    def export(self):
        d = super().export()
        d.update(
            {
                "path": self.path,
                "name": self.name,
                "description": self.description,
                "tags": [tag for tag in self.tags] if self.tags else None,
                "organization": self.organization.export(),
            }
        )
        return d