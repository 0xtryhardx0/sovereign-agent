import json
from typing import Dict, Any
from config import VERIFIED_TOKEN_MINTS

class SovereignTradingAgent:
    """
    Core AI Decision Engine.
    Evaluates real-time market data, sentiment, and technical setups,
    and proposes structured trade actions for policy wall review.
    """
    def __init__(self, agent_name: str = "Sovereign-Alpha-1"):
        self.name = agent_name

    def evaluate_market_and_propose(self, market_snapshot: Dict[str, Any]) -> Dict[str, Any]:
        """
        Synthesizes market telemetry into a formal trade proposal.
        In production, this queries Gemini 1.5/2.0 or Claude with strict JSON schema.
        """
        sol_price = market_snapshot.get("sol_price", 145.0)
        rsi_14 = market_snapshot.get("rsi_14", 50.0)
        whale_net_flow_sol = market_snapshot.get("whale_net_flow_sol", 0.0)

        # Strategic heuristic / agent logic
        if rsi_14 > 72.0:
            # Overbought setup: Propose partial hedge into USDC
            amount_sol = 0.5
            return {
                "symbol_in": "SOL",
                "symbol_out": "USDC",
                "input_mint": VERIFIED_TOKEN_MINTS["SOL"],
                "output_mint": VERIFIED_TOKEN_MINTS["USDC"],
                "amount_sol": amount_sol,
                "estimated_usd_value": amount_sol * sol_price,
                "slippage_bps": 50,
                "reasoning": f"RSI is overbought at {rsi_14:.1f}. Taking profits and hedging into USDC."
            }
        elif rsi_14 < 35.0 and whale_net_flow_sol > 1000.0:
            # Oversold bounce with whale accumulation
            amount_sol = 0.8
            return {
                "symbol_in": "USDC",
                "symbol_out": "SOL",
                "input_mint": VERIFIED_TOKEN_MINTS["USDC"],
                "output_mint": VERIFIED_TOKEN_MINTS["SOL"],
                "amount_sol": amount_sol,
                "estimated_usd_value": amount_sol * sol_price,
                "slippage_bps": 50,
                "reasoning": f"RSI oversold ({rsi_14:.1f}) accompanied by +{whale_net_flow_sol} SOL whale accumulation."
            }
        else:
            # Hold / Neutral
            return {
                "symbol_in": "NONE",
                "symbol_out": "NONE",
                "amount_sol": 0.0,
                "estimated_usd_value": 0.0,
                "slippage_bps": 0,
                "reasoning": "Market conditions neutral; risk-reward profile unfavorable for entry."
            }
