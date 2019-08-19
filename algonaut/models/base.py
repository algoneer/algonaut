from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import UUIDType, JSONType
from sqlalchemy import BigInteger, Column, DateTime
from sqlalchemy.sql import func
import sqlalchemy
from sqlalchemy.dialects import sqlite, postgresql
from sqlalchemy.orm.attributes import flag_modified

BigIntegerType = BigInteger()
BigIntegerType = BigIntegerType.with_variant(postgresql.BIGINT(), "postgresql")
BigIntegerType = BigIntegerType.with_variant(sqlite.INTEGER(), "sqlite")

DeclarativeBase = declarative_base()
PkType = BigIntegerType
ExtPkType = UUIDType(binary=False)

import uuid


class Base(DeclarativeBase):  # type: ignore

    __abstract__ = True

    id = Column(PkType, primary_key=True)
    ext_id = Column(
        ExtPkType, default=lambda: uuid.uuid4(), nullable=False, unique=True
    )
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(
        DateTime, server_onupdate=func.current_timestamp(), server_default=func.now()
    )
    deleted_at = Column(DateTime)
    data = Column(JSONType, nullable=True)

    def set_data(self, key, value):
        if self.data is None:
            self.data = {}
        self.data[key] = value
        flag_modified(self, "data")

    def get_data(self, key):
        if self.data is None:
            return None
        return self.data.get(key)

    @property
    def type(self):
        return self.__class__.__name__.lower()

    def export(self):
        return {
            "id" : self.ext_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at,
            "data": self.data,
        }

    def delete(self, session: "sqlalchemy.orm.session.Session") -> None:
        """
        This is the default delete implementation, which just uses SQLAlchemy's
        delete capabilities. We may override this in subclasses to provide more
        efficient deletion capabilities.
        """
        session.delete(self)
