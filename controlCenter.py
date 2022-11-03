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


#sample tradeObj = {'Curr': 'XRP ', 'TP': ['0.4640', '0.4594', '0.4546', '0.4476', '0.4406', '0.4313'], 'SL': '0.4920', 'entry': ['0.4688 ', ' 0.4780'], 'side': 'sell'}
if __name__ == "__main__":
    message = ''
    #tradeObject = messageprocess.processMessage(message)
    tradeObj = {'Curr': 'XRP ', 'TP': ['0.4557', '0.4594', '0.4546', '0.4476', '0.4406', '0.4313'],
                'SL': '0.4300', 'entry': ['0.4535 ', ' 0.4341'], 'side': 'buy'}
    client_trade = kc.kcscalls('params')
    TradeManager = TM.TradeManager(tradeObj, client_trade)

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


