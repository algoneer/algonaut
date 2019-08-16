from .base import Base, ExtPkType

from sqlalchemy import Column, Unicode
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

    organization_id = Column(ExtPkType, nullable=False)
    object_id = Column(ExtPkType, nullable=False)
    object_type = Column(Unicode)
    organization_role = Column(Unicode)
    object_role = Column(Unicode)

    # we unset the data field...
    data = None

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
