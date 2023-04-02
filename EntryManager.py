import configparser
import json
import re
import time
import string as str
import kcsCalls as kc
from telethon.errors import SessionPasswordNeededError
from telethon import TelegramClient, events, sync
from telethon.tl.functions.messages import (GetHistoryRequest)
import messageProcess
import asyncio
from telethon.tl.types import (
PeerChannel
)

from telethon import TelegramClient

#params = {'stop': 'down', 'stopPrice': 0.22 , 'stopPriceType': 'TP'}

client_trade = kc.kcscalls('params')

def checkLimitOrderStatus(order_id,stop_loss_id):
    details = client_trade.get_order_details(order_id)
    sldetails = client_trade.get_order_details(stop_loss_id)
    if(details['status'] == 'done'):
        return 'order_executed'
    elif(sldetails['status'] == 'done'):
        return 'sl_triggered'
    else:
        return 'order_pending'

def trade_side_reverse(side):
    return 'buy' if side == 'sell' else 'sell'

def tradeCallToKCS(tradeObj):
    #URL -  change for Sanbox/Real
   
    trade_pair = tradeObj['Curr'].strip() + 'USDTM'
    trade_side = tradeObj['side']
    stop_loss = tradeObj['SL']
    trade_leverage = 1
    entryArr = tradeObj['entry']
    entryUpper = entryArr[0]
    entryLower = entryArr[1]
    #entryUpper = float(entryArr[0].replace(',',''))
    #entryLower = float(entryArr[1].replace(',',''))
    price_data = client_trade.getPriceData(trade_pair)
    price = float(price_data['price'])
    contract_detail = client_trade.get_contract_detail(trade_pair)
    multiplier = contract_detail['multiplier']
    #print(trade_pair)
    #print(entryUpper)
    #print(entryLower)

    '''
    Got all contract details begin trading and while true loop until entry trade done
    '''
    order_id = ''
    stop_order_id = ''
    # or connect to Sandbox
    # client = Trade(api_key, api_secret, api_passphrase, is_sandbox=True)
    #print(f'price: {price}, entryLower: {entryLower}, entryUpper: {entryUpper}' )
    cost_of_one_lot = multiplier * price
    #print(multiplier)
    #print(cost_of_one_lot)
    dollar_per_trade = 10
    lot_quantity = int(dollar_per_trade/cost_of_one_lot)
    params = {'leverage': trade_leverage, 'stop': 'loss', 'stopPrice': stop_loss , 'stopPriceType': 'TP'}
    #print(lot_quantity)
    if(trade_side == 'buy'):
        if(price >= entryLower and price<= entryUpper):  #case where current price is between than the entries,  enter at current market price

            order_id = client_trade.create_limit_order(trade_pair, trade_side, trade_leverage, lot_quantity, price)
            #add stop order
            #print(order_id)
            #print('Order Confirmed,scenario1b')

        elif(price<=entryLower): #case where current price is less than the LowerEntry enter at current market price
            order_id = client_trade.create_limit_order(trade_pair, trade_side, trade_leverage, lot_quantity, price)
            #add stop order
            #print(order_id)
            #print('Order Confirmed,scenario2b')
            
        else: #case where current price is more than the HigherEntry, wait for entry place the limit order for upper entry
            order_id = client_trade.create_limit_order(trade_pair, trade_side, trade_leverage, lot_quantity, entryUpper)
            #add stop order
            #print(order_id)
            #print('Order Confirmed,scenario3b')
        #stop_order_id = client_trade.create_limit_order(trade_pair, trade_side_reverse(trade_side), trade_leverage, lot_quantity, stop_loss)

    elif(trade_side == 'sell'):
        if(price <= entryLower and price>= entryUpper):#case where current price is between than the entries,  enter at current market price

            order_id = client_trade.create_limit_order(trade_pair, trade_side, trade_leverage, lot_quantity, price)
            #print(order_id)

            #print('Order Confirmed,scenario1s')
        elif(price <= entryUpper):#case where current price is below the lowerentry(upperEntry=lowerEntry in short case),
            # enter at upperentry price
            order_id = client_trade.create_limit_order(trade_pair, trade_side, trade_leverage, lot_quantity, entryUpper)
            #print('Order Confirmed,scenario2s')
        else:#case where current price is
            order_id = client_trade.create_limit_order(trade_pair, trade_side, trade_leverage, lot_quantity, price)
            #print('Order Confirmed,scenario3s')
        params = {'stop': 'loss', 'stopPrice': 1500 , 'stopPriceType': 'TP'}
        #stop_order_id = client_trade.create_stop_order(trade_pair, trade_side, trade_leverage, lot_quantity, price,params)
        stop_order_id = 'helo'
    tradeObj['size'] = lot_quantity
    return order_id,tradeObj

if __name__ == '__main__':
    print('')
    #demoTradeCalls();
    #client_trade.cancel_order('63128de241a533000104a462')
    #print(client_trade.get_position_details('ADAUSDTM'))
    #client_trade = kc.kcscalls(params)
    #print(client_trade.getPriceData('ADAUSDTM'))