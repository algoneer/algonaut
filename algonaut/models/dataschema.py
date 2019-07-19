from .base import Base, PkType, ExtPkType

from sqlalchemy import Column, DateTime, Unicode, BigInteger, Integer

class DataSchema(Base):

    __tablename__ = 'dataschema'

    """
    Describes a data schema.
    """