from .base import Base, PkType

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship, backref


class DatasetDataSchema(Base):

    __tablename__ = "dataset_dataschema"

    """
    Describes a data set version mapped to a data schema.
    """

    dataset_id = Column(PkType, ForeignKey("dataset.id"), nullable=False)
    dataschema_id = Column(PkType, ForeignKey("dataschema.id"), nullable=False)

    dataset = relationship(
        "Dataset",
        backref=backref("dataschemas", cascade="all,delete,delete-orphan"),
        innerjoin=True,
    )
    dataschema = relationship(
        "DataSchema",
        backref=backref("datasets", cascade="all,delete,delete-orphan"),
        innerjoin=True,
    )
