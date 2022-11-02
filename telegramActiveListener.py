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
import curr_price_data
import messageprocess
import Enter_trade
import Trade_manager
from telethon.tl.types import (
PeerChannel
)

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
user_input_channel = 'https://t.me/autotrigger'

@client.on(events.NewMessage(chats=user_input_channel))
async def NewMessageListener(event):
	message = event.message.message
	tradeObj = messageprocess.processMessage(message)
	print(tradeObj)
	opened_position_order,stop_loss_order,tradeObject_with_more_details = Enter_trade.tradeCallToKCS(tradeObj)
	(print(opened_position_order,stop_loss_order,tradeObject_with_more_details))
	'''
	while True:
		status = Enter_trade.checkLimitOrderStatus(opened_position_order,stop_loss_order)
		if(status == 'order_executed'):
			tradeMan1 = Trade_manager.TradeManager(tradeObject_with_more_details)
		elif(status == 'sl_triggered'):
			break
		else:
			time.sleep(10)
	'''
	
with client:
	client.run_until_disconnected()
