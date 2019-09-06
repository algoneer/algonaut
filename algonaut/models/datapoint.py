from .base import Base
from .hashable import Hashable
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import BYTEA


import sqlalchemy


class Datapoint(Hashable, Base):

    __tablename__ = "datapoint"

    """
    Describes a datapoint.
    """

    hash = Column(BYTEA, nullable=False)

    def get_existing(self, session: sqlalchemy.orm.session.Session):
        return (
            session.query(Datapoint)
            .filter(Datapoint.hash == self.hash, Datapoint.deleted_at == None)
            .one_or_none()
        )

    @classmethod
    def hash_data(cls, data):
        return {"data": data.get("data")}
