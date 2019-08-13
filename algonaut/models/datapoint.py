from .base import Base, PkType, ExtPkType

from sqlalchemy import Column, DateTime, Unicode, BigInteger, Integer


class DataPoint(Base):

    __tablename__ = "datapoint"

    """
    Describes a datapoint.
    """
