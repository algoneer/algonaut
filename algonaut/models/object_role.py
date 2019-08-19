from .base import Base, ExtPkType

from sqlalchemy import Column, Unicode
from algonaut.utils.auth import User, Organization
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

    organization_id = Column(ExtPkType, nullable=False)
    object_id = Column(ExtPkType, nullable=False)
    object_type = Column(Unicode)
    organization_role = Column(Unicode)
    object_role = Column(Unicode)

    # we unset the data field...
    data = None

    @classmethod
    def get_or_create(
        cls,
        session: "sqlalchemy.orm.session.Session",
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
                ObjectRole.object_id == object.ext_id,
                ObjectRole.object_type == object.type,
                ObjectRole.object_role == object_role,
                ObjectRole.organization_role == organization_role,
            )
            .one_or_none()
        )

        if obj_role is None:
            obj_role = ObjectRole(
                organization_id=organization.id,
                object_id=object.ext_id,
                object_type=object.type,
                object_role=object_role,
                organization_role=organization_role,
            )
            session.add(obj_role)

        return obj_role

    @classmethod
    def roles_for(
        cls, session: "sqlalchemy.orm.session.Session", user: User, object: Base
    ):
        return (
            session.query(ObjectRole)
            .filter(
                ObjectRole.organization_id == user.roles.organization.id,
                ObjectRole.organization_role.in_(user.roles.roles),
                ObjectRole.object_id == object.ext_id,
                ObjectRole.object_type == object.type,
            )
            .all()
        )

    @classmethod
    def select_for(
        cls,
        session: "sqlalchemy.orm.session.Session",
        user: User,
        object_type: str,
        object_roles: Optional[Iterable[str]] = None,
    ) -> Any:
        if object_roles is None:
            object_roles = [r.value for r in ObjectRole.Roles]
        return session.query(ObjectRole.object_id).filter(
            ObjectRole.organization_id == user.roles.organization.id,
            ObjectRole.organization_role.in_(user.roles.roles),
            ObjectRole.object_role.in_(object_roles),
            ObjectRole.deleted_at == None,
        )
