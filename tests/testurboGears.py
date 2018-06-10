from example.model.runner import *
from example.model.order import *
from example.model.bank import *
from example.model.bank_account import *

class TestOrderModel(unittest.TestCase):
    def test_attrs_exist(self):
	o=Order(description='description', total=12.34, runner_id=1,
                platform_fee=0.225)
        self.assertTrue(o.description=='description')
        self.assertTrue(o.total==12.34)
        self.assertTrue(o.runner_id==1)
        self.assertTrue(isinstance(o.runner,Runner))
