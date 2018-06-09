# -*- coding: utf-8 -*-
"""Runner model module."""
from sqlalchemy import *
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Numeric, Integer, Unicode, DateTime, LargeBinary
from sqlalchemy.orm import relationship, backref, relation

from example.model import DeclarativeBase, metadata, DBSession
from example.model.bank_account import Bank_account

from example.model.bank import Bank


class Runner(DeclarativeBase):
    __tablename__ = 'runners'

    uid = Column(Integer, primary_key=True)
    name = Column(Unicode(255), nullable=False)
    acct_id = Column(Integer,ForeignKey('bank_accounts.id'), nullable=True)
    bank_account = relation(Bank_account, foreign_keys=acct_id)
    bank_id = Column(Integer,ForeignKey('banks.id'), nullable=True)
    bank = relation(Bank, foreign_keys=bank_id)
    runner_fee = Column(Numeric, default=6.00)
    available = Column(Boolean, nullable=False, default=True)
    user_id = Column(Integer, ForeignKey('tg_user.user_id'), index=True)
    user = relationship('User', uselist=False,
                        backref=backref('runners',
                                        cascade='all, delete-orphan'))


__all__ = ['Runner']
