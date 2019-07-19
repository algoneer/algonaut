from .base import Base, PkType, ExtPkType

from sqlalchemy import Column, DateTime, Unicode, BigInteger, Integer

class Algorithm(Base):

    __tablename__ = 'algorithm'

    """
    Describes an algorithm.
    """