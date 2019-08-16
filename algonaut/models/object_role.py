from .base import Base, PkType, ExtPkType

from sqlalchemy import Column, DateTime, Unicode, BigInteger, Integer
from algonaut.utils.worf.user import User
from typing import Iterable, Any
import sqlalchemy


class ObjectRole(Base):

    __tablename__ = "object_role"

    """
    Describes a model.
    """

    organization_id = Column(ExtPkType, nullable=False)
    object_id = Column(ExtPkType, nullable=False)
    object_type = Column(Unicode)
    organization_role = Column(Unicode)
    object_role = Column(Unicode)

    @classmethod
    def select_for(
        cls,
        session: "sqlalchemy.orm.session.Session",
        user: User,
        object_type: str,
        object_roles: Iterable[str],
    ) -> Any:
        return session.query(ObjectRole.object_id).filter(
            ObjectRole.organization_role.in_(user.roles),
            ObjectRole.object_role.in_(object_roles),
            ObjectRole.deleted_at == None,
        )
