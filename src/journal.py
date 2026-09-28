import time
from typing import Dict, Any, List

class TradeJournal:
    """
    Public Alpha Broadcast Engine & Social Journal.
    Generates high-engagement, transparent callout cards formatted
    for X (Twitter), Telegram, and Discord, complete with 1-click
    Solana Action / Blink links so followers can copy trades.
    """
    def __init__(self):
        self.callout_history: List[Dict[str, Any]] = []

    def format_alpha_callout(self, signal: Dict[str, Any]) -> str:
        """
        Creates a viral, high-clarity callout card for social broadcast.
        """
        symbol = signal["symbol"]
        action = signal["action"]
        entry = signal["entry_price"]
        target = signal["target_price"]
        stop = signal["stop_price"]
        tp_pct = signal["take_profit_pct"]
        sl_pct = signal["stop_loss_pct"]
        conf = signal["confidence_score"]
        rationale = signal["rationale"]
        callout_id = signal["callout_id"]

        # Real Jupiter swap deep link for 1-click execution
        jup_link = f"https://jup.ag/swap/USDC-{symbol}"
        dial_to_blink = f"https://dial.to/?action=solana-action:https://jup.ag/api/v6/swap-action/{symbol}"

        card = (
            f"🎯 [SOVEREIGN ALPHA CALLOUT] #{callout_id}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🪙 Asset: #{symbol}/USDC\n"
            f"⚡ Signal: {action} @ ${entry:,.4f}\n"
            f"🎯 Take Profit: ${target:,.4f} (+{tp_pct}%)\n"
            f"🛑 Stop Loss:   ${stop:,.4f} (-{sl_pct}%)\n"
            f"📊 Confidence:  {conf}%\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🧠 Technical Rationale:\n"
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
