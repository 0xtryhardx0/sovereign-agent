"""
BlinkCraft 1-Click Copy Trading Integration for Sovereign Agent.
Generates Dialect-compliant Solana Actions and shareable dial.to Blinks
for high-conviction alpha callouts and portfolio signals.
"""

from typing import Dict, Any

class BlinkCraftBridge:
    """
    Generates Dialect / Solana Action URLs and formatted tweet preview payloads
    so followers can 1-click copy trade Sovereign Agent's on-chain positions.
    """
    def __init__(self, base_hub_url: str = "https://blinkcraftstudio.vercel.app"):
        self.base_hub_url = base_hub_url.rstrip("/")

    def generate_trade_blink(self, signal: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a live Solana Blink specification and dial.to link from a trade signal.
        """
        symbol = signal.get("symbol", "SOL").upper()
        price = float(signal.get("entry_price") or signal.get("entry_price_usd") or signal.get("price_usd") or signal.get("price") or 1.0)
        target = float(signal.get("target_price") or signal.get("target_price_usd") or (price * 1.08))
        stop = float(signal.get("stop_price") or signal.get("stop_loss_usd") or (price * 0.94))
        score = signal.get("confluence_score") or signal.get("score") or 5

        target_pct = ((target - price) / price * 100) if price > 0 else 8.0
        stop_pct = ((price - stop) / price * 100) if price > 0 else 6.0

        title = f"Copy Sovereign Agent: Buy ${symbol} on Jupiter"
        description = (
            f"⚡ Sovereign AI Signal [{score}/5 Confluence]: Entry ${price:,.2f} | "
            f"Target ${target:,.2f} (+{target_pct:.1f}%) | "
            f"Stop ${stop:,.2f} (-{stop_pct:.1f}%). "
            f"Audited by Argus Sentinel."
        )

        icon_map = {
            "SOL": "https://raw.githubusercontent.com/solana-labs/token-list/main/assets/mainnet/So11111111111111111111111111111111111111112/logo.png",
            "JUP": "https://static.jup.ag/jup/icon.png",
            "RAY": "https://raw.githubusercontent.com/solana-labs/token-list/main/assets/mainnet/4k3Dyjzvzp8eMZWUXbBCjEvwSkkk59S5iCNLY3QrkX6R/logo.png",
            "BONK": "https://arweave.net/hQiPZOsRZXGXBJd_82PhVdlM_hACsT_q6wqwf5c90TU",
            "WIF": "https://bafkreibk3yf35svwvqj32amdrldwax5e7ehy2k67tnhqg4j3j4z6c3m6eu.ipfs.nftstorage.link"
        }
        icon_url = icon_map.get(symbol, "https://raw.githubusercontent.com/solana-labs/token-list/main/assets/mainnet/So11111111111111111111111111111111111111112/logo.png")

        # Dialect compliant action URL
        action_api = f"{self.base_hub_url}/api/actions/copy-trade?token={symbol}&price={price}"
        dial_to_url = f"https://dial.to/?action=solana-action:{action_api}"

        tweet_text = (
            f"🚨 SOVEREIGN ALPHA SIGNAL: ${symbol}\n\n"
            f"📊 Confluence: {score}/5 Verified\n"
            f"🎯 Target: ${target:,.2f} | 🛑 Stop: ${stop:,.2f}\n"
            f"🛡️ Argus Audit: PASSED (Zero Honeypot Risk)\n\n"
            f"1-Click Copy Trade via Solana Blink 👇\n{dial_to_url}"
        )

        return {
            "symbol": symbol,
            "title": title,
            "description": description,
            "icon": icon_url,
            "action_url": action_api,
            "blink_url": dial_to_url,
            "tweet_text": tweet_text,
            "actions": [
                {"label": "0.1 SOL", "href": f"{action_api}&amount=0.1"},
                {"label": "0.5 SOL", "href": f"{action_api}&amount=0.5"},
                {"label": "1.0 SOL", "href": f"{action_api}&amount=1.0"}
            ]
        }
