from example.model.runner import *
from example.model.order import *
from example.model.bank import *
from example.model.bank_account import *

class TestOrderModel(unittest.TestCase):
    def test_attrs_exist(self):
	o=Order(description='description', total=12.34, runner_id=1,
                platform_fee=0.225)
        self.assertTrue(o.description == 'description')
        self.assertTrue(o.total == 12.34)
        self.assertTrue(o.runner_id == 1)
        self.assertTrue(o.status == 'submitted')
        self.assertTrue(isinstance(o.runner,Runner))

class TestRunnerModel(unittest.TestCase):
    def test_attrs_exist(self):
        r=Runner(name="test_runner", acct_id='test_account', bank_id='bb.01.nl.nl',
                runner_fee=6.00)
        self.assertTrue(r.name == 'test_runner')
        self.assertTrue(r.acct_id == 'test_account')
        self.assertTrue(r.bank_id == 'bb.01.nl.nl')
        self.assertTrue(r.runner_gee == 6.00)
        self.assertTrue(r.availabe == True)

