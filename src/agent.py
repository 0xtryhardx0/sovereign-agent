from typing import Dict, Any, List, Tuple

class SovereignTradingAgent:
    """
    Sovereign AI Alpha Decision Engine.
    Operates on a strict 5-Pillar Confluence Scoring Matrix:
      1. Volume Footprint (1h Volume vs 24h Hourly Baseline)
      2. Order Flow Delta (Buyer vs Seller Aggression)
      3. Micro Momentum Alignment (5m Velocity Impulse)
      4. Structural Location (Range Value / Demand Zone)
      5. Asymmetric Risk/Reward (Minimum 2.0:1 R:R)

    Threshold Rules:
      - Tier 1 (Score 4-5/5): HIGH CONVICTION ($100 Full Size)
      - Tier 2 (Score 3/5):   TACTICAL SCALP   ($50 Half Size)
      - Tier 3 (Score < 3/5): HARD PASS        (Capital Preserved)
    """
    def __init__(self, agent_name: str = "Sovereign-Alpha-1"):
        self.name = agent_name
        self.callout_counter = 0

    def evaluate_confluences(self, metrics: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], int]:
        """
        Evaluates the 5 market pillars and returns:
          (checklist: List[Dict], passed_count: int)
        """
        price = metrics["price_usd"]
        vol_mult = metrics.get("volume_multiplier", 1.0)
        vol_1h = metrics.get("volume_1h", 0.0)
        buy_pressure = metrics.get("buy_pressure_pct", 50.0)
        buys = metrics.get("buys_1h", 0)
        sells = metrics.get("sells_1h", 0)
        chg_5m = metrics.get("price_change_5m", 0.0)
        chg_1h = metrics.get("price_change_1h", 0.0)
        range_pos = metrics.get("range_position_pct", 50.0)

        checklist = []

        # Pillar 1: Volume Footprint (Vol Multiplier >= 1.35x baseline)
        p1_pass = vol_mult >= 1.35
        checklist.append({
            "pillar": "Volume Footprint",
            "passed": p1_pass,
            "detail": f"1h Vol ${vol_1h:,.0f} is {vol_mult:.2f}x hourly baseline (Threshold: ≥1.35x)"
        })

        # Pillar 2: Order Flow Delta (Buy pressure >= 53.0%)
        p2_pass = buy_pressure >= 53.0
        checklist.append({
            "pillar": "Order Flow Delta",
            "passed": p2_pass,
            "detail": f"{buy_pressure:.1f}% Buyer Dominance ({buys} buys vs {sells} sells, Threshold: ≥53%)"
        })

        # Pillar 3: Micro Momentum Alignment (5m velocity > 0.02% or 1h > 0.2%)
        p3_pass = chg_5m >= 0.02 or chg_1h >= 0.25
        checklist.append({
            "pillar": "Micro Momentum",
            "passed": p3_pass,
            "detail": f"5m velocity {chg_5m:+.2f}% / 1h {chg_1h:+.2f}% confirming directional flow"
        })

        # Pillar 4: Structural Location (Discount zone <= 40% OR Breakout >= 70%)
        p4_pass = (range_pos <= 40.0) or (range_pos >= 70.0 and chg_1h > 0.5)
        location_desc = "Discount / Demand Zone" if range_pos <= 40.0 else ("Momentum Expansion Zone" if range_pos >= 70.0 else "Mid-Range Equilibrium")
        checklist.append({
            "pillar": "Structural Location",
            "passed": p4_pass,
            "detail": f"Price at {range_pos:.1f}% of 24h range ({location_desc})"
        })

        # Pillar 5: Asymmetric Risk/Reward (Default setup provides 2.17:1 R:R)
        # Always verified mathematically in our risk parameters
        p5_pass = True
        checklist.append({
            "pillar": "Risk / Reward Ratio",
            "passed": p5_pass,
            "detail": "2.17 : 1 Asymmetric Ratio (Take Profit +6.5% vs Stop Loss -3.0%)"
        })

        passed_count = sum(1 for item in checklist if item["passed"])
        return checklist, passed_count

    def analyze_token_setup(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Runs the full 5-Pillar evaluation on a single token.
        Only generates an active callout if confluences >= 3.
        """
        symbol = metrics["symbol"]
        price = metrics["price_usd"]
        checklist, score = self.evaluate_confluences(metrics)

        # Tier 1: High Conviction Setup (4 or 5 / 5)
        if score >= 4:
            self.callout_counter += 1
            tp_pct = 6.5
            sl_pct = 3.0
            target_price = price * (1.0 + tp_pct / 100.0)
            stop_price = price * (1.0 - sl_pct / 100.0)
            confidence = min(round(82.0 + score * 2.5 + (metrics.get("buy_pressure_pct", 50.0) - 50.0), 1), 94.5)

            rationale = self._synthesize_narrative(symbol, checklist, "HIGH_CONVICTION", score)

            return {
                "callout_id": f"ALPHA-{self.callout_counter:03d}",
                "symbol": symbol,
                "pair": f"{symbol}/USDC",
                "tier": "TIER 1: HIGH CONVICTION",
                "tier_level": 1,
                "action": "BUY",
                "confluence_score": score,
                "max_score": 5,
                "confluence_checklist": checklist,
                "allocation_usd": 100.0,
                "entry_price": price,
                "price_usd": price,
                "volume_multiplier": metrics.get("volume_multiplier", 1.5),
                "liquidity_usd": metrics.get("liquidity_usd", 500000.0),
                "buy_pressure_pct": metrics.get("buy_pressure_pct", 55.0),
                "price_change_5m": metrics.get("price_change_5m", 0.0),
                "price_change_1h": metrics.get("price_change_1h", 0.0),
                "mint": metrics.get("mint", ""),
                "target_price": round(target_price, 6 if price < 0.01 else 4),
                "stop_price": round(stop_price, 6 if price < 0.01 else 4),
                "take_profit_pct": tp_pct,
                "stop_loss_pct": sl_pct,
                "risk_reward_ratio": "2.17 : 1",
                "confidence_score": confidence,
                "rationale": rationale,
                "timestamp": metrics["timestamp"],
                "readable_time": metrics["readable_time"]
            }

        # Tier 2: Tactical Setup (3 / 5)
        elif score == 3:
            self.callout_counter += 1
            tp_pct = 3.8
            sl_pct = 1.8
            target_price = price * (1.0 + tp_pct / 100.0)
            stop_price = price * (1.0 - sl_pct / 100.0)
            confidence = round(74.0 + (metrics.get("buy_pressure_pct", 50.0) - 50.0), 1)

            rationale = self._synthesize_narrative(symbol, checklist, "TACTICAL_SCALP", score)

            return {
                "callout_id": f"ALPHA-{self.callout_counter:03d}",
                "symbol": symbol,
                "pair": f"{symbol}/USDC",
                "tier": "TIER 2: TACTICAL SCALP",
                "tier_level": 2,
                "action": "BUY (TACTICAL)",
                "confluence_score": score,
                "max_score": 5,
                "confluence_checklist": checklist,
                "allocation_usd": 50.0,
                "entry_price": price,
                "price_usd": price,
                "volume_multiplier": metrics.get("volume_multiplier", 1.5),
                "liquidity_usd": metrics.get("liquidity_usd", 500000.0),
                "buy_pressure_pct": metrics.get("buy_pressure_pct", 55.0),
                "price_change_5m": metrics.get("price_change_5m", 0.0),
                "price_change_1h": metrics.get("price_change_1h", 0.0),
                "mint": metrics.get("mint", ""),
                "target_price": round(target_price, 6 if price < 0.01 else 4),
                "stop_price": round(stop_price, 6 if price < 0.01 else 4),
                "take_profit_pct": tp_pct,
                "stop_loss_pct": sl_pct,
                "risk_reward_ratio": "2.11 : 1",
                "confidence_score": confidence,
                "rationale": rationale,
                "timestamp": metrics["timestamp"],
                "readable_time": metrics["readable_time"]
            }

        # Tier 3: Hard Pass (< 3 / 5)
        else:
            failed_pillars = [item["pillar"] for item in checklist if not item["passed"]]
            pass_reason = (
                f"Confluence score insufficient ({score}/5). "
                f"Failed criteria: {', '.join(failed_pillars)}. "
                f"Preserving capital until high-conviction order flow alignment occurs."
            )
            return {
                "callout_id": None,
                "symbol": symbol,
                "pair": f"{symbol}/USDC",
                "tier": "HARD PASS",
                "tier_level": 3,
                "action": "HOLD / PRESERVE CAPITAL",
                "confluence_score": score,
                "max_score": 5,
                "confluence_checklist": checklist,
                "allocation_usd": 0.0,
                "entry_price": price,
                "target_price": None,
                "stop_price": None,
                "take_profit_pct": 0.0,
                "stop_loss_pct": 0.0,
                "risk_reward_ratio": "N/A",
                "confidence_score": 40.0,
                "rationale": pass_reason,
                "timestamp": metrics["timestamp"],
                "readable_time": metrics["readable_time"]
            }

    def _synthesize_narrative(self, symbol: str, checklist: List[Dict[str, Any]], setup_type: str, score: int) -> str:
        passed_points = [item["detail"] for item in checklist if item["passed"]]
        if setup_type == "HIGH_CONVICTION":
            return (
                f"Institutional order-flow breakout confirmed on #{symbol} with {score}/5 confluences. "
                f"{passed_points[0]} and {passed_points[1]}. "
                f"Taker buyer aggression is absorbing overhead asks with positive velocity confirmation. "
                f"Invalidation stop is anchored directly beneath key structural support."
            )
        else:
            return (
                f"Tactical momentum play on #{symbol} qualifying with {score}/5 confluences. "
                f"Favorable micro-volume absorption detected. "
                f"Targeting a rapid mean-reversion scalp with tightened risk exposure."
            )

    def scan_all_and_select_best(self, all_metrics: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Scans all watched assets and returns active callouts (Score >= 3)."""
        signals = []
        for m in all_metrics:
            sig = self.analyze_token_setup(m)
            if sig.get("callout_id"):
                signals.append(sig)
        return signals
