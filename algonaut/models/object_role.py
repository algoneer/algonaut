from .base import Base, PkType, ExtPkType

from sqlalchemy import Column, DateTime, Unicode, BigInteger, Integer

class ObjectRole(Base):

    __tablename__ = 'object_role'

    """
    Describes a model.
    """

    organization_id = Column(ExtPkType, index=True, nullable=False)
    object_id = Column(ExtPkType, index=True, nullable=False)
    object_type = Column(Unicode, index=True)
    organization_role = Column(Unicode, index=True)
    object_role = Column(Unicode, index=True)
