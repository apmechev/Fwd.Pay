import FWDpay
import unittest
from FWDpay import Bank_Account as BankAccount

class TestOBPClient(unittest.TestCase):
    def test_bank_transfer(self):
        """Creates a bank transfer and checks if it has succeeded"""

        g = FWDpay.OBPClient(BankAccount('bb.01.nl.nl','User1'))
        init_bal = g.check_balance()
        g.send_payment(10,BankAccount(g.bank_id, 'FWDPay'))
        self.assertTrue(float(g.check_balance()['amount']) == float(init_bal['amount']) - 10)
        
        g = FWDpay.OBPClient(BankAccount('bb.01.nl.nl','FWDPay'))
        init_rec = g.check_balance()
        g.send_payment(10,BankAccount(g.bank_id, 'User1'))
        self.assertTrue(float(g.check_balance()['amount']) == float(init_rec['amount']) - 10)
        g = FWDpay.OBPClient(BankAccount('bb.01.nl.nl','User1'))
        self.assertTrue(float(g.check_balance()['amount']) == float(init_bal['amount']))


    def test_bad_bank(self):
        with self.assertRaises(Exception) as context:
            g = FWDpay.OBPClient(BankAccount('bogus_bank_name_here','FWD.Pay'))

        self.assertTrue('Bank not found in banks list' in context.exception)

    def test_bad_account(self):
        with self.assertRaises(Exception) as context:
            g = FWDpay.OBPClient(BankAccount('bb.01.nl.nl','totally_fake_account'))

        self.assertTrue('Account not found in accounts list' in context.exception)

    def test_unequal_currency(self):
        with self.assertRaises(Exception) as context:
            g = FWDpay.OBPClient(BankAccount('bb.01.nl.nl','User1'))
            g.send_payment(100,BankAccount(g.bank_id, 'test_account'))
        
        self.assertTrue('Unequal Currencies EUR!=GBP' in context.exception) 

class TestFWDCalculations(unittest.TestCase):
    def test_sums_add_up(self):
        total = 100
        runner_fee = 6.00
        fees = FWDpay.calculate_transfer_amounts(total, runner_fee)
        self.assertTrue(fees['total_bill'] == total)
        self.assertTrue(fees['platform_fee'] == total * FWDpay.CONVENIENCE_TAX * FWDpay.PLATFORM_FEE + runner_fee * FWDpay.PLATFORM_FEE)
        self.assertTrue(fees['runner_takeaway'] + fees['platform_fee'] == total * FWDpay.CONVENIENCE_TAX +runner_fee )

    def test_convenience_amount(self):
        bill = 1.99
        self.assertTrue(FWDpay.calculate_convenience_amount(bill) == 2.00 )
        bill = 2.01/ FWDpay.CONVENIENCE_TAX 
        self.assertTrue(FWDpay.calculate_convenience_amount(bill) == bill * FWDpay.CONVENIENCE_TAX )


    def test_platform_fee(self):
        bill = 25.99
        p_fee = FWDpay.platform_fee(bill, 6.00)
        self.assertTrue(p_fee == FWDpay.calculate_convenience_amount(bill) * FWDpay.PLATFORM_FEE + 
                6.00 * FWDpay.PLATFORM_FEE)

