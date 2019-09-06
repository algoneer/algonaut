from .base import Base
from .hashable import Hashable

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import BYTEA

import sqlalchemy


class AlgorithmSchema(Hashable, Base):

    __tablename__ = "algorithmschema"

    """
    Describes an algorithm schema.
    """

    hash = Column(BYTEA, nullable=False)

    def get_existing(self, session: sqlalchemy.orm.session.Session):
        return (
            session.query(AlgorithmSchema)
            .filter(
                AlgorithmSchema.hash == self.hash, AlgorithmSchema.deleted_at == None
            )
            .one_or_none()
        )

    @classmethod
    def hash_data(cls, data):
        return {"data": data.get("data")}
