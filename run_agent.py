#!/usr/bin/env python3
import sys
import time
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent))

from src.market_data import MarketDataFeed
from src.agent import SovereignTradingAgent
from src.policy_engine import DeterministicPolicyWall
from src.paper_portfolio import PaperPortfolio
from src.journal import TradeJournal

def main():
    print("="*68)
    print("⚡ SOVEREIGN AGENT — 5-Pillar Confluence Alpha Sentinel")
    print("   Mode: Paper Trading & Social Callout Engine (Zero Capital at Risk)")
    print("   Strategy: Multi-Confluence Scoring (Tier 1: ≥4/5 | Tier 2: 3/5)")
    print("   Data Feed: Live DexScreener Solana Telemetry")
    print("="*68)

    feed = MarketDataFeed()
    agent = SovereignTradingAgent(agent_name="Sovereign-Alpha-1")
    policy_wall = DeterministicPolicyWall(initial_portfolio_usd=1000.0)
    portfolio = PaperPortfolio(initial_balance_usd=1000.0, default_position_size_usd=100.0)
    journal = TradeJournal()

    print("\n📡 Fetching live real-time market data from Solana DEXes...")
    all_metrics = feed.fetch_all_watched()

    print(f"\n{'TOKEN':<7} | {'PRICE (USD)':<11} | {'1H CHG':<7} | {'VOL MULT':<8} | {'BUY DELTA':<9} | {'SCORE':<5} | {'STATUS'}")
    print("-" * 76)
    
    live_prices = {}
    signals = []

    for m in all_metrics:
        live_prices[m["symbol"]] = m["price_usd"]
        checklist, score = agent.evaluate_confluences(m)
        p_str = f"${m['price_usd']:,.4f}" if m['price_usd'] >= 0.01 else f"${m['price_usd']:.8f}"
        
        status_label = "PASS (HOLD)"
        if score >= 4:
            status_label = "TIER 1 (STRONG BUY)"
        elif score == 3:
            status_label = "TIER 2 (TACTICAL)"

        print(f"{m['symbol']:<7} | {p_str:<11} | {m['price_change_1h']:>+5.2f}% | {m['volume_multiplier']:>6.2f}x | {m['buy_pressure_pct']:>7.1f}% | {score}/5 | {status_label}")
        
        setup = agent.analyze_token_setup(m)
        if setup.get("callout_id"):
            signals.append(setup)

    print("\n🧠 Evaluating Trade Opportunities Against Deterministic Policy Wall...")

    if not signals:
        print("\n[Audit Log] All watched tokens scored below minimum confluence threshold (<3/5).")
        print("            Deterministic Policy Wall preserved capital against noisy chop.")
    else:
        print(f"\n[Alpha Detected] Emitting {len(signals)} Qualified Trade Setup(s):\n")

        for sig in signals:
            proposal = {
                "input_mint": "So11111111111111111111111111111111111111112",
                "output_mint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                "amount_sol": 0.8,
                "estimated_usd_value": sig.get("allocation_usd", 100.0),
                "slippage_bps": 50,
            }
            is_valid, reason = policy_wall.validate_proposed_trade(proposal)
            
            if is_valid:
                pos_res = portfolio.open_paper_trade(sig)
                callout_text = journal.format_alpha_callout(sig)
                print(callout_text)
                print("\n" + "="*68 + "\n")

    # Update open positions with live prices
    events = portfolio.update_and_evaluate_positions(live_prices)
    for ev in events:
        close_post = journal.format_closure_update(ev["position"])
        print(close_post)
        print("\n" + "="*68 + "\n")

    # Display Performance Summary
    summary = portfolio.get_performance_summary()
    print("📊 VIRTUAL PERFORMANCE SUMMARY:")
    print(f"   Initial Bankroll:  ${summary['initial_balance']:,.2f}")
    print(f"   Cash Balance:      ${summary['cash_balance']:,.2f}")
    print(f"   Open Positions:    {summary['open_count']} (${summary['open_positions_value']:,.2f})")
    print(f"   Total Portfolio:   ${summary['total_portfolio_usd']:,.2f} ({summary['net_return_pct']:+.2f}%)")
    print(f"   Closed Trades:     {summary['closed_count']} (Win Rate: {summary['win_rate_pct']}%)")
    print("\n✅ Sovereign Agent Alpha Loop Complete.")

if __name__ == "__main__":
    main()
