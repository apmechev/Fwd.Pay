# -*- coding: utf-8 -*-
"""Bank_account model module."""
from sqlalchemy import *
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Numeric, Integer, Unicode, DateTime, LargeBinary
from sqlalchemy.orm import relationship, backref

from example.model import DeclarativeBase, metadata, DBSession

__all__ = [ 'Bank_account' ]


class Bank_account(DeclarativeBase):
    __tablename__ = 'bank_accounts'

    id = Column(Integer, primary_key=True)
    data = Column(Unicode(255), nullable=False)

    balance = Column(Numeric, nullable=True)
    currency = Column(Unicode(3), nullable=False)
    user_id = Column(Integer, ForeignKey('tg_user.user_id'), index=True)
    user = relationship('User', uselist=False,
                        backref=backref('bank_accounts',
                                        cascade='all, delete-orphan'))
    def __repr__(self):
        return (u"Bank Account ")

__all__ = ['Bank_account']
