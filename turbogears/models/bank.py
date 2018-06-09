# -*- coding: utf-8 -*-
"""Bank model module."""
from sqlalchemy import *
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode, DateTime, LargeBinary
from sqlalchemy.orm import relationship, backref

from example.model import DeclarativeBase, metadata, DBSession


class Bank(DeclarativeBase):
    __tablename__ = 'banks'

    id = Column(Integer, primary_key=True)
    bank_id = Column(Unicode(255), nullable=False)

    user_id = Column(Integer, ForeignKey('tg_user.user_id'), index=True)
    user = relationship('User', uselist=False,
                        backref=backref('banks',
                                        cascade='all, delete-orphan'))


__all__ = ['Bank']
