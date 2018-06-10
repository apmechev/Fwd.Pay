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
    __omit_fields__ = ['status','runner','platform_fee','user']
add_order_form = AddOrder(DBSession)


def get_random_runner():
    runners = DBSession.query(Runner).filter(Runner.available == True)
    random_runner_id = int(random.uniform(0,runners.count()+1))
    random_runner = runners[random_runner_id]
    return random_runner.uid


class OrderController(BaseController):

    @expose()
    def index(self):
        redirect('orders/vieworder?_id=1')

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

    @expose('example.templates.index')
    def index(self):
        """Handle the front-page."""
        return dict(page='index')

    @expose('example.templates.FWDPay')
    def FWDpay(self, **named):
        """Handle the front-page."""
        runners = DBSession.query( Runner ).order_by( Runner.name )
        tmpl_context.add_order_form = add_order_form
        return dict(page='FWDPay',runners=runners)

    @expose('example.templates.Runners')
    def Runners(self, **named):
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


    @expose('example.templates.about')
    def about(self):
        """Handle the 'about' page."""
        return dict(page='about')

    orders = OrderController()

    @expose('example.templates.environ')
    def environ(self):
        """This method showcases TG's access to the wsgi environment."""
        return dict(page='environ', environment=request.environ)

    @expose('example.templates.data')
    @expose('json')
    def data(self, **kw):
        """
        This method showcases how you can use the same controller
        for a data page and a display page.
        """
        return dict(page='data', params=kw)
    @expose('example.templates.index')
    @require(predicates.has_permission('manage', msg=l_('Only for managers')))
    def manage_permission_only(self, **kw):
        """Illustrate how a page for managers only works."""
        return dict(page='managers stuff')

    @expose('example.templates.index')
    @require(predicates.is_user('editor', msg=l_('Only for the editor')))
    def editor_user_only(self, **kw):
        """Illustrate how a page exclusive for the editor works."""
        return dict(page='editor stuff')

#    @expose('example.templates.login')
#    def login(self, came_from=lurl('/'), failure=None, login=''):
#        """Start the user login."""
#        if failure is not None:
#            if failure == 'user-not-found':
#                flash(_('User not found'), 'error')
#            elif failure == 'invalid-password':
#                flash(_('Invalid Password'), 'error')
#
#        login_counter = request.environ.get('repoze.who.logins', 0)
#        if failure is None and login_counter > 0:
#            flash(_('Wrong credentials'), 'warning')
#
#        return dict(page='login', login_counter=str(login_counter),
#                    came_from=came_from, login=login)

    @expose()
    def post_login(self, came_from=lurl('/')):
        """
        Redirect the user to the initially requested page on successful
        authentication or redirect her back to the login page if login failed.

        """
        if not request.identity:
            login_counter = request.environ.get('repoze.who.logins', 0) + 1
            redirect('/login',
                     params=dict(came_from=came_from, __logins=login_counter))
        userid = request.identity['repoze.who.userid']
        flash(_('Welcome back, %s!') % userid)

        # Do not use tg.redirect with tg.url as it will add the mountpoint
        # of the application twice.
        return HTTPFound(location=came_from)

    @expose()
    def post_logout(self, came_from=lurl('/')):
        """
        Redirect the user to the initially requested page on logout and say
        goodbye as well.

        """
        flash(_('We hope to see you soon!'))
        return HTTPFound(location=came_from)

