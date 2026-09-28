import time
from typing import Dict, Any, List

class TradeJournal:
    """
    Public Alpha Broadcast Engine & Social Journal.
    Generates high-engagement, transparent callout cards with full
    confluence checklists formatted for X (Twitter), Telegram, and Discord,
    complete with 1-click Solana Action / Blink links.
    """
    def __init__(self):
        self.callout_history: List[Dict[str, Any]] = []

    def format_alpha_callout(self, signal: Dict[str, Any]) -> str:
        """
        Creates a viral, high-clarity callout card showing the 5 confluences.
        Properly handles micro-prices for memecoins (e.g. BONK).
        """
        symbol = signal["symbol"]
        action = signal["action"]
        entry = signal["entry_price"]
        target = signal["target_price"]
        stop = signal["stop_price"]
        tp_pct = signal["take_profit_pct"]
        sl_pct = signal["stop_loss_pct"]
        rr = signal.get("risk_reward_ratio", "2.17 : 1")
        tier = signal.get("tier", "TIER 1: HIGH CONVICTION")
        score = signal.get("confluence_score", 4)
        max_score = signal.get("max_score", 5)
        conf = signal["confidence_score"]
        rationale = signal["rationale"]
        callout_id = signal["callout_id"]
        checklist = signal.get("confluence_checklist", [])

        # Micro-pricing formatter
        fmt_price = lambda p: f"${p:,.4f}" if (p and p >= 0.01) else (f"${p:.8f}" if p else "$0.00")

        # Build visual checklist lines
        checklist_lines = []
        for item in checklist:
            icon = "[✓]" if item["passed"] else "[✗]"
            checklist_lines.append(f"  {icon} {item['pillar']}: {item['detail']}")
        checklist_str = "\n".join(checklist_lines)

        dial_to_blink = f"https://dial.to/?action=solana-action:https://jup.ag/api/v6/swap-action/{symbol}"

        card = (
            f"🎯 [SOVEREIGN ALPHA CALLOUT] #{callout_id}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🪙 Asset: #{symbol}/USDC\n"
            f"⚡ Signal: {action} @ {fmt_price(entry)}\n"
            f"🎯 Take Profit: {fmt_price(target)} (+{tp_pct}%)\n"
            f"🛑 Stop Loss:   {fmt_price(stop)} (-{sl_pct}%)\n"
            f"⚖️ Risk/Reward: {rr}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🔍 Confluence Score: {score} / {max_score} [{tier}]\n"
            f"{checklist_str}\n\n"
            f"🧠 Analytical Synthesis:\n"
            f"\"{rationale}\"\n\n"
            f"⚡ 1-Click Copy Trade (Solana Blink):\n"
            f"👉 {dial_to_blink}\n\n"
            f"🛡️ Mode: Unfunded Paper Signal\n"
            f"#Solana #AgentFi #CryptoAlpha #TradingBots"
        )
        return card

    def format_closure_update(self, closed_pos: Dict[str, Any]) -> str:
        """Formats a transparent win/loss closure report."""
        sym = closed_pos["symbol"]
        reason = closed_pos["exit_reason"]
        pnl_pct = closed_pos["realized_pnl_pct"]
        pnl_usd = closed_pos["realized_pnl_usd"]
        sign = "+" if pnl_usd >= 0 else ""
        icon = "🎉" if pnl_usd >= 0 else "🛡️"

        card = (
            f"{icon} [POSITION CLOSED] #{closed_pos.get('callout_id', 'ALPHA')}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🪙 Asset: #{sym}/USDC\n"
            f"🏁 Result: {reason}\n"
            f"💰 Return: {sign}{pnl_pct}% ({sign}${pnl_usd:,.2f})\n"
            f"⏱️ Hold: {closed_pos['entry_readable']} ➔ {closed_pos.get('exit_readable', 'Now')}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Verified on Sovereign Virtual Ledger. #Transparency"
        )
        return card
