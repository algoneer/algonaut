from .base import Base, PkType, ExtPkType

from sqlalchemy import Column, DateTime, Unicode, BigInteger, Integer

class AlgorithmSchema(Base):

    __tablename__ = 'algorithmschema'

    """
    Describes an algorithm schema.
    """