# -*- coding: utf-8 -*-
"""Setup the example application"""
from __future__ import print_function, unicode_literals
import transaction
from example import model
from example.model.runner import *
from example.model.bank import *
from example.model.order import *
def bootstrap(command, conf, vars):
    """Place any commands to setup example here"""
    # <websetup.bootstrap.before.auth
    from sqlalchemy.exc import IntegrityError
    try:
        run1 = Runner(name="Runner0",acct_id='Runner0',bank_id='bb.01.nl.nl')
	model.DBSession.add(run1)
        model.DBSession.flush()
        transaction.commit()

	b1 = Bank(bank_id='bb.01.nl.nl')
        model.DBSession.add(b1)
        model.DBSession.flush()
        transaction.commit()

        o=Order(total=00.00, status="test_order", runner_id=1 , platform_fee=0.05, description="")
        model.DBSession.add(o)
        model.DBSession.flush()
        transaction.commit()

    except IntegrityError:
        print('Warning, there was a problem adding your auth data, '
              'it may have already been added:')
        import traceback
        print(traceback.format_exc())
        transaction.abort()
        print('Continuing with bootstrapping...')

    # <websetup.bootstrap.after.auth>
