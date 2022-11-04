import TradeManager as tm
import kcscalls as kc
import time
client_trade = kc.kcscalls('params')

def checkOrderStatus(opened_position_order, tradeObj):
    print(f'Loop to check orderstatus of open order: {opened_position_order}')
    TradeManager = tm.TradeManager(tradeObj,client_trade)
    while True:
        orderDetails = client_trade.checkLimitOrderStatus(opened_position_order)
        status = orderDetails['status']
        if (status == 'done'):
            print('order_executed')
            break
        else:
            print(status)
            time.sleep(10)

def checkOrderStatusWithSL(opened_position_order, sl_position_order,tradeObj):
    {f"Loop to check orderstatus of open order: {opened_position_order} and stopOrder: {sl_position_order}"}
    TradeManager = tm.TradeManager(tradeObj,client_trade)
    what_hit = ''
    while True:
        tpOrderDetails = client_trade.checkLimitOrderStatus(opened_position_order)
        time.sleep(1)
        slOrderDetails = client_trade.checkLimitOrderStatus(sl_position_order)
        tpstatus = tpOrderDetails['status']
        slstatus = slOrderDetails['status']
        if (slstatus == 'done'):
            what_hit = 'sl'
            break
        elif(tpstatus == 'done'):
            what_hit = 'tp'
            break
        else:
            print(f'TP trade status: {tpstatus}')
            print(f'SL trade status: {slstatus}')
            time.sleep(10)

    return what_hit