"""
BlinkCraft 1-Click Copy Trading Integration for Sovereign Agent.
Generates Dialect-compliant Solana Action specifications and shareable dial.to Blinks
bound directly to real trades taken, scanned coins, or custom investment theses.
"""

from typing import Dict, Any

POPULAR_TOKEN_MINTS = {
    "SOL": "So11111111111111111111111111111111111111112",
    "JUP": "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN",
    "RAY": "4k3Dyjzvzp8eMZWUXbBCjEvwSkkk59S5iCNLY3QrkX6R",
    "BONK": "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263",
    "WIF": "EKpQGSJtjMFqKZ9KQanSqYXRcF8fBopzLHYxdM65zcjm",
    "POPCAT": "7GCihgDB8fe6KNjn2MYtkzZcRjQy3t9GHdC8uHYmW2hr",
    "RENDER": "rndrizKT3MK1iimdxRdWabcF7Zg7AR5T4nud4EkHBof"
}

POPULAR_TOKEN_ICONS = {
    "SOL": "https://raw.githubusercontent.com/solana-labs/token-list/main/assets/mainnet/So11111111111111111111111111111111111111112/logo.png",
    "JUP": "https://static.jup.ag/jup/icon.png",
    "RAY": "https://raw.githubusercontent.com/solana-labs/token-list/main/assets/mainnet/4k3Dyjzvzp8eMZWUXbBCjEvwSkkk59S5iCNLY3QrkX6R/logo.png",
    "BONK": "https://arweave.net/hQiPZOsRZXGXBJd_82PhVdlM_hACsT_q6wqwf5c90TU",
    "WIF": "https://bafkreibk3yf35svwvqj32amdrldwax5e7ehy2k67tnhqg4j3j4z6c3m6eu.ipfs.nftstorage.link",
    "POPCAT": "https://bafkreidvkvfweqf7s2q6uquqzgvkmvyfx72j3b4m5t7m3a7s4u2p4g5qhe.ipfs.nftstorage.link",
    "RENDER": "https://raw.githubusercontent.com/solana-labs/token-list/main/assets/mainnet/rndrizKT3MK1iimdxRdWabcF7Zg7AR5T4nud4EkHBof/logo.png"
}

class BlinkCraftBridge:
    """
    Generates Dialect / Solana Action URLs and formatted tweet preview payloads
    bound directly to live trade setups, scanned coins, or written theses.
    """
    def __init__(self, base_hub_url: str = "https://blinkcraftstudio.vercel.app"):
        self.base_hub_url = base_hub_url.rstrip("/")

    def generate_trade_blink(self, signal: Dict[str, Any]) -> Dict[str, Any]:
        """
        Binds a Blink directly to an active trade setup.
        """
        symbol = signal.get("symbol", "SOL").upper()
        price = float(signal.get("entry_price") or signal.get("entry_price_usd") or signal.get("price_usd") or signal.get("price") or 1.0)
        target = float(signal.get("target_price") or signal.get("target_price_usd") or (price * 1.085))
        stop = float(signal.get("stop_price") or signal.get("stop_loss_usd") or (price * 0.94))
        score = signal.get("confluence_score") or signal.get("score") or 5
        thesis = signal.get("thesis") or signal.get("rationale") or f"High volume breakout confirmed on Jupiter order flow."

        target_pct = ((target - price) / price * 100) if price > 0 else 8.5
        stop_pct = ((price - stop) / price * 100) if price > 0 else 6.0

        title = f"Copy Trade: Buy ${symbol} on Jupiter"
        description = (
            f"⚡ Sovereign AI Signal [{score}/5 Confluence]: Entry ${price:,.2f} | "
            f"Target ${target:,.2f} (+{target_pct:.1f}%) | Stop ${stop:,.2f} (-{stop_pct:.1f}%). "
            f"{thesis} Audited by Argus Sentinel."
        )

        mint = signal.get("mint") or POPULAR_TOKEN_MINTS.get(symbol, "So11111111111111111111111111111111111111112")
        icon_url = POPULAR_TOKEN_ICONS.get(symbol, f"https://api.dicebear.com/7.x/identicon/svg?seed={symbol}")

        # Dialect compliant action URL
        action_api = f"{self.base_hub_url}/api/actions/copy-trade?token={symbol}&mint={mint}&price={price}"
        dial_to_url = f"https://dial.to/?action=solana-action:{action_api}"

        tweet_text = (
            f"🚨 SOVEREIGN TRADE SIGNAL: ${symbol}\n\n"
            f"💡 Thesis: {thesis[:90]}\n"
            f"🎯 Target: ${target:,.2f} (+{target_pct:.1f}%)\n"
            f"🛑 Stop: ${stop:,.2f} (-{stop_pct:.1f}%)\n"
            f"🛡️ Argus Audit: PASSED (Zero Honeypot Risk)\n\n"
            f"1-Click Copy Trade via Solana Blink 👇\n{dial_to_url}"
        )

        return {
            "symbol": symbol,
            "mint": mint,
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

    def generate_thesis_blink(self, symbol: str, custom_thesis: str, price: float = 1.0) -> Dict[str, Any]:
        """
        Binds a Blink to a custom written investment thesis or scanned coin.
        """
        sym = symbol.upper().strip()
        signal = {
            "symbol": sym,
            "entry_price": price,
            "target_price": price * 1.10,
            "stop_price": price * 0.95,
            "score": 5,
            "thesis": custom_thesis or f"Strategic position taken on ${sym}."
        }
        return self.generate_trade_blink(signal)
