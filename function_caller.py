import sys
import json
from dbOps import getTrade, testFunction, putTradeintoDB
from controlCenter import dreamerEntryBotManual


def getTradeObj(curr, entry, tp, sl, side):
    # Your function implementation here
    tradeObj = {
        'Curr': curr,
        'TP': tp.split(','),
        'SL': sl,
        'entry': entry.split(','),
        'side': side
    }
    return tradeObj

try:
    function_name = sys.argv[1]
    args = sys.argv[2:]

    # Call the appropriate function based on the function name
    if function_name == 'get':
        result = getTrade(*args)
    elif function_name == 'get1':
        result = testFunction(*args)
    elif function_name == 'put':
        result = putTradeintoDB(*args)
    elif function_name == 'entry':
        tradeObj = getTradeObj(*args)
        result = dreamerEntryBotManual(tradeObj)
    # Add more conditions for other functions

    print(json.dumps(result))

except Exception as e:
    print(e)
