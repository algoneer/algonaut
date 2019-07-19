from .base import Base, PkType, ExtPkType

from sqlalchemy import Column, DateTime, Unicode, BigInteger, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

class AlgorithmVersionAlgorithmSchema(Base):

    __tablename__ = 'algorithmversion_algorithmschema'

    """
    Describes an algorithm version mapped to an algorithm schema.
    """

    algorithmversion_id = Column(PkType, ForeignKey('algorithmversion.id'), index=True, nullable=False)
    algorithmschema_id = Column(PkType, ForeignKey('algorithmschema.id'), index=True, nullable=False)

    algorithmversion = relationship('AlgorithmVersion', backref=backref('schemas', cascade="all,delete,delete-orphan"))
    algorithmschema = relationship('AlgorithmSchema', backref=backref('versions', cascade="all,delete,delete-orphan"))
