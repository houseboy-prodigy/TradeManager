from kucoin_futures.client import Trade
from kucoin_futures.client import Market

'''
client = Market(url='https://api-sandbox-futures.kucoin.com')
api_key = '630fe5b137a609000198dad4'
api_secret = '10ec6fd4-1dcd-447b-b0cf-521aab359bd7'
api_passphrase = 'SepactMfdst1114'
'''
client = Market(url='https://api-futures.kucoin.com')
api_key = '634b944da99b0c00016f4c02'
api_secret = 'fb43171f-1aad-4418-8577-0ce672b308c6'
api_passphrase = 'SepactMfdst1114'
client_trade = Trade(key=api_key, secret=api_secret, passphrase=api_passphrase,is_sandbox=False, url='https://api-futures.kucoin.com')

class kcscalls(object):


        # Trade
    client_trade = Trade(key=api_key, secret=api_secret, passphrase=api_passphrase,
    is_sandbox=False, url='https://api-futures.kucoin.com')

    client = Market(url='https://api-futures.kucoin.com')

    def __init__(self,tradeObj):
        self.tradeObj = tradeObj

    def cancelLimitOrders(self,curr):
        client_trade.cancel_all_limit_order(curr)


    def demoTradeCalls(self):

        params = {'stop': 'loss', 'stopPrice': 1500 , 'stopPriceType': 'TP'}
        order_id = client_trade.create_limit_order('XBTUSDTM', 'buy', 1, 1, 2000.0,params=params)
        #add stop order
        print(order_id)

    def getPriceData(self,curr):
        #curr_pair = curr+'USDTM'
        price_data = client.get_ticker(curr)
        return price_data

    def get_contract_detail(self,curr):
        contract_detail = client.get_contract_detail(curr)
        return contract_detail

    def trade_side_reverse(self,side):
        return 'buy' if side == 'sell' else 'sell'

    def create_limit_order(self,trade_pair,trade_side,trade_leverage,lot_quantity,price):
        order_id = client_trade.create_limit_order(trade_pair, trade_side, trade_leverage, lot_quantity, price)
        return order_id

    #def create_market_order(tradeObj):
    #    pass

    def create_stop_order(self,trade_pair,trade_side,trade_leverage,lot_quantity,price,params):
        order_id = client_trade.create_limit_order(trade_pair, self.trade_side_reverse(trade_side), trade_leverage, lot_quantity, price,params=params)
        #order_id = client_trade.create_limit_order(symbol=symbol, type='limit', side=side, amount=amount, price=price, params=params)
        return order_id

if __name__ == "__main__":

    #cancel orders
    #print(client_trade.cancel_all_limit_order('ADAUSDTM'))
    #print(client_trade.cancel_order('634b3bd62b968a0001bf1134'))
    tradeobj = (client_trade.get_position_details('CHZUSDTM'))
    print(tradeobj)
    #pricetosell = (getPriceData('CHZUSDTM'))['price']
    #print(client_trade.get_order_details('634b3bd62b968a0001bf1134'))
    #print(getPriceData('CHZUSDTM'))

    #create_orders
    #print(client_trade.create_limit_order('CHZUSDTM', 'sell', 5, 2, pricetosell))
    #print(client_trade.create_market_order('CHZUSDTM','sell',5,size=1))