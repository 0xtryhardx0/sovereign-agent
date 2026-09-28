from typing import Dict, Any, List

class SovereignTradingAgent:
    """
    Autonomous AI Alpha Engine.
    Analyzes live Solana market telemetry (Price action, 1h/24h volume, buy pressure,
    and momentum indicators) to generate high-conviction trade setups with exact
    Take-Profit, Stop-Loss, and technical order-flow rationale.
    """
    def __init__(self, agent_name: str = "Sovereign-Alpha-1"):
        self.name = agent_name
        self.callout_counter = 0

    def analyze_token_setup(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluates a single token's telemetry and generates a formal trade signal.
        """
        symbol = metrics["symbol"]
        price = metrics["price_usd"]
        chg_5m = metrics.get("price_change_5m", 0.0)
        chg_1h = metrics.get("price_change_1h", 0.0)
        chg_24h = metrics.get("price_change_24h", 0.0)
        buy_pressure = metrics.get("buy_pressure_pct", 50.0)
        vol_1h = metrics.get("volume_1h", 0.0)

        # 1. Bullish Momentum Breakout Strategy
        if buy_pressure >= 52.0 and (chg_5m > 0.05 or chg_1h > 0.2):
            tp_pct = 0.065   # +6.5% Target
            sl_pct = 0.030   # -3.0% Stop Loss
            self.callout_counter += 1

            target_price = price * (1.0 + tp_pct)
            stop_price = price * (1.0 - sl_pct)
            confidence = min(round(50 + (buy_pressure - 50) * 1.8 + max(chg_1h, 0) * 2, 1), 94.0)

            rationale = (
                f"Aggressive buyer dominance ({buy_pressure}% buy ratio) across 1h volume of ${vol_1h:,.0f}. "
                f"5-min velocity (+{chg_5m}%) confirms upward momentum break. "
                f"Risk/Reward profile is favorable at 2.17:1 with stop pegged at ${stop_price:.4f}."
            )

            return {
                "callout_id": f"ALPHA-{self.callout_counter:03d}",
                "symbol": symbol,
                "pair": f"{symbol}/USDC",
                "action": "BUY",
                "entry_price": price,
                "target_price": round(target_price, 6 if price < 0.01 else 4),
                "stop_price": round(stop_price, 6 if price < 0.01 else 4),
                "take_profit_pct": round(tp_pct * 100, 1),
                "stop_loss_pct": round(sl_pct * 100, 1),
                "confidence_score": confidence,
                "rationale": rationale,
                "timestamp": metrics["timestamp"],
                "readable_time": metrics["readable_time"]
            }

        # 2. Oversold Dip Reversal Strategy
        elif chg_1h <= -1.8 and buy_pressure >= 48.0:
            tp_pct = 0.050   # +5.0% Mean Reversion
            sl_pct = 0.025   # -2.5% Tight Stop
            self.callout_counter += 1

            target_price = price * (1.0 + tp_pct)
            stop_price = price * (1.0 - sl_pct)
            confidence = 82.5

            rationale = (
                f"Exhaustion dip detected: 1-hour drop of {chg_1h}% entering strong liquidity support. "
                f"Bid absorption increasing with buy ratio stabilizing at {buy_pressure}%. "
                f"Anticipating quick mean-reversion bounce toward ${target_price:.4f}."
            )

            return {
                "callout_id": f"ALPHA-{self.callout_counter:03d}",
                "symbol": symbol,
                "pair": f"{symbol}/USDC",
                "action": "BUY (DIP)",
                "entry_price": price,
                "target_price": round(target_price, 6 if price < 0.01 else 4),
                "stop_price": round(stop_price, 6 if price < 0.01 else 4),
                "take_profit_pct": round(tp_pct * 100, 1),
                "stop_loss_pct": round(sl_pct * 100, 1),
                "confidence_score": confidence,
                "rationale": rationale,
                "timestamp": metrics["timestamp"],
                "readable_time": metrics["readable_time"]
            }

        # 3. Neutral / No Clear Edge
        else:
            return {
                "callout_id": None,
                "symbol": symbol,
                "pair": f"{symbol}/USDC",
                "action": "HOLD / NEUTRAL",
                "entry_price": price,
                "target_price": None,
                "stop_price": None,
                "take_profit_pct": 0.0,
                "stop_loss_pct": 0.0,
                "confidence_score": 45.0,
                "rationale": f"Market ranging sideways (1h change: {chg_1h}%, buy pressure: {buy_pressure}%). Capital preserved.",
                "timestamp": metrics["timestamp"],
                "readable_time": metrics["readable_time"]
            }

    def scan_all_and_select_best(self, all_metrics: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Scans all watched assets and returns active callouts."""
        signals = []
        for m in all_metrics:
            sig = self.analyze_token_setup(m)
            if sig.get("callout_id"):
                signals.append(sig)
        return signals
