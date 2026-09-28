#!/usr/bin/env python3
import sys
import time
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent))

from config import RISK_POLICY, NETWORK_CONFIG
from src.agent import SovereignTradingAgent
from src.policy_engine import DeterministicPolicyWall
from src.dex_router import JupiterRouter
from src.journal import TradeJournal

def main():
    print("="*65)
    print("⚡ SOVEREIGN AGENT — Autonomous On-Chain AI Treasury Engine")
    print("   Architecture: 'The Model Proposes, Deterministic Code Disposes'")
    print("="*65)
    
    agent = SovereignTradingAgent(agent_name="Sovereign-Alpha-1")
    policy_wall = DeterministicPolicyWall(initial_portfolio_usd=5000.0)
    router = JupiterRouter(is_simulation=True)
    journal = TradeJournal()
    
    # Mock wallet public key
    mock_pubkey = "SovAgent11111111111111111111111111111111111"
    
    print(f"\n[Status] Agent Initialized: {agent.name}")
    print(f"[Status] Portfolio Value: ${policy_wall.current_portfolio_usd:,.2f}")
    print(f"[Status] Max Trade Cap: {RISK_POLICY.max_trade_sol} SOL | Daily Stop: {RISK_POLICY.max_daily_loss_pct*100}%\n")
    
    # Test Scenario 1: Overbought market signal
    print("--- [Cycle 1: Market Telemetry Ingestion] ---")
    telemetry_1 = {
        "sol_price": 148.20,
        "rsi_14": 74.5, # Overbought!
        "whale_net_flow_sol": -450.0
    }
    print(f"Incoming Telemetry: SOL=${telemetry_1['sol_price']} | RSI(14)={telemetry_1['rsi_14']} (Overbought)")
    
    # AI proposes
    proposal_1 = agent.evaluate_market_and_propose(telemetry_1)
    print(f"\n🧠 Model Proposed Action:")
    print(f"   Swap: {proposal_1['symbol_in']} ➔ {proposal_1['symbol_out']}")
    print(f"   Size: {proposal_1['amount_sol']} SOL (~${proposal_1['estimated_usd_value']:.2f})")
    print(f"   Reasoning: \"{proposal_1['reasoning']}\"")
    
    # Deterministic Policy Wall evaluates
    is_approved, reason = policy_wall.validate_proposed_trade(proposal_1)
    print(f"\n🛡️ Deterministic Policy Wall Verdict: {'APPROVED' if is_approved else 'REJECTED'}")
    print(f"   Details: {reason}")
    
    if is_approved:
        # Route through Jupiter
        quote = router.get_swap_quote(
            input_mint=proposal_1["input_mint"],
            output_mint=proposal_1["output_mint"],
            amount_lamports=int(proposal_1["amount_sol"] * 1e9),
            slippage_bps=proposal_1["slippage_bps"]
        )
        exec_res = router.execute_swap(quote, mock_pubkey)
        policy_wall.record_execution(proposal_1["estimated_usd_value"])
        entry = journal.log_trade(proposal_1, is_approved, reason, exec_res)
        
        print("\n⚡ Execution Complete:")
        print(f"   Tx Signature: {exec_res['tx_signature']}")
        print(f"   Explorer: {exec_res['explorer_url']}")
        
        # Social Syndicate Post
        x_post = journal.generate_x_broadcast_post(entry)
        print("\n📢 Public X/Twitter Syndicate Broadcast:")
        print("-" * 50)
        print(x_post)
        print("-" * 50)

    # Test Scenario 2: Hallucinated / Rogue Proposal (Blocked by Policy Wall)
    print("\n--- [Cycle 2: Rogue / Unverified Token Trap Test] ---")
    rogue_proposal = {
        "symbol_in": "SOL",
        "symbol_out": "MOON_SCAM",
        "input_mint": "So11111111111111111111111111111111111111112",
        "output_mint": "ScamHoneypotMint444444444444444444444444444",
        "amount_sol": 5.0, # Exceeds 1.0 SOL limit!
        "estimated_usd_value": 740.0,
        "slippage_bps": 500, # 5% slippage!
        "reasoning": "Unverified token trending on social media with 100x potential."
    }
    print("Model proposes 5 SOL swap into unverified meme token...")
    is_approved_2, reason_2 = policy_wall.validate_proposed_trade(rogue_proposal)
    print(f"🛡️ Deterministic Policy Wall Verdict: {'APPROVED' if is_approved_2 else 'REJECTED'}")
    print(f"   Reason: {reason_2}")
    
    entry_2 = journal.log_trade(rogue_proposal, is_approved_2, reason_2)
    x_post_2 = journal.generate_x_broadcast_post(entry_2)
    print("\n📢 Public X/Twitter Transparency Post:")
    print("-" * 50)
    print(x_post_2)
    print("-" * 50)
    print("\n✅ Sovereign Agent Cycle Successfully Verified.")

if __name__ == "__main__":
    main()
