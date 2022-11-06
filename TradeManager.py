import time

from kucoin_futures.client import Trade


class TradeManager(object):

    def __init__(self, tradeObj, client_trade):
        self.tradeObj = tradeObj
        self.client_trade = client_trade

    def trade_side_reverse(self,side):
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

    def manage_trade(self,tp,tpnum):
        print(f'at manage_trade, tp:{tp} , tpnum: {tpnum}')
        trade_pair = self.tradeObj['Curr'].strip() + 'USDTM'
        trade_side = self.tradeObj['side']
        tp_arr = self.tradeObj['TP']
        sl = self.tradeObj['SL']
        sl = self.get_updated_sl(sl,tpnum)
        print(f'tp_num: {tpnum}, updated sl: {sl}')
        trade_leverage = 1
        tp_hit_num = tpnum
        position_details = self.client_trade.get_position_details(trade_pair)
        print('**************************\n'
              f'{position_details}')
        print('***************************')
        current_quantity = position_details['currentQty']
        tp_quantity = self.find_tp_strat(tpnum,current_quantity)
        tp_quantity = round(tp_quantity)
        print(f'tp_quantity: {tp_quantity}')
        params = {'stop': 'down', 'stopPrice': sl}
        trade_side_reverse = self.trade_side_reverse(trade_side)
        if trade_side == 'buy':
            tp_order_id = self.client_trade.create_limit_order(trade_pair, trade_side_reverse, trade_leverage, tp_quantity, tp)
            time.sleep(5)
            sl_order_id = self.client_trade.create_stop_market_order(trade_pair,trade_side_reverse,trade_leverage,current_quantity,params)
        else:
            params = {'stop': 'up', 'stopPrice': sl}
            tp_quantity = abs(tp_quantity)
            current_quantity = abs(current_quantity)
            tp_order_id = self.client_trade.create_limit_order(trade_pair, trade_side_reverse, trade_leverage,
                                                               tp_quantity, tp)
            time.sleep(5)
            sl_order_id = self.client_trade.create_stop_market_order(trade_pair, trade_side_reverse, trade_leverage,
                                                                     current_quantity, params)
        return tp_order_id, sl_order_id

    def createTradeStats(self):
        pass

    def find_tp_strat(self, tp_hit_num, current_qty):
        if (tp_hit_num == 0):
            return (current_qty* 0.15)
        elif (tp_hit_num == 1):
            return (current_qty*0.25)
        elif (tp_hit_num == 2):
            return (current_qty* 0.35)
        else:
            return (current_qty * 0.10)

