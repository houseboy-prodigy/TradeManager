import configparser
import json
import re
import time
from kucoin_futures.client import Trade
from telethon.errors import SessionPasswordNeededError
from telethon import TelegramClient, events, sync
from telethon.tl.functions.messages import (GetHistoryRequest)
from kucoin_futures.client import Market
import messageprocess
import EntryManager
import TradeManager as TM
import kcscalls as kc
import checkOrderStatus as cos

def dreamerEntryBot(message):
    tradeObj = messageprocess.processMessage(message)
    print(f"******Message Processed from telegram: {tradeObj}******")

    client_trade = kc.kcscalls('params')
    TradeManager = TM.TradeManager(tradeObj, client_trade)

    opened_position_order_details, tradeObject_with_more_details = EntryManager.tradeCallToKCS(tradeObj)
    print(f'opened_position_order_details: {opened_position_order_details}')
    #opened_position_order = ''
    cos.checkOrderStatus(opened_position_order_details['orderId'],tradeObj)
    trade_pair = tradeObj['Curr'].strip() + 'USDTM'
    tp_arr = tradeObj['TP']
    sl = tradeObj['SL']
    arr_index_len = len(tp_arr) - 1
    for i in range(2):
        tp_order_id, sl_order_id = TradeManager.manage_trade(tp_arr[i],i)
        print(f'TP orderid: {tp_order_id}, SL orderid: {sl_order_id}')
        what_hit = cos.checkOrderStatusWithSL(tp_order_id['orderId'], sl_order_id['orderId'], tradeObj)
        print(what_hit)
        if what_hit == 'sl':
            break

    print(f'Dreamer bot done! details of position:{client_trade.get_position_details(trade_pair)}')

def dreamerTradeManagerBot(message):
    print(f"******Message Processed from telegram: {tradeObj}******")

#sample tradeObj = {'Curr': 'XRP ', 'TP': ['0.4640', '0.4594', '0.4546', '0.4476', '0.4406', '0.4313'], 'SL': '0.4920', 'entry': ['0.4688 ', ' 0.4780'], 'side': 'sell'}
#tradeObj2 = {'Curr': 'ADA ', 'TP': ['0.4121', '0.4594', '0.4546', '0.4476', '0.4406', '0.4313'],'SL': '0.34', 'entry': ['0.3912 ', ' 0.3800'], 'side': 'buy'}
if __name__ == "__main__":
    message = ''
    #tradeObject = messageprocess.processMessage(message)
    tradeObj = {'Curr': 'XRP ', 'TP': ['0.4570', '0.4578', '0.4546', '0.4476', '0.4406', '0.4313'],
                'SL': '0.4560', 'entry': ['0.4565 ', ' 0.4441'], 'side': 'buy', 'size': 2}

    client_trade = kc.kcscalls('params')
    TradeManager = TM.TradeManager(tradeObj, client_trade)

    #opened_position_order_details, tradeObject_with_more_details = EntryManager.tradeCallToKCS(tradeObj)
    #print(f'opened_position_order_details: {opened_position_order_details}')

    #opened_position_order = opened_position_order_details['orderId']
    #time.sleep(5)
    #opened_position_order = ''
    #cos.checkOrderStatus(opened_position_order,tradeObj)
    tp_arr = tradeObj['TP']
    sl = tradeObj['SL']
    #arr_index_len = len(tp_arr) - 1
    for i in range(1):
        tp_order_id, sl_order_id = TradeManager.manage_trade(tp_arr[1],1)
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


