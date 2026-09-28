import unittest
from src.agent import SovereignTradingAgent
from src.paper_portfolio import PaperPortfolio

class TestConfluenceEngine(unittest.TestCase):
    def setUp(self):
        self.agent = SovereignTradingAgent()
        self.portfolio = PaperPortfolio(initial_balance_usd=1000.0)

    def test_tier_1_high_conviction(self):
        """Metrics with strong volume, high buy pressure, and velocity should achieve Tier 1."""
        strong_metrics = {
            "symbol": "SOL",
            "price_usd": 120.0,
            "volume_multiplier": 1.85, # Pass (>=1.35)
            "volume_1h": 15000000.0,
            "buy_pressure_pct": 62.0,   # Pass (>=53.0)
            "buys_1h": 320,
            "sells_1h": 190,
            "price_change_5m": 0.35,   # Pass (>=0.02)
            "price_change_1h": 1.20,
            "range_position_pct": 32.0, # Pass (<=40.0 discount zone)
            "timestamp": 1727550000,
            "readable_time": "12:00:00 UTC"
        }
        setup = self.agent.analyze_token_setup(strong_metrics)
        self.assertGreaterEqual(setup["confluence_score"], 4)
        self.assertEqual(setup["tier_level"], 1)
        self.assertEqual(setup["action"], "BUY")
        self.assertEqual(setup["allocation_usd"], 100.0)
        self.assertIsNotNone(setup["callout_id"])

        # Test portfolio opens full $100 position
        res = self.portfolio.open_paper_trade(setup)
        self.assertEqual(res["status"], "OPENED")
        self.assertEqual(res["position"]["size_usd"], 100.0)

    def test_tier_2_tactical_scalp(self):
        """Metrics qualifying exactly 3 confluences should achieve Tier 2 Tactical Scalp."""
        tactical_metrics = {
            "symbol": "JUP",
            "price_usd": 0.35,
            "volume_multiplier": 1.45, # Pass (>=1.35) [1]
            "volume_1h": 500000.0,
            "buy_pressure_pct": 55.0,   # Pass (>=53.0) [2]
            "buys_1h": 110,
            "sells_1h": 90,
            "price_change_5m": -0.05,  # Fail (<0.02)
            "price_change_1h": -0.10,
            "range_position_pct": 55.0, # Fail (Mid range)
            "timestamp": 1727550000,
            "readable_time": "12:00:00 UTC"
        } # Plus R:R is always Pass [3] => Total 3 confluences
        setup = self.agent.analyze_token_setup(tactical_metrics)
        self.assertEqual(setup["confluence_score"], 3)
        self.assertEqual(setup["tier_level"], 2)
        self.assertEqual(setup["allocation_usd"], 50.0)
        self.assertIn("TACTICAL", setup["tier"])

        # Test portfolio opens half $50 position
        res = self.portfolio.open_paper_trade(setup)
        self.assertEqual(res["status"], "OPENED")
        self.assertEqual(res["position"]["size_usd"], 50.0)

    def test_tier_3_hard_pass(self):
        """Weak metrics with only 1 or 2 confluences must trigger Hard Pass (No Trade)."""
        weak_metrics = {
            "symbol": "BONK",
            "price_usd": 0.0000035,
            "volume_multiplier": 0.70, # Fail (<1.35)
            "volume_1h": 20000.0,
            "buy_pressure_pct": 44.0,   # Fail (<53.0)
            "buys_1h": 40,
            "sells_1h": 51,
            "price_change_5m": -0.40,  # Fail
            "price_change_1h": -1.20,
            "range_position_pct": 52.0, # Fail
            "timestamp": 1727550000,
            "readable_time": "12:00:00 UTC"
        }
        setup = self.agent.analyze_token_setup(weak_metrics)
        self.assertLess(setup["confluence_score"], 3)
        self.assertEqual(setup["tier_level"], 3)
        self.assertEqual(setup["action"], "HOLD / PRESERVE CAPITAL")
        self.assertIsNone(setup["callout_id"])
        self.assertEqual(setup["allocation_usd"], 0.0)

if __name__ == "__main__":
    unittest.main()
