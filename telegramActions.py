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
import asyncio
import messageProcess
import controlCenter
import ReturnValueThready

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
    await sendMessage('got a message')
    # adding multithreading -
    #thread = threading.Thread(target=afterMessage, args=(message,))
    asyncio.create_task(afterMessage(message))

    # controlCenter.dreamerBot(message)


async def afterMessage(messagee):
    print('afterMessage Starting')
    tradeObjAfterTrades = await (thirdFunc(messagee))

    print(tradeObjAfterTrades)

async def thirdFunc(mess):
    val = 0
    while val == 0:
        print(f'gonna sleep for 30sec, {mess}')
        time.sleep(30)
        val = 1
        print('done sleeping')
    return (f'{mess} came from thridfunc')


with client:
    client.run_until_disconnected()
