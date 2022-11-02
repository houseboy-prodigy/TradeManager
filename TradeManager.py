from kucoin_futures.client import Trade



api_key = '630fe5b137a609000198dad4'
api_secret = '10ec6fd4-1dcd-447b-b0cf-521aab359bd7'
api_passphrase = 'SepactMfdst1114'
    # Trade
client_trade = Trade(key=api_key, secret=api_secret, passphrase=api_passphrase,
is_sandbox=True, url='https://api-sandbox-futures.kucoin.com')

class TradeManager(object):

    def __init__(self,tradeObj):
        self.tradeObj = tradeObj

    def manage_trade(self):
        trade_pair = self.tradeObj['Curr'].strip() + 'USDTM'
        trade_side = self.tradeObj['side']
        trade_leverage = 1
        tp_hit_num = 0
        #trade_size and lotsizeperc math
        lot_size_perc = self.find_lot_size(tp_hit_num)
        #lot_quantity_logic
        tp_arr = self.tradeObj['TP']
        sl = self.tradeObj['SL']
        tp_len = len(tp_arr) - 1
        for i in range(0,tp_len):
            trigger_label = self.place_order_and_check_status(trade_pair,trade_side,trade_leverage, tp_arr[i],sl)
            if(trigger_label == 0):
                break
            else:
                tp_hit_num += 1
                i =+ 1

        self.createTradeStats()

    def createTradeStats(self):
        pass


    def find_lot_size(self,tp_hit_num):
        if(tp_hit_num == 0):
            return 25
        elif(tp_hit_num == 1):
            return 30
        elif(tp_hit_num == 2):
            return 35
        else:
            return 10
        


    def place_order_and_check_status(self,curr,side,lev,tp,sl):
        tp_order_id = client_trade.create_limit_order(curr, side, lev, lot_quantity, tp)
        sl_order_id = client_trade.create_limit_order(curr, side, lev, lot_quantity, sl)
        tp_or_sl = 0
        while(True):
            tp_details = client_trade.get_order_details(tp_order_id)
            sl_details = client_trade.get_order_details(sl_order_id)
            if(tp_details['status'] == 'done'):
                tp_or_sl = 1
                break
            elif(sl_details['status' == 'done']):
                break
                
        return tp_or_sl
