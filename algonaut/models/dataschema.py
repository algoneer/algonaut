from .base import Base
from .hashable import Hashable

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import BYTEA

import sqlalchemy


class DataSchema(Hashable, Base):

    __tablename__ = "dataschema"

    """
    Describes a data schema.
    """

    hash = Column(BYTEA, nullable=False)

    def get_existing(self, session: sqlalchemy.orm.session.Session):
        return (
            session.query(DataSchema)
            .filter(DataSchema.hash == self.hash, DataSchema.deleted_at == None)
            .one_or_none()
        )

    @classmethod
    def hash_data(cls, data):
        return {"data": data.get("data")}
