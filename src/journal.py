import time
from typing import Dict, Any, List

class TradeJournal:
    """
    Maintains a transparent, public audit log of all agent proposals,
    policy decisions (approvals/rejections), and on-chain execution receipts.
    Also formats broadcast-ready messages for X (Twitter) and Discord.
    """
    def __init__(self):
        self.history: List[Dict[str, Any]] = []

    def log_trade(
        self,
        proposal: Dict[str, Any],
        is_approved: bool,
        policy_reason: str,
        execution_result: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        entry = {
            "timestamp": time.time(),
            "readable_time": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
            "proposal": proposal,
            "approved": is_approved,
            "policy_reason": policy_reason,
            "execution": execution_result or {}
        }
        self.history.append(entry)
        return entry

    def generate_x_broadcast_post(self, entry: Dict[str, Any]) -> str:
        """Format an approved trade into a viral, transparent X (Twitter) update."""
        prop = entry["proposal"]
        exec_res = entry["execution"]
        
        pair = f"{prop.get('symbol_in', 'SOL')} ➔ {prop.get('symbol_out', 'USDC')}"
        rationale = prop.get("reasoning", "Algorithmic momentum rebalance")
        
        if entry["approved"]:
            tx_sig = exec_res.get("tx_signature", "pending")
            return (
                f"🤖 [Sovereign Agent Trade Executed]\n\n"
                f"📊 Asset Pair: {pair}\n"
                f"💰 Size: {prop.get('amount_sol', 0)} SOL (~${prop.get('estimated_usd_value', 0):.2f})\n"
                f"🧠 Rationale: \"{rationale}\"\n"
                f"🛡️ Policy Wall: Verified 100% compliant with risk limits.\n"
                f"🔗 On-chain Tx: https://solscan.io/tx/{tx_sig}\n\n"
                f"#Solana #AgentFi #AutonomousAgents"
            )
        else:
            return (
                f"🛡️ [Sovereign Agent Trade Blocked]\n\n"
                f"The AI model proposed swapping {pair}, but the Deterministic Policy Wall intercepted and rejected the transaction:\n"
                f"⚠️ Reason: {entry['policy_reason']}\n\n"
                f"Non-custodial guardrails protect capital against hallucinations. #SecurityFirst"
            )
