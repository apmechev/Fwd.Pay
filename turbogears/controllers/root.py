# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import expose, flash, require, url, lurl
from tg import request, redirect, tmpl_context
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tg.exceptions import HTTPFound
from tg import predicates
from tg import validate
from example import model
from example.controllers.secure import SecureController
from example.model import DBSession
from tgext.admin.tgadminconfig import BootstrapTGAdminConfig as TGAdminConfig
from tgext.admin.controller import AdminController
from tg import tmpl_context
from tgext.crud import EasyCrudRestController
from formencode import validators



from example.lib.base import BaseController
from example.controllers.error import ErrorController
from example.model.runner import *
import random

__all__ = ['RootController']

from sprox.formbase import AddRecordForm
from tg import tmpl_context
from example.model.order import *
from example.model import DeclarativeBase, metadata, DBSession


class AddOrder(AddRecordForm):
    __model__ = Order
    __omit_fields__ = ['status','runner','platform_fee']
add_order_form = AddOrder(DBSession)


def get_random_runner():
    runners = DBSession.query(Runner).filter(Runner.available == True)
    random_runner_id = int(random.uniform(0,runners.count()+1))
    random_runner = runners[random_runner_id]
    return random_runner.uid


class OrderController(BaseController):

    @expose()
    def index(self):
        redirect('list/')

    @expose('example.templates.Order')
    @validate({"_id" : validators.Int(max=DBSession.query(Order).count())  })
    def vieworder(self, _id=None):
        """Handle the 'about' page."""
        order = DBSession.query(Order)[int(_id) - 1]
        total = order.total
        status = order.status
        description = order.description
	order_runner = order.runner 
        return dict(page='Order', order_id=_id, total="%.2f"%total, status=status,
                description=description, order_runner=order_runner)

    def create(self, title, text, order_id=1, **kw):
        order_page = Page(title=tile, text=text, order_id=_id, tags=str(kw))
        DBSession.add(order_page)


class RootController(BaseController):
    """
    The root controller for the example application.

    All the other controllers and WSGI applications should be mounted on this
    controller. For example::

        panel = ControlPanelController()
        another_app = AnotherWSGIApplication()

    Keep in mind that WSGI applications shouldn't be mounted directly: They
    must be wrapped around with :class:`tg.controllers.WSGIAppController`.

    """
    secc = SecureController()
    admin = AdminController(model, DBSession, config_type=TGAdminConfig)

    error = ErrorController()

    def _before(self, *args, **kw):
        tmpl_context.project_name = "example"


    @expose('example.templates.FWDPay')
    def FWDpay(self, **named):
        """Handle the front-page."""
        runners = DBSession.query( Runner ).order_by( Runner.name )
        tmpl_context.add_order_form = add_order_form
        return dict(page='FWDPay',runners=runners)


    @expose( )
    @validate(
        form=add_order_form,
        error_handler=index)
    def add_order( self, description, total):
        """Create a new order record"""
	runner_id = get_random_runner()
        new = Order(
            runner_id = runner_id,
            description = description,
            status = 'submitted',
            total = total,
            platform_fee= 0.225,
        )
        DBSession.add( new )
        count = DBSession.query( Order ).count()
        runner = DBSession.query(Runner ).order_by(Runner.uid)[runner_id - 1]
	runner.available = False
        flash( '''Added Order #%s for EUR %s with runner %s'''%( count ,total, runner.name ))
        redirect( './FWDpay' )

    orders = OrderController()

    @expose('example.templates.environ')
    def environ(self):
        """This method showcases TG's access to the wsgi environment."""
        return dict(page='environ', environment=request.environ)

