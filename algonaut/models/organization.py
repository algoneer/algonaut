from .base import Base
from algonaut.utils.auth import Organization as AuthOrganization

from sqlalchemy import Column, Unicode
from sqlalchemy.dialects.postgresql import BYTEA


class Organization(Base):

    __tablename__ = "organization"

    """
    Describes an organization.
    """
    name = Column(Unicode, nullable=False)
    title = Column(Unicode, nullable=False, default="")
    source = Column(Unicode, nullable=False)
    source_id = Column(BYTEA, nullable=False)
    description = Column(Unicode, nullable=False, default="")

    @classmethod
    def get_or_create(cls, session, auth_org: AuthOrganization) -> "Organization":
        org = (
            session.query(Organization)
            .filter(
                Organization.source == auth_org.source,
                Organization.source_id == auth_org.id,
                Organization.deleted_at == None,
            )
            .one_or_none()
        )
        if org is None:
            org = Organization(
                source=auth_org.source,
                source_id=auth_org.id,
                name=auth_org.name,
                title=auth_org.title,
                description=auth_org.description,
            )
            session.add(org)

        return org

    def export(self):
        d = super().export()
        d.update(
            {
                "title": self.title,
                "name": self.name,
                "source": self.source,
                "source_id": self.source_id.hex(),
                "description": self.description,
            }
        )
        return d
