import time
from typing import Tuple, Dict, Any
from config import RISK_POLICY

class PolicyViolationError(Exception):
    """Raised when a proposed trade violates hard risk limits."""
    pass

class DeterministicPolicyWall:
    """
    Deterministic Policy Wall enforcing strict safety boundaries.
    The AI model can propose any action, but the policy wall alone
    decides whether the action is permitted to execute on-chain.
    """
    def __init__(self, initial_portfolio_usd: float = 1000.0):
        self.initial_portfolio_usd = initial_portfolio_usd
        self.current_portfolio_usd = initial_portfolio_usd
        self.daily_high_watermark_usd = initial_portfolio_usd
        self.last_trade_timestamp = 0.0
        self.daily_trades_count = 0
        self.is_circuit_breaker_active = False

    def check_circuit_breaker(self) -> Tuple[bool, str]:
        """Check if portfolio drawdown exceeds allowable 24h loss."""
        if self.daily_high_watermark_usd <= 0:
            return True, "Invalid portfolio state."
            
        drawdown = (self.daily_high_watermark_usd - self.current_portfolio_usd) / self.daily_high_watermark_usd
        if drawdown >= RISK_POLICY.max_daily_loss_pct:
            self.is_circuit_breaker_active = True
            return False, f"CIRCUIT BREAKER TRIGGERED: Daily loss {drawdown*100:.2f}% exceeds limit {RISK_POLICY.max_daily_loss_pct*100}%."
        return True, "Circuit breaker normal."

    def validate_proposed_trade(self, trade_proposal: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Validates all parameters of an AI-proposed trade.
        Returns: (is_valid: bool, reason: str)
        """
        # 1. Circuit breaker check
        ok, reason = self.check_circuit_breaker()
        if not ok:
            return False, reason

        # 2. Token Allowlist verification
        input_mint = trade_proposal.get("input_mint", "")
        output_mint = trade_proposal.get("output_mint", "")
        if input_mint not in RISK_POLICY.allowed_mints:
            return False, f"REJECTED: Input mint {input_mint} is not in the verified allowlist."
        if output_mint not in RISK_POLICY.allowed_mints:
            return False, f"REJECTED: Output mint {output_mint} is not in the verified allowlist."
        if input_mint == output_mint:
            return False, "REJECTED: Input and output mints are identical."

        # 3. Maximum Trade Size (SOL)
        amount_sol = float(trade_proposal.get("amount_sol", 0.0))
        if amount_sol <= 0:
            return False, "REJECTED: Trade amount must be positive."
        if amount_sol > RISK_POLICY.max_trade_sol:
            return False, f"REJECTED: Amount {amount_sol} SOL exceeds max trade cap of {RISK_POLICY.max_trade_sol} SOL."

        # 4. Maximum Portfolio Percentage
        trade_usd_value = float(trade_proposal.get("estimated_usd_value", 0.0))
        max_allowed_usd = self.current_portfolio_usd * RISK_POLICY.max_trade_pct_portfolio
        if trade_usd_value > max_allowed_usd:
            return False, (
                f"REJECTED: Trade value ${trade_usd_value:.2f} exceeds "
                f"{RISK_POLICY.max_trade_pct_portfolio*100:.1f}% portfolio cap (${max_allowed_usd:.2f})."
            )

        # 5. Slippage Tolerance Guard
        slippage_bps = int(trade_proposal.get("slippage_bps", 0))
        if slippage_bps > RISK_POLICY.max_slippage_bps:
            return False, f"REJECTED: Slippage {slippage_bps} bps exceeds maximum allowable {RISK_POLICY.max_slippage_bps} bps."

        # 6. Cooldown interval check
        now = time.time()
        elapsed = now - self.last_trade_timestamp
        if elapsed < RISK_POLICY.cooldown_seconds:
            remaining = RISK_POLICY.cooldown_seconds - elapsed
            return False, f"REJECTED: Cooldown active. Must wait {remaining:.1f}s before next execution."

        return True, "PASSED: All policy parameters verified safe."

    def record_execution(self, trade_usd_value: float, pnl_usd: float = 0.0):
        """Update internal accounting after an approved trade completes."""
        self.last_trade_timestamp = time.time()
        self.daily_trades_count += 1
        self.current_portfolio_usd += pnl_usd
        if self.current_portfolio_usd > self.daily_high_watermark_usd:
            self.daily_high_watermark_usd = self.current_portfolio_usd
