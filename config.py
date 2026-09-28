import os
from dataclasses import dataclass
from typing import Dict, List

# Token Mints on Solana (Mainnet / Devnet verified mints)
VERIFIED_TOKEN_MINTS: Dict[str, str] = {
    "SOL": "So11111111111111111111111111111111111111112",
    "USDC": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
    "JUP": "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN",
    "BONK": "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263",
    "RENDER": "rndrizKT3MK1iimdxRdWabcF7Zg7AR5T4nud4EkHBof",
}

@dataclass(frozen=True)
class RiskPolicyConfig:
    max_trade_sol: float = 1.0                # Maximum SOL per individual trade
    max_trade_pct_portfolio: float = 0.05     # Maximum 5% of total portfolio in one position
    max_slippage_bps: int = 150              # Maximum 1.5% slippage (150 bps)
    max_daily_loss_pct: float = 0.08          # 8% 24h circuit breaker
    cooldown_seconds: int = 60                # Minimum interval between trades
    allowed_mints: tuple = tuple(VERIFIED_TOKEN_MINTS.values())

@dataclass
class NetworkConfig:
    solana_rpc_url: str = os.getenv("SOLANA_RPC_URL", "https://api.devnet.solana.com")
    jupiter_quote_api: str = "https://quote-api.jup.ag/v6"
    is_simulation: bool = os.getenv("SIMULATION_MODE", "true").lower() == "true"

RISK_POLICY = RiskPolicyConfig()
NETWORK_CONFIG = NetworkConfig()
