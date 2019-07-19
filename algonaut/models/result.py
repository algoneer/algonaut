from .base import Base, PkType, ExtPkType

from sqlalchemy import Column, DateTime, Unicode, BigInteger, Integer

class Result(Base):

    __tablename__ = 'result'

    """
    Describes a result.
    """