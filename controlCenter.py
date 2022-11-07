import configparser
import json
import re
import time
from kucoin_futures.client import Trade
from telethon.errors import SessionPasswordNeededError
from telethon import TelegramClient, events, sync
from telethon.tl.functions.messages import (GetHistoryRequest)
from kucoin_futures.client import Market
import messageProcess
import EntryManager
import TradeManager as TM
import kcsCalls as kc
import checkOrderStatus as cos

def dreamerEntryBot(message):
    client_trade = kc.kcscalls('params')

    tradeObj = messageProcess.processMessage(message)
    trade_pair = tradeObj['Curr'].strip() + 'USDTM'
    response = client_trade.get_position_details(trade_pair)
    open_position = response['isOpen']
    tradeObject_with_more_details = {}
    if not open_position:
        print(f"******Entry Message Processed from telegram: {tradeObj}******")


        opened_position_order_details, tradeObject_with_more_details = EntryManager.tradeCallToKCS(tradeObj)
        print(f'opened_position_order_details: {opened_position_order_details}')
        #opened_position_order = ''
        cos.checkOrderStatus(opened_position_order_details['orderId'],tradeObject_with_more_details)
        response = client_trade.get_position_details(trade_pair)
        tradeObject_with_more_details['avgEntry'] = response['avgEntryPrice']
        return tradeObject_with_more_details
    else:
        tradeObject_with_more_details = tradeObj
        tradeObject_with_more_details['size'] = ''
        tradeObject_with_more_details['avgEntry'] = 'empty'
        return tradeObject_with_more_details

def dreamerTradeManagerBot(tradeObj,i):
    client_trade = kc.kcscalls('params')
    TradeManager = TM.TradeManager(tradeObj, client_trade)
    print(f"******Message Processed from telegram: {tradeObj}******")
    tp_arr = tradeObj['TP']
    sl = tradeObj['SL']
    arr_index_len = len(tp_arr)
    tp_order_id, sl_order_id = TradeManager.manage_trade(tp_arr[i], i)
    print(f'TP orderid: {tp_order_id}, SL orderid: {sl_order_id}')
    what_hit = cos.checkOrderStatusWithSL(tp_order_id['orderId'], sl_order_id['orderId'], tradeObj)
    print(what_hit)
    if(what_hit == 'tp'):
        client_trade.cancelLimitOrders(sl_order_id['orderId'])
    tradeObj['hit'] = what_hit
    tradeObj['tp_order_id'] = tp_order_id
    tradeObj['sl_order_id'] = sl_order_id
    return tradeObj
#sample tradeObj = {'Curr': 'XRP ', 'TP': ['0.4640', '0.4594', '0.4546', '0.4476', '0.4406', '0.4313'], 'SL': '0.4920', 'entry': ['0.4688 ', ' 0.4780'], 'side': 'sell'}
#tradeObj2 = {'Curr': 'ADA ', 'TP': ['0.4121', '0.4594', '0.4546', '0.4476', '0.4406', '0.4313'],'SL': '0.34', 'entry': ['0.3912 ', ' 0.3800'], 'side': 'buy'}
if __name__ == "__main__":
    message = ''
    #tradeObject = messageprocess.processMessage(message)
    tradeObj = {'Curr': 'CHZ ', 'TP': ['0.2885', '0.2887'], 'SL': '0.2785', 'entry': ['0.2880 ', ' 0.2788'], 'side': 'buy',
     'size': 34, 'avgEntry': 0.2871}

    #{'Curr': 'KAVA ', 'TP': ['1.4483', '1.4625', '1.4770', '1.5056', '1.5486'], 'SL': '1.3598',
    # 'entry': ['1.4340 ', ' 1.4000'], 'side': 'buy'}
    client_trade = kc.kcscalls('params')
    trade_pair = tradeObj['Curr'].strip() + 'USDTM'
    response = client_trade.get_position_details(trade_pair)
    open_position = response['isOpen']
    TradeManager = TM.TradeManager(tradeObj, client_trade)
    if not open_position:
        print(f"******Entry Message Processed from telegram: {tradeObj}******")

        opened_position_order_details, tradeObject_with_more_details = EntryManager.tradeCallToKCS(tradeObj)
        print(f'opened_position_order_details: {opened_position_order_details}')
        # opened_position_order = ''
        cos.checkOrderStatus(opened_position_order_details['orderId'], tradeObj)

    tp_arr = tradeObj['TP']
    sl = tradeObj['SL']
    arr_index_len = len(tp_arr)
    time.sleep(5)
    for i in range(arr_index_len):
        tp_order_id, sl_order_id = TradeManager.manage_trade(tp_arr[i],i)
        print(f'TP orderid: {tp_order_id}, SL orderid: {sl_order_id}')
        what_hit = cos.checkOrderStatusWithSL(tp_order_id['orderId'],sl_order_id['orderId'],tradeObj)
        print(what_hit)
        if what_hit == 'sl':
            break

    print('finished')

    #print(opened_position_order)
    #TradeManager = TM.TradeManager(tradeObj, client_trade)

    '''
    #calling entryManager - working
    
    opened_position_order, stop_loss_order, tradeObject_with_more_details = EntryManager.tradeCallToKCS(tradeObj)
    print(opened_position_order)
    time.sleep(2)
    
    
    #Entry manager entry trigger check loop
    
    opened_position_order = '6363209d3cf0b000011714a7'
    while True:
        orderDetails = client_trade.checkLimitOrderStatus(opened_position_order['orderId'])
        print(orderDetails)
        status = orderDetails['status']
        if (status == 'done'):
            print('Horrrrr')
        else:
            print(status)
            time.sleep(10)
    
    #working code for trade manager
    
    TradeManager = TM.TradeManager(tradeObj,client_trade)
    TradeManager.manage_trade()

    '''


