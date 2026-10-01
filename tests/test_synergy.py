import unittest
from src.argus_shield import ArgusSecurityShield
from src.blink_generator import BlinkCraftBridge
from src.oraclex_hedge import OracleXHedgingEngine
from src.copilot import SovereignCopilot
from src.market_data import MarketDataFeed
from src.agent import SovereignTradingAgent
from src.policy_engine import DeterministicPolicyWall
from src.paper_portfolio import PaperPortfolio

class TestSynergyModules(unittest.TestCase):
    def setUp(self):
        self.shield = ArgusSecurityShield()
        self.blink_bridge = BlinkCraftBridge()
        self.hedge_engine = OracleXHedgingEngine()
        self.feed = MarketDataFeed()
        self.agent = SovereignTradingAgent()
        self.policy = DeterministicPolicyWall()
        self.portfolio = PaperPortfolio()
        self.copilot = SovereignCopilot(
            agent=self.agent,
            feed=self.feed,
            portfolio=self.portfolio,
            policy=self.policy,
            shield=self.shield,
            blink_bridge=self.blink_bridge,
            hedge_engine=self.hedge_engine
        )

    def test_argus_shield_audit_verified_tokens(self):
        """Verifies Argus shield audits known Solana tokens accurately."""
        audit = self.shield.audit_token("SOL")
        self.assertTrue(audit["passed"])
        self.assertEqual(audit["safety_score"], 99)
        self.assertTrue(audit["freeze_authority_revoked"])
        self.assertFalse(audit["honeypot_detected"])

    def test_argus_shield_pre_flight_safety(self):
        """Pre-flight check returns safe=True for approved token."""
        is_safe, reason, audit = self.shield.verify_pre_trade_safety("JUP")
        self.assertTrue(is_safe)
        self.assertIn("ARGUS SHIELD CLEARED", reason)

    def test_blink_generator_dial_to_link(self):
        """Verifies BlinkCraft bridge generates Dialect action and dial.to link."""
        signal = {
            "symbol": "SOL",
            "entry_price_usd": 150.0,
            "target_price_usd": 165.0,
            "stop_loss_usd": 140.0,
            "score": 5
        }
        blink = self.blink_bridge.generate_trade_blink(signal)
        self.assertIn("https://dial.to/?action=solana-action:", blink["blink_url"])
        self.assertIn("$SOL", blink["title"])
        self.assertEqual(len(blink["actions"]), 3)

    def test_oraclex_hedge_engine(self):
        """Verifies OracleX hedge engine evaluates portfolio risk."""
        mock_summary = {"total_exposure_usd": 300.0, "open_positions_count": 2}
        hedge = self.hedge_engine.evaluate_portfolio_hedge(mock_summary)
        self.assertEqual(hedge["status"], "ACTIVE_RECOMMENDATION")
        self.assertGreater(hedge["recommended_hedge_usd"], 0)
        self.assertGreaterEqual(len(hedge["hedge_contracts"]), 1)

    def test_copilot_slash_commands(self):
        """Verifies Conversational Co-Pilot routes slash commands properly."""
        # /help
        help_resp = self.copilot.handle_message("/help")
        self.assertEqual(help_resp["action_type"], "HELP")
        self.assertIn("Sovereign Agent Co-Pilot", help_resp["reply"])

        # /audit
        audit_resp = self.copilot.handle_message("/audit SOL")
        self.assertEqual(audit_resp["action_type"], "AUDIT_RESULT")
        self.assertIn("Argus Pre-Flight Security Audit", audit_resp["reply"])

        # /portfolio
        port_resp = self.copilot.handle_message("/portfolio")
        self.assertEqual(port_resp["action_type"], "PORTFOLIO_SUMMARY")
        self.assertIn("Virtual Bankroll", port_resp["reply"])

if __name__ == "__main__":
    unittest.main()
