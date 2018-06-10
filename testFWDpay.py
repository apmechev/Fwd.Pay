import FWDpay
import unittest


class TestOBPClient(unittest.TestCase):
    def test_bank_transfer():
        g = FWDpay.OBPClient('bb.01.nl.nl','User1')
        init_bal = g.check_balance()
        g.send_payment(100,g.bank_id, 'FWDPay')
        self.assertTrue(g.check_balance( )== init_bal-100)
        
        g = FWDpay.OBPClient('bb.01.nl.nl','FWDPay')
        init_rec = g.check_balance()
        g.send_payment(100,g.bank_id, 'User1')
        self.assertTrue(g.check_balance() == init_rec-100)


    def test_bad_bank(self):
        with self.assertRaises(Exception) as context:
            g = FWDpay.OBPClient('bogus_bank_name_here','FWD.Pay')

        self.assertTrue('Bank not found in banks list' in context.exception)

    def test_bad_account(self):
        with self.assertRaises(Exception) as context:
            g = FWDpay.OBPClient('bb.01.nl.nl','totally_fake_account')

        self.assertTrue('Account not found in accounts list' in context.exception)

   def test_unequal_currency(self):
        with self.assertRaises(Exception) as context:
            g = FWDpay.OBPClient('bb.01.nl.nl','User1')
            g.send_payment(100,g.bank_id, 'test_account')
        
        self.assertTrue('Unequal Currencies EUR!=GBP' in context.exception) 




