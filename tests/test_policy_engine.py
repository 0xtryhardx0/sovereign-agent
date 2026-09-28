import unittest
from config import VERIFIED_TOKEN_MINTS, RISK_POLICY
from src.policy_engine import DeterministicPolicyWall

class TestDeterministicPolicyWall(unittest.TestCase):
    def setUp(self):
        # 10,000 USD portfolio for tests
        self.policy = DeterministicPolicyWall(initial_portfolio_usd=10000.0)

    def test_valid_trade_approval(self):
        """A normal trade within all limits should pass."""
        valid_proposal = {
            "input_mint": VERIFIED_TOKEN_MINTS["SOL"],
            "output_mint": VERIFIED_TOKEN_MINTS["USDC"],
            "amount_sol": 0.5,
            "estimated_usd_value": 72.50, # Well below 5% of 10k ($500)
            "slippage_bps": 50,
        }
        is_valid, reason = self.policy.validate_proposed_trade(valid_proposal)
        self.assertTrue(is_valid)
        self.assertIn("PASSED", reason)

    def test_reject_unverified_token(self):
        """Trades with unverified honeypot tokens must be rejected."""
        honeypot_proposal = {
            "input_mint": VERIFIED_TOKEN_MINTS["SOL"],
            "output_mint": "ScamTokenMint11111111111111111111111111111",
            "amount_sol": 0.5,
            "estimated_usd_value": 70.0,
            "slippage_bps": 50,
        }
        is_valid, reason = self.policy.validate_proposed_trade(honeypot_proposal)
        self.assertFalse(is_valid)
        self.assertIn("not in the verified allowlist", reason)

    def test_reject_excessive_trade_amount(self):
        """Trade amount exceeding max_trade_sol cap must be blocked."""
        excessive_proposal = {
            "input_mint": VERIFIED_TOKEN_MINTS["SOL"],
            "output_mint": VERIFIED_TOKEN_MINTS["USDC"],
            "amount_sol": 2.5, # Exceeds 1.0 SOL cap
            "estimated_usd_value": 360.0,
            "slippage_bps": 50,
        }
        is_valid, reason = self.policy.validate_proposed_trade(excessive_proposal)
        self.assertFalse(is_valid)
        self.assertIn("exceeds max trade cap", reason)

    def test_reject_excessive_portfolio_percentage(self):
        """Trade exceeding max portfolio allocation percentage must be blocked."""
        # Create smaller portfolio of $1,000 where 5% is $50
        small_policy = DeterministicPolicyWall(initial_portfolio_usd=1000.0)
        large_proposal = {
            "input_mint": VERIFIED_TOKEN_MINTS["SOL"],
            "output_mint": VERIFIED_TOKEN_MINTS["USDC"],
            "amount_sol": 0.8,
            "estimated_usd_value": 116.0, # Exceeds 5% ($50)
            "slippage_bps": 50,
        }
        is_valid, reason = small_policy.validate_proposed_trade(large_proposal)
        self.assertFalse(is_valid)
        self.assertIn("portfolio cap", reason)

    def test_reject_excessive_slippage(self):
        """Slippage exceeding maximum bps must be blocked."""
        high_slippage_proposal = {
            "input_mint": VERIFIED_TOKEN_MINTS["SOL"],
            "output_mint": VERIFIED_TOKEN_MINTS["USDC"],
            "amount_sol": 0.5,
            "estimated_usd_value": 70.0,
            "slippage_bps": 300, # 3.0% exceeds 1.5% (150 bps)
        }
        is_valid, reason = self.policy.validate_proposed_trade(high_slippage_proposal)
        self.assertFalse(is_valid)
        self.assertIn("exceeds maximum allowable", reason)

    def test_circuit_breaker(self):
        """If drawdown exceeds allowable daily limit, circuit breaker triggers."""
        # Drop portfolio from 10,000 to 9,000 (10% loss > 8% limit)
        self.policy.current_portfolio_usd = 9000.0
        proposal = {
            "input_mint": VERIFIED_TOKEN_MINTS["SOL"],
            "output_mint": VERIFIED_TOKEN_MINTS["USDC"],
            "amount_sol": 0.1,
            "estimated_usd_value": 14.50,
            "slippage_bps": 50,
        }
        is_valid, reason = self.policy.validate_proposed_trade(proposal)
        self.assertFalse(is_valid)
        self.assertIn("CIRCUIT BREAKER TRIGGERED", reason)

if __name__ == "__main__":
    unittest.main()
