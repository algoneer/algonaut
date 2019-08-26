from .base import Base, PkType
from .organization import Organization

from sqlalchemy import Column, Unicode, ForeignKey
from sqlalchemy.orm import backref, relationship
from algonaut.utils.auth import User
from typing import Iterable, Any, Optional
import sqlalchemy

from enum import Enum


class ObjectRole(Base):

    __tablename__ = "object_role"

    """
    Describes a model.
    """

    class Roles(Enum):
        superuser = "superuser"
        admin = "admin"
        developer = "developer"
        viewer = "viewer"
        auditor = "auditor"

    object_id = Column(PkType, nullable=False)
    object_type = Column(Unicode)
    organization_role = Column(Unicode)
    object_role = Column(Unicode)

    organization_id = Column(PkType, ForeignKey("organization.id"), nullable=False)
    organization = relationship(
        "Organization",
        backref=backref("roles", cascade="all,delete,delete-orphan"),
        innerjoin=True,
    )

    # we unset the data field...
    data = None

    @classmethod
    def get_or_create(
        cls,
        session: sqlalchemy.orm.session.Session,
        object: Base,
        organization: Organization,
        object_role: str,
        organization_role: str,
    ):
        """
        Creates a new role for a given organization and a given object.
        """
        obj_role = (
            session.query(ObjectRole)
            .filter(
                ObjectRole.organization_id == organization.id,
                ObjectRole.object_id == object.id,
                ObjectRole.object_type == object.type,
                ObjectRole.object_role == object_role,
                ObjectRole.organization_role == organization_role,
            )
            .one_or_none()
        )

        if obj_role is None:
            obj_role = ObjectRole(
                organization_id=organization.id,
                object_id=object.id,
                object_type=object.type,
                object_role=object_role,
                organization_role=organization_role,
            )
            session.add(obj_role)

        obj_role.deleted_at = None

        return obj_role

    @classmethod
    def roles_for(
        cls, session: sqlalchemy.orm.session.Session, user: User, object: Base
    ):
        filters = [
            ObjectRole.object_id == object.id,
            ObjectRole.object_type == object.type,
            ObjectRole.deleted_at == None,
        ]
        for org_roles in user.roles:
            filters.extend(
                [
                    ObjectRole.organization_role.in_(org_roles.roles),
                    Organization.source_id == org_roles.organization.id,
                    Organization.source == org_roles.organization.source,
                ]
            )
        return session.query(ObjectRole).join(Organization).filter(*filters).all()

    @classmethod
    def select_for(
        cls,
        session: sqlalchemy.orm.session.Session,
        user: User,
        object_type: str,
        object_roles: Optional[Iterable[str]] = None,
    ) -> Any:
        if object_roles is None:
            object_roles = [r.value for r in ObjectRole.Roles]
        filters = [
            ObjectRole.deleted_at == None,
            ObjectRole.object_type == object_type,
            ObjectRole.object_role.in_(object_roles),
        ]
        for org_roles in user.roles:
            filters.extend(
                [
                    Organization.source_id == org_roles.organization.id,
                    Organization.source == org_roles.organization.source,
                    ObjectRole.organization_role.in_(org_roles.roles),
                ]
            )
        return session.query(ObjectRole.object_id).join(Organization).filter(*filters)
