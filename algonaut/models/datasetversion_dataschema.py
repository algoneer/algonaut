from .base import Base, PkType, ExtPkType

from sqlalchemy import Column, DateTime, Unicode, BigInteger, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref


class DataSetVersionDataSchema(Base):

    __tablename__ = "datasetversion_dataschema"

    """
    Describes a data set version mapped to a data schema.
    """

    datasetversion_id = Column(
        PkType, ForeignKey("datasetversion.id"), index=True, nullable=False
    )
    dataschema_id = Column(
        PkType, ForeignKey("dataschema.id"), index=True, nullable=False
    )

    datasetversion = relationship(
        "DataSetVersion",
        backref=backref("dataschemas", cascade="all,delete,delete-orphan"),
    )
    dataschema = relationship(
        "DataSchema", backref=backref("datasets", cascade="all,delete,delete-orphan")
    )
