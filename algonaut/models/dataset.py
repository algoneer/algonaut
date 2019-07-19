from .base import Base, PkType, ExtPkType

from sqlalchemy import Column, DateTime, Unicode, BigInteger, Integer

class DataSet(Base):

    __tablename__ = 'dataset'

    """
    Describes a data set.
    """
