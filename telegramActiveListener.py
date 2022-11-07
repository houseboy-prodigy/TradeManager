import configparser
import json
import re
import time
import string as str
from kucoin_futures.client import Trade
from telethon.errors import SessionPasswordNeededError
from telethon import TelegramClient, events, sync
from telethon.tl.functions.messages import (GetHistoryRequest)
from kucoin_futures.client import Market
import threading
import messageProcess
import controlCenter
from telethon.tl.types import (
    PeerChannel
)
import ReturnValueThready

from telethon import TelegramClient

'''
api_id = 12223282
api_hash = 'dd27c92671e9b82b788c8b7d93716032'

client = TelegramClient('anon3', api_id, api_hash)
user_input_channel = 'https://t.me/autotrigger'
async def sendMessage(message):
    # Now you can use all client methods listed below, like for example...
    await client.send_message(user_input_channel, message)

with client:
    client.loop.run_until_complete(sendMessage('bye'))

'''

api_id = 12223282
api_hash = 'dd27c92671e9b82b788c8b7d93716032'

client = TelegramClient('anon3', api_id, api_hash)

# Here you define the target channel that you want to listen to:
#user_input_channel = 'https://t.me/autotrigger'
user_input_channel = 'https://t.me/scratchactivework'
async def sendMessage(message):
    # Now you can use all client methods listed below, like for example...
    await client.send_message(user_input_channel, message)

def validateMessage(message):
    lines = message.splitlines()
    first_line = lines[0]
    if(first_line.startswith('HIGH')):
        return True
    else:
        return False
def runProcess(message):
    while True:
        print(message)
        time.sleep(3)
@client.on(events.NewMessage(chats=user_input_channel))
async def NewMessageListener(event):
    message = event.message.message
    message_validated = validateMessage(message)
    if not message_validated:
        print('wrong Message, only post signals')
    else:
        try:
            await sendMessage('got a valid trade message....starting EntryDreamerBot')
            #adding multithreading -
            thread1 = ReturnValueThready.ReturnValueThread(target=controlCenter.dreamerEntryBot, args=(message,))
            #thread = threading.Thread(target=controlCenter.dreamerEntryBot, args=(message,))
            thread1.start()
            entered_trade_tradeObj = thread1.join()
            print(f'TradeObject after entry phase {entered_trade_tradeObj}')
            #add entry details by returning entry bot

            curr = entered_trade_tradeObj['Curr']

            entered_trade_tradeObj = {'Curr': 'MATIC ', 'TP': ['1.299','1.367'], 'SL': '1.130', 'entry': ['0.2880 ', ' 0.2788'],
                                  'side': 'buy',
                                  'size': 2, 'avgEntry': 1.2450}
            entry = entered_trade_tradeObj['avgEntry']
            tp_hit_arr = []
            if(entry == 'empty'):
                await sendMessage(f'Trade already entered')
            else:
                await sendMessage(f'completed entry phase, avgEntry at {entry} for {curr}')
                await sendMessage('starting TradeManagerDreamerBot')
                tp_arr = entered_trade_tradeObj['TP']
                arr_index_len = len(tp_arr)
                for i in range(arr_index_len):
                    thread2 = ReturnValueThready.ReturnValueThread(target=controlCenter.dreamerTradeManagerBot, args=(entered_trade_tradeObj,i,))
                    thread2.start()
                    tradeObjAfterTrades = thread2.join()
                    sl_order_id = tradeObjAfterTrades['sl_order_id']
                    print(f'TradeObject in trade phase {i+1}{tradeObjAfterTrades}')
                    what_hit = tradeObjAfterTrades['hit']
                    if what_hit == 'sl':
                        entered_trade_tradeObj['sl_hit_id'] = sl_order_id
                        await sendMessage(f'completed trade phase hit: {what_hit}')
                        break
                    else:
                        #cancel order_using_sl_order_id
                        print('at tp in tradephase')
                        tp_hit_arr.append(tradeObjAfterTrades['tp_order_id'])
                        print(tp_hit_arr)
                        await sendMessage(f'completed trade phase hit: {what_hit}{i+1}')

                entered_trade_tradeObj['tps_hit_id'] = tp_hit_arr
                print(f'TradeObject after trade phase {entered_trade_tradeObj}')
                await sendMessage(f'completed trade phase for {curr}')
        except Exception as e:
            print(e)
            await sendMessage(f'got some error')



with client:
    client.run_until_disconnected()
