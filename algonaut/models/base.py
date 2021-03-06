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

from typing import Optional


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

    @classmethod
    def hash_data(cls, data):
        raise NotImplementedError

    def export_fields(self):
        return {}

    def export(self):
        d = {
            "id": self.ext_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at,
            "data": self.data,
        }
        d.update(self.export_fields())
        # decorators might set role context for the object and given user, if such a context
        # exists we return it as well...
        if hasattr(self, "_roles"):
            d["roles"] = [role.export() for role in self._roles]
        return d

    def delete(
        self, session: sqlalchemy.orm.session.Session, context: Optional["Base"] = None
    ) -> None:
        """
        This is the default delete implementation, which just uses SQLAlchemy's
        delete capabilities. We may override this in subclasses to provide more
        efficient deletion capabilities.

        :param session: The SQLAlchemy session that should be used to delete the object.
        :param context: An optional context object for the deletion. Sometimes useful
                        to determine which linked classes to delete or to modify the
                        default deletion behavior.
        """
        session.delete(self)

    def get_existing(self, session: sqlalchemy.orm.session.Session):
        return None
