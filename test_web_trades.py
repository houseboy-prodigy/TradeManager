import unittest

import web_trades


class NormalizeTradeTest(unittest.TestCase):
    def test_derives_buy_side_and_maps_btc(self):
        trade = web_trades.normalize_trade(
            {
                "curr": "btc/usd",
                "entry": ["64000", "63500"],
                "tp": ["65000", "66000"],
                "sl": "62000",
            }
        )
        self.assertEqual(trade["curr"], "XBT")
        self.assertEqual(trade["side"], "buy")
        self.assertEqual(trade["entry"], [64000.0, 63500.0])

    def test_derives_sell_side_when_targets_fall(self):
        trade = web_trades.normalize_trade(
            {
                "curr": "ETH",
                "entry": [2500, 2480],
                "tp": [2450, 2400],
                "sl": 2550,
            }
        )
        self.assertEqual(trade["side"], "sell")

    def test_parse_signal_matches_telegram_sample(self):
        message = "ETH/USD\nEntry Zone:\n4120 - 4135\nDCA if price\n\nTP1: 4150\nTP2: 4250\nTP3: 4400\nSL: 3988"
        trade = web_trades.parse_signal(message)
        self.assertEqual(trade["curr"], "ETH")
        self.assertEqual(trade["entry"], [4120.0, 4135.0])
        self.assertEqual(trade["tp"], [4150.0, 4250.0, 4400.0])
        self.assertEqual(trade["sl"], 3988.0)
        self.assertEqual(trade["side"], "buy")

    def test_rejects_a_single_target(self):
        with self.assertRaises(ValueError):
            web_trades.normalize_trade(
                {"curr": "ETH", "entry": [1, 2], "tp": [3], "sl": 0.5}
            )


if __name__ == "__main__":
    unittest.main()
