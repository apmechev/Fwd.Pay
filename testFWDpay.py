import FWDpay

#g=FWDpay.OBPClient('bb.01.nl.nlf','FWDPay')
#g=FWDpay.OBPClient('bb.01.nl.nl','dfasfdsFWDpay')
g=FWDpay.OBPClient('bb.01.nl.nl','FWD.Pay')
print(g.check_balance())
g.send_payment(100,g.bank_id, 'FWDPay')
print(g.check_balance())

g=FWDpay.OBPClient('bb.01.nl.nl','FWDPay')
print(g.check_balance())
g.send_payment(100,g.bank_id, 'FWD.Pay')
print(g.check_balance())




