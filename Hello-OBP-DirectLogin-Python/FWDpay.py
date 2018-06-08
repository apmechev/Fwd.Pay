from __future__ import print_function    # (at top of module)
import sys
import time
import requests
import pdb

# Note: in order to use this example, you need to have at least one account
# that you can send money from (i.e. be the owner).
# All properties are now kept in one central place

from props.default import *


# You probably don't need to change those
import lib.obp
obp = lib.obp

obp.setBaseUrl(BASE_URL)
obp.setBaseUrl(BASE_URL)
obp.setApiVersion(API_VERSION)

# Login and set authorized token
obp.login(USERNAME, PASSWORD, CONSUMER_KEY)

user = obp.getCurrentUser()
print("current user data:\n{0}".format(user))
user_id = user['user_id']
print("current user id: {0}".format(user))

our_bank = OUR_BANK  # banks[0]['id']
print("our bank: {0}".format(our_bank))

# Get accounts for a specific bank
print(" --- Private accounts")

accounts = obp.getPrivateAccounts(our_bank)

for a in accounts:
        our_account = accounts[0]['id']



def get_balance(our_bank=our_bank, our_account=our_account):
    account_data = obp.getAccount(our_bank, our_account)
    amount = account_data['balance']['amount']
    currency = account_data['balance']['currency']
    return {'amount':amount, 'currency':currency}

print(get_balance())
