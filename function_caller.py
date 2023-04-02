import sys
import json
from dbOps import getTrade, testFunction, putTrad, getAllTrades
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
    elif function_name == 'getAllTrades':
        result = getAllTrades()
    elif function_name == 'put':
        # Parse the JSON strings for the 'entry' and 'TP' arrays
        entry_string = args[1]
        tp_string = args[2]

        print('entry_string:', entry_string)
        print('tp_string:', tp_string)

        try:
            entry = json.loads(entry_string)
        except json.JSONDecodeError:
            entry = []

        try:
            tp = json.loads(tp_string)
        except json.JSONDecodeError:
            tp = []

        print('entry:', entry)
        print('tp:', tp)

        # Replace the JSON strings in the 'args' list with the parsed arrays
        args[1] = entry
        args[2] = tp

        result = putTrad(*args)
    elif function_name == 'entry':
        tradeObj = getTradeObj(*args)
        result = dreamerEntryBotManual(tradeObj)
    # Add more conditions for other functions

    print(json.dumps(result))

except Exception as e:
    print(e)
