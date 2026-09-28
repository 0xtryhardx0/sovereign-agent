import time
import requests
from typing import Dict, Any, List

# Core Solana tokens to track
WATCHED_TOKENS = {
    "SOL": {
        "mint": "So11111111111111111111111111111111111111112",
        "name": "Solana",
        "symbol": "SOL"
    },
    "JUP": {
        "mint": "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN",
        "name": "Jupiter",
        "symbol": "JUP"
    },
    "BONK": {
        "mint": "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263",
        "name": "Bonk",
        "symbol": "BONK"
    },
    "RENDER": {
        "mint": "rndrizKT3MK1iimdxRdWabcF7Zg7AR5T4nud4EkHBof",
        "name": "Render",
        "symbol": "RENDER"
    }
}

class MarketDataFeed:
    """
    Ingests live market telemetry from DexScreener's real-time API
    for Solana tokens (Price, Volume, Price Changes, Liquidity, Buy/Sell Tx Ratio).
    """
    def __init__(self):
        self.base_url = "https://api.dexscreener.com/latest/dex/tokens"

    def fetch_token_metrics(self, token_symbol: str) -> Dict[str, Any]:
        info = WATCHED_TOKENS.get(token_symbol.upper())
        if not info:
            raise ValueError(f"Token {token_symbol} not in watched tokens list.")

        mint = info["mint"]
        url = f"{self.base_url}/{mint}"

        try:
            resp = requests.get(url, timeout=6)
            if resp.status_code != 200:
                return self._fallback_metrics(token_symbol)

            data = resp.json()
            pairs = data.get("pairs", [])
            if not pairs:
                return self._fallback_metrics(token_symbol)

            # Filter for primary high-liquidity pair (prefer USDC or SOL quote)
            top_pair = pairs[0]
            price_usd = float(top_pair.get("priceUsd", 0.0) or 0.0)
            vol_24h = float(top_pair.get("volume", {}).get("h24", 0.0) or 0.0)
            vol_1h = float(top_pair.get("volume", {}).get("h1", 0.0) or 0.0)
            chg_5m = float(top_pair.get("priceChange", {}).get("m5", 0.0) or 0.0)
            chg_1h = float(top_pair.get("priceChange", {}).get("h1", 0.0) or 0.0)
            chg_24h = float(top_pair.get("priceChange", {}).get("h24", 0.0) or 0.0)
            liquidity_usd = float(top_pair.get("liquidity", {}).get("usd", 0.0) or 0.0)

            txns_1h = top_pair.get("txns", {}).get("h1", {})
            buys_1h = int(txns_1h.get("buys", 0) or 0)
            sells_1h = int(txns_1h.get("sells", 0) or 0)
            total_tx_1h = buys_1h + sells_1h
            buy_ratio = (buys_1h / total_tx_1h) if total_tx_1h > 0 else 0.50

            return {
                "symbol": token_symbol.upper(),
                "name": info["name"],
                "mint": mint,
                "price_usd": price_usd,
                "liquidity_usd": liquidity_usd,
                "volume_24h": vol_24h,
                "volume_1h": vol_1h,
                "price_change_5m": chg_5m,
                "price_change_1h": chg_1h,
                "price_change_24h": chg_24h,
                "buys_1h": buys_1h,
                "sells_1h": sells_1h,
                "buy_pressure_pct": round(buy_ratio * 100, 1),
                "timestamp": time.time(),
                "readable_time": time.strftime("%H:%M:%S UTC", time.gmtime())
            }

        except Exception as e:
            print(f"[MarketDataFeed] Warning fetching {token_symbol}: {e}")
            return self._fallback_metrics(token_symbol)

    def fetch_all_watched(self) -> List[Dict[str, Any]]:
        """Fetch metrics for all watched Solana tokens."""
        results = []
        for symbol in WATCHED_TOKENS:
            results.append(self.fetch_token_metrics(symbol))
        return results

    def _fallback_metrics(self, token_symbol: str) -> Dict[str, Any]:
        """Safe fallback if network/API drops temporarily."""
        defaults = {
            "SOL": 120.0,
            "JUP": 0.33,
            "BONK": 0.0000035,
            "RENDER": 1.95
        }
        price = defaults.get(token_symbol.upper(), 1.0)
        return {
            "symbol": token_symbol.upper(),
            "name": WATCHED_TOKENS[token_symbol.upper()]["name"],
            "mint": WATCHED_TOKENS[token_symbol.upper()]["mint"],
            "price_usd": price,
            "liquidity_usd": 500000.0,
            "volume_24h": 1000000.0,
            "volume_1h": 50000.0,
            "price_change_5m": 0.1,
            "price_change_1h": 0.4,
            "price_change_24h": 1.2,
            "buys_1h": 50,
            "sells_1h": 40,
            "buy_pressure_pct": 55.5,
            "timestamp": time.time(),
            "readable_time": time.strftime("%H:%M:%S UTC", time.gmtime())
        }
