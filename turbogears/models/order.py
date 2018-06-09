# -*- coding: utf-8 -*-
"""Order model module."""
from sqlalchemy import *
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode, DateTime, LargeBinary
from sqlalchemy.orm import relationship, backref, relation

from example.model import DeclarativeBase, metadata, DBSession
from example.model.runner import Runner


class Order(DeclarativeBase):
    __tablename__ = 'orders'

    uid = Column(Integer, primary_key=True)
    description = Column(Unicode(255), nullable=False)

    total = Column(Numeric, nullable=False)
    runner_id = Column(Integer,ForeignKey('runners.uid'), nullable=True)
    runner = relation(Runner, foreign_keys=runner_id)
    platform_fee = Column(Numeric, nullable=False)

    status =  Column(Unicode(255), nullable=False)
    user_id = Column(Integer, ForeignKey('tg_user.user_id'), index=True)
    user = relationship('User', uselist=False,
                        backref=backref('orders',
                                        cascade='all, delete-orphan'))


__all__ = ['Order']
