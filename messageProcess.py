# from kcstraderest import testFileConncetion

def processMessage(message):
    tradeObj = {}
    # check for message relevace
    substrings = ['TP1', 'TP2', 'TP3', 'TP4']
    tpArr = []
    crypy = ""
    splitMessage = message.splitlines()
    entryFlag = False
    for element in splitMessage:

        if entryFlag:
            entryString = element.partition('-')
            range_entry = [entryString[0], entryString[2]]
            entryFlag = False
        # print(element)
        if "/" in element:
            strArr = element.partition('/')
            crypy = strArr[0]
        # print(f'trading pair is {crypy}.')
        if "Entry" in element:
            entryFlag = True

        if "TP" in element:
            tpString = element.partition(':')
            tpPrice = tpString[2]
            tpArr.append(tpPrice.strip())
        if "SL" in element:
            slString = element.partition(':')
            sl = slString[2].strip()
    if 'BTC' in crypy:
        crypy = 'XBT'
    tradeObj['Curr'] = crypy
    tradeObj['TP'] = tpArr
    tradeObj['SL'] = sl

    long_short = ''
    tp_diff = float(tpArr[0].replace(',', '')) - float(tpArr[1].replace(',', ''))
    #print(tp_diff)
    if tp_diff < 0:
        long_short = 'buy'
    else:
        long_short = 'sell'

    tradeObj['entry'] = range_entry
    tradeObj['side'] = long_short
    #print(tradeObj)
    return tradeObj


if __name__ == '__main__':
    messages1 = "ETH/USD\nEntry Zone:\n4120 - 4135\nDCA if price\n\nTP1: 4150\nTP2: 4250\nTP3: 4400\nSL: 3988"

    processedMsg = processMessage(messages1)
# print(processedMsg)
# testFileConncetion(processedMsg)
