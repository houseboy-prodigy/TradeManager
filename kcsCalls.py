from kucoin_futures.client import Trade
from kucoin_futures.client import Market
import makefile as mk

makeFileObject = mk.safeHello()
data = makeFileObject.decrypt()

key1 = str(data[0], encoding='utf-8')
key2 = str(data[1], encoding='utf-8')
key3 = str(data[2], encoding='utf-8')

client = Market(url='https://api-futures.kucoin.com')
api_key = key1
api_secret = key2
api_passphrase = key3

client_trade = Trade(key=api_key, secret=api_secret, passphrase=api_passphrase,is_sandbox=False, url='https://api-futures.kucoin.com')

class kcscalls(object):


        # Trade
    client_trade = Trade(key=api_key, secret=api_secret, passphrase=api_passphrase,
    is_sandbox=False, url='https://api-futures.kucoin.com')

    client = Market(url='https://api-futures.kucoin.com')

    def __init__(self,tradeObj):
        self.tradeObj = tradeObj
        self.clientt = client_trade

    def cancelLimitOrders(self,orderid):
        client_trade.cancel_order(orderid)


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
        try:
            order_id = client_trade.create_limit_order(trade_pair, trade_side, trade_leverage, lot_quantity, price)
            return order_id
        except Exception as e:
            print('error')
            exceptionStr = str(e)
            print(f'exception at kcscalls.py: {e}')
            code = (exceptionStr[13:19])
            if (code == '300003'):
                return ('balInsuff')
            elif (code == '100000'):
                return 'decimalError'
            elif code == '100001':
                return 'quantityInvalid'
            elif code == '429000':
                return 'tooMany'

    #def create_market_order(tradeObj):
    #    pass

    def create_stop_order(self,trade_pair,trade_side,trade_leverage,lot_quantity,price,params):
        order_id = client_trade.create_limit_order(
            symbol=trade_pair,
            side=trade_side,
            lever=trade_leverage,
            size=lot_quantity,
            price=price,
            stop=params['stop'],
            stopPrice=params['stopPrice'],  # When the price is reached, it will enter the orderbook and the funds will be frozen
            stopPriceType='MP',
        )
        return order_id

    def create_stop_market_order(self, trade_pair, trade_side, trade_leverage, lot_quantity, params):
        order_id = client_trade.create_market_order(
                symbol=trade_pair,
                side=trade_side,
                lever=trade_leverage,
                size=lot_quantity,
                stop=params['stop'],
                stopPrice=params['stopPrice'],
                # When the price is reached, it will enter the orderbook and the funds will be frozen
                stopPriceType='MP',
        )
        return order_id

    def get_position_details(self,symbol):
        return client_trade.get_position_details(symbol)

    def checkLimitOrderStatus(self, orderId):
        return client_trade.get_order_details(orderId)
if __name__ == "__main__":

    #cancel orders
    #print(client_trade.cancel_all_limit_order('ADAUSDTM'))
    #print(client_trade.cancel_order('634b3bd62b968a0001bf1134'))
    #print(client_trade.get_position_details('MATICUSDTM'))
    try:
        order = client_trade.create_limit_order(
            symbol='MATICUSDTM',
            side='buy',
            lever=1,
            size='3',
            price='1.22',
        )
        print(order)
    except Exception as e:
        print('error')
        exceptionStr = str(e)
        print(e)
        code = (exceptionStr[13:19])
        if(code == '300003'):
            print('bal insuff')



'''
    #print(client_trade.get_order_details('636703eceda1bc0001f22353'))
     #- stop loss order
    order = client_trade.create_limit_order(
        symbol='MATICUSDTM',
        side='sell',
        lever=1,
        size='1',
        price='1.22',
    )
    print(order)


    
    #- stop loss market order
    order = client_trade.create_market_order(
        symbol='XRPUSDTM',
        side='sell',
        lever=1,
        size='1',
        stop='down',
        stopPrice='0.4545',  # When the price is reached, it will enter the orderbook and the funds will be frozen
        stopPriceType='MP',
    )
    print(order)

    '''
    #pricetosell = (getPriceData('CHZUSDTM'))['price']
    #print(client_trade.get_order_details('634b3bd62b968a0001bf1134'))
    #print(getPriceData('CHZUSDTM'))
    #print(client.get_contract_detail('XRPUSDTM'))
    #create_orders
    #print(client_trade.create_limit_order('CHZUSDTM', 'sell', 5, 2, pricetosell))
    #print(client_trade.create_market_order('CHZUSDTM','sell',5,size=1))