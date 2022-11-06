import unittest

def trade_side_reverse(side):
    return 'buy' if side == 'sell' else 'sell'


def find_tp_quantity(self, tp_hit_num, current_qty):
    if (tp_hit_num == 0):
        return (current_qty* 0.50)
    elif (tp_hit_num == 1):
        return (current_qty)
    elif (tp_hit_num == 2):
        return (current_qty* 0.35)
    else:
        return (current_qty * 0.10)

def get_updated_sl(self,sl,tpnum):

    if tpnum == 0 or tpnum == 1:
        return sl
    else:
        tp_arr = self.tradeObj['TP']
        sl = tp_arr[tpnum-2]
        return sl

class TestTradeManager(unittest.TestCase):

    def test_checkTradeManagerReverse(self):
        actual = trade_side_reverse(side='buy')
        expected = 'sell'
        self.assertEqual(actual,expected)

    def test_find_tp_quant(self):
        pass

if __name__ == '__main__':
    unittest.main()
