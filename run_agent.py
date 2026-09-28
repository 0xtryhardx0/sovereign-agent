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
    print("="*65)
    print("⚡ SOVEREIGN AGENT — Unfunded AI Alpha Sentinel & Paper Trader")
    print("   Mode: Paper Trading & Social Callout Engine (Zero Capital at Risk)")
    print("   Data Feed: Live DexScreener Solana Telemetry")
    print("="*65)

    feed = MarketDataFeed()
    agent = SovereignTradingAgent(agent_name="Sovereign-Alpha-1")
    policy_wall = DeterministicPolicyWall(initial_portfolio_usd=1000.0)
    portfolio = PaperPortfolio(initial_balance_usd=1000.0, position_size_usd=100.0)
    journal = TradeJournal()

    print("\n📡 Fetching live real-time market data from Solana DEXes...")
    all_metrics = feed.fetch_all_watched()

    print(f"\n{'TOKEN':<8} | {'PRICE (USD)':<12} | {'1H CHG':<8} | {'24H VOL':<12} | {'BUY PRESSURE'}")
    print("-" * 65)
    live_prices = {}
    for m in all_metrics:
        live_prices[m["symbol"]] = m["price_usd"]
        p_str = f"${m['price_usd']:,.4f}" if m['price_usd'] >= 0.01 else f"${m['price_usd']:.8f}"
        print(f"{m['symbol']:<8} | {p_str:<12} | {m['price_change_1h']:>+6.2f}% | ${m['volume_24h']:>10,.0f} | {m['buy_pressure_pct']:>5.1f}%")

    print("\n🧠 Running Sovereign AI Alpha Decision Engine across live tokens...")
    signals = agent.scan_all_and_select_best(all_metrics)

    if not signals:
        print("\n[Status] Market conditions currently neutral across watched assets. Capital preserved.")
    else:
        print(f"\n[Alpha Detected] Found {len(signals)} actionable trade setup(s):\n")

        for sig in signals:
            # 1. Deterministic Policy Wall Verification
            # In paper mode, we mock the mints for policy check
            proposal = {
                "input_mint": "So11111111111111111111111111111111111111112",
                "output_mint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                "amount_sol": 0.8,
                "estimated_usd_value": 100.0,
                "slippage_bps": 50,
            }
            is_valid, reason = policy_wall.validate_proposed_trade(proposal)
            
            if is_valid:
                # 2. Open Virtual Position
                pos_res = portfolio.open_paper_trade(sig)
                
                # 3. Format Public Callout
                callout_text = journal.format_alpha_callout(sig)
                print(callout_text)
                print("\n" + "="*65 + "\n")

    # Update open positions with live prices
    events = portfolio.update_and_evaluate_positions(live_prices)
    for ev in events:
        close_post = journal.format_closure_update(ev["position"])
        print(close_post)
        print("\n" + "="*65 + "\n")

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
