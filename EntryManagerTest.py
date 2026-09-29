import EntryManager
import unittest


def buy_sell_scenarios(trade_side, tradeObj):
    trade_pair = tradeObj['Curr'].strip() + 'USDTM'
    trade_side = tradeObj['side']
    stop_loss = tradeObj['SL']
    trade_leverage = 1
    entryArr = tradeObj['entry']
    entryUpper = float(entryArr[0].replace(',', ''))
    entryLower = float(entryArr[1].replace(',', ''))
    price_data = client_trade.getPriceData(trade_pair)
    price = float(price_data['price'])
    contract_detail = client_trade.get_contract_detail(trade_pair)
    multiplier = contract_detail['multiplier']
    print(trade_pair)
    print(entryUpper)
    print(entryLower)
    order_id = ''

    print(f'price: {price}, entryLower: {entryLower}, entryUpper: {entryUpper}')
    cost_of_one_lot = multiplier * price
    print(multiplier)
    print(cost_of_one_lot)
    dollar_per_trade = 10
    lot_quantity = int(dollar_per_trade / cost_of_one_lot)
    params = {'leverage': trade_leverage, 'stop': 'loss', 'stopPrice': stop_loss, 'stopPriceType': 'TP'}
    print(lot_quantity)
    if (trade_side == 'buy'):
        if (price >= entryLower and price <= entryUpper):

            order_id = client_trade.create_limit_order(trade_pair, trade_side, trade_leverage, lot_quantity, price)
            # add stop order
            print(order_id)
            print('Order Confirmed,scenario1b')

        elif (price <= entryLower):
            order_id = client_trade.create_limit_order(trade_pair, trade_side, trade_leverage, lot_quantity, price)
            # add stop order
            print(order_id)
            print('Order Confirmed,scenario2b')

        else:
            order_id = client_trade.create_limit_order(trade_pair, trade_side, trade_leverage, lot_quantity, entryUpper)
            # add stop order
            print(order_id)
            print('Order Confirmed,scenario3b')
        # stop_order_id = client_trade.create_limit_order(trade_pair, trade_side_reverse(trade_side), trade_leverage, lot_quantity, stop_loss)

    elif (trade_side == 'sell'):
        if (price <= entryLower and price >= entryUpper):

            order_id = client_trade.create_limit_order(trade_pair, trade_side, trade_leverage, lot_quantity, price)
            print(order_id)

            print('Order Confirmed,scenario1s')
        elif (price <= entryLower):
            order_id = client_trade.create_limit_order(trade_pair, trade_side, trade_leverage, lot_quantity, entryLower)
            print('Order Confirmed,scenario2s')
        else:
            order_id = client_trade.create_limit_order(trade_pair, trade_side, trade_leverage, lot_quantity, price)
            print('Order Confirmed,scenario3s')
        params = {'stop': 'loss', 'stopPrice': 1500, 'stopPriceType': 'TP'}
        # stop_order_id = client_trade.create_stop_order(trade_pair, trade_side, trade_leverage, lot_quantity, price,params)
        stop_order_id = 'helo'
    tradeObj['size'] = lot_quantity
    return order_id, tradeObj

class Test(unittest.TestCase):
    def test_entry_order_id_params(self):
        actual = EntryManager.tradeCallToKCS(tradeObj={'Curr': 'XRP ', 'TP': ['0.4570', '0.4578', '0.4546', '0.4476', '0.4406', '0.4313'],
                'SL': '0.4560', 'entry': ['0.4565 ', ' 0.4441'], 'side': 'buy', 'size': 2})
        expected = {"tank_a": ["shark", "tuna"]}
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
