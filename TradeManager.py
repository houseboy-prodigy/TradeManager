from kucoin_futures.client import Trade


class TradeManager(object):

    def __init__(self, tradeObj, client_trade):
        self.tradeObj = tradeObj
        self.client_trade = client_trade

    def manage_trade(self):
        trade_pair = self.tradeObj['Curr'].strip() + 'USDTM'
        trade_side = self.tradeObj['side']
        trade_leverage = 1
        tp_hit_num = 0

        # trade_size and lotsizeperc math
        lot_size_perc = self.find_lot_size(tp_hit_num)
        # lot_quantity_logic
        tp_arr = self.tradeObj['TP']
        sl = self.tradeObj['SL']
        tp_len = len(tp_arr) - 1

        tp_order_id = self.client_trade.create_limit_order(trade_pair,'sell', trade_leverage,1, tp_arr[0])
        print(tp_order_id)


        #trigger_label = self.place_order_and_check_status(trade_pair, trade_side, trade_leverage, tp_arr[0], sl)
        #print(trigger_label)

        '''
            if trigger_label == 0:
                break
            else:
                tp_hit_num += 1
                i = + 1

        self.createTradeStats()
        '''

    def createTradeStats(self):
        pass

    def find_lot_size(self, tp_hit_num):
        if (tp_hit_num == 0):
            return 25
        elif (tp_hit_num == 1):
            return 30
        elif (tp_hit_num == 2):
            return 35
        else:
            return 10

    def place_order_and_check_status(self, curr, side, lev, tp, sl):
        tp_order_id = self.client_trade.create_limit_order(curr, side, lev, 1, tp)
        #sl_order_id = self.client_trade.create_limit_order(curr, side, lev, 1, sl)
        tp_or_sl = 0

        ''' loop for tp or sl hit after entry
        while (True):
            tp_details = self.client_trade.get_order_details(tp_order_id)
            sl_details = self.client_trade.get_order_details(sl_order_id)
            if (tp_details['status'] == 'done'):
                tp_or_sl = 1
                break
            elif (sl_details['status' == 'done']):
                break
        '''
        return tp_or_sl

