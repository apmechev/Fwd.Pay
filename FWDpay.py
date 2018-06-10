"""
.. module:: FWDpay
   :platform: Unix
   :synopsis: A Module that integrates with Payment APIs and allows to calculate fees for BunRun

.. moduleauthor:: Alexandar Mechev <apmechev@gmail.com>


"""



from __future__ import print_function    # (at top of module)
import sys
import time
import requests
import pdb

from props.default import *

# You probably don't need to change those
import lib.obp

class Bank_Account(object):
    def __init__(self, bank_id, account_id):
        self.bank_id = bank_id
        self.account_id = account_id


class FWDpay_client(object):
    """Parent class for all our clients. It defines 
    all the methods an API needs to support"""
    def __init__(self):
        raise(NotImplementedError)

    def authorize(self):
        raise(NotImplementedError)

    def check_balance(self, bank_account):
        raise(NotImplementedError)

    def block_balance(self, amount, bank_account):
        raise(NotImplementedError)

    def transfer(self, amount, bank_account ):
        raise(NotImplementedError)



class OBPClient(FWDpay_client):
    """ Interface using the OBP API
    """

    def __init__(self, bank_account=Bank_Account('bank_id','acct_id'), verbose=False):
        self.obp = lib.obp
        if not verbose:
            self.obp.LOGGING = False
        self.obp.setBaseUrl(BASE_URL)
        self.obp.setBaseUrl(BASE_URL)
        self.obp.setApiVersion(API_VERSION)
        self.bank_id = bank_account.bank_id
        self.authorize(USERNAME, PASSWORD)
        self._verify_bank_id(self.bank_id)
        self.account_id = bank_account.account_id 
        self._verify_account_id(self.account_id)
        self.verbose = verbose

    def _verify_bank_id(self, bank_id):
        if not bank_id in [i['id'] for i in self.obp.getBanks()]:
            raise(RuntimeError("Bank not found in banks list"))

    def _verify_account_id(self, account_id):
        accounts = self.obp.getPrivateAccounts(self.bank_id)
        if account_id not in [i['id'] for i in accounts]:
            raise(RuntimeError("Account not found in accounts list"))


    def authorize(self,username,password):
        """ Username and Password Authorization for the OBP api
        """ 
        self.obp.login(username,password, CONSUMER_KEY)
        self.user = self.obp.getCurrentUser()
        
    def check_balance(self, bank_account=None):
        """Check if the account has sufficient balance for the transaction
        """
        bank_id = self.bank_id
        account_id = self.account_id
        account_data = self.obp.getAccount(self.bank_id, self.account_id)
        amount = account_data['balance']['amount']
        currency = account_data['balance']['currency']
        return {'account_id':account_id,'amount':amount, 'currency':currency}

    def send_payment(self, amount, rec_bank_account ):
        amount = str(amount)
        self._verify_account_id(rec_bank_account.account_id)
        self._verify_bank_id(rec_bank_account.bank_id)
        account_data = self.obp.getAccount(
                rec_bank_account.bank_id,
                rec_bank_account.account_id)
        target_currency = account_data['balance']['currency']
        if target_currency != OUR_CURRENCY:
            raise(ValueError("Unequal Currencies "+ OUR_CURRENCY + "!=" + target_currency ))
        self.obp.setPaymentDetails(OUR_CURRENCY, amount) 
        initiate_response = self.obp.createTransactionRequestV210(from_bank_id=self.bank_id,
                                    from_account_id=self.account_id,
                                    transaction_request_type="SANDBOX_TAN",
                                    to_bank_id=rec_bank_account.bank_id,
                                    to_account_id=rec_bank_account.account_id,
                                    to_counterparty_id="",  # used for SEPA
                                    to_counterparty_iban="")  # used for COUNTERPARTY
        if self.verbose:
            self.obp.printMessageNoChallenge(initiate_response)


CONVENIENCE_TAX = 0.09
PLATFORM_FEE = 0.225

#TODO: Close token after transfer

def calculate_transfer_amounts(bill_amount, runner_fee):
    platform_fee_sum = platform_fee(bill_amount, runner_fee)
    runner_takeaway_sum = runner_takeaway(bill_amount, runner_fee)
    return {'platform_fee':platform_fee_sum, 
            'runner_takeaway':runner_takeaway_sum, 
            'total_bill':bill_amount}

def calculate_convenience_amount(bill_amount): 
    conv_amount = 2
    if CONVENIENCE_TAX*bill_amount > 2:
        conv_amount = CONVENIENCE_TAX*bill_amount
    return conv_amount 

def platform_fee(bill_amount, runner_fee):
    convenience_amount = calculate_convenience_amount(bill_amount) * PLATFORM_FEE
    runner_amount = runner_fee * PLATFORM_FEE
    return (convenience_amount + runner_amount)

def runner_takeaway(bill_amount, runner_fee):
    convenience_amount = calculate_convenience_amount(bill_amount) * (1 - PLATFORM_FEE)
    runner_amount = runner_fee * (1 - PLATFORM_FEE)
    return (convenience_amount + runner_amount)




