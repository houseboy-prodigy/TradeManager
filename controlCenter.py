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
import messageprocess
import EntryManager
import TradeManager


#sample tradeObj = {'Curr': 'XRP ', 'TP': ['0.4640', '0.4594', '0.4546', '0.4476', '0.4406', '0.4313'], 'SL': '0.4920', 'entry': ['0.4688 ', ' 0.4780'], 'side': 'sell'}
if __name__ == "__main__":
    message = ''
    #tradeObject = messageprocess.processMessage(message)
    tradeObj = {'Curr': 'XRP ', 'TP': ['0.4640', '0.4594', '0.4546', '0.4476', '0.4406', '0.4313'], 
                'SL': '0.4920', 'entry': ['0.4688 ', ' 0.4780'], 'side': 'sell'}
    



