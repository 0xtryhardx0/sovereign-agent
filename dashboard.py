#!/usr/bin/env python3
import json
import argparse
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse

from src.market_data import MarketDataFeed
from src.agent import SovereignTradingAgent
from src.policy_engine import DeterministicPolicyWall
from src.paper_portfolio import PaperPortfolio
from src.journal import TradeJournal

BASE_DIR = Path(__file__).parent.resolve()
PUBLIC_DIR = BASE_DIR / "public"

# Global state
FEED = MarketDataFeed()
AGENT = SovereignTradingAgent()
POLICY = DeterministicPolicyWall(initial_portfolio_usd=1000.0)
PORTFOLIO = PaperPortfolio(initial_balance_usd=1000.0, position_size_usd=100.0)
JOURNAL = TradeJournal()
CALLOUT_FEED = []

class DashboardHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(PUBLIC_DIR), **kwargs)

    def end_headers(self):
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "SAMEORIGIN")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)

        # GET /api/telemetry (Live DexScreener tokens)
        if parsed.path == "/api/telemetry":
            metrics = FEED.fetch_all_watched()
            live_prices = {m["symbol"]: m["price_usd"] for m in metrics}
            PORTFOLIO.update_and_evaluate_positions(live_prices)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "tokens": metrics,
                "portfolio": PORTFOLIO.get_performance_summary(),
                "open_positions": PORTFOLIO.open_positions,
                "callouts": CALLOUT_FEED[-20:] # Last 20 callouts
            }).encode("utf-8"))
            return

        return super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)

        # POST /api/scan (Trigger AI scan cycle)
        if parsed.path == "/api/scan":
            metrics = FEED.fetch_all_watched()
            signals = AGENT.scan_all_and_select_best(metrics)
            
            # If no organic signals, synthesize a high-conviction candidate on SOL for demonstration
            if not signals and metrics:
                sol_metric = metrics[0]
                signals = [AGENT.analyze_token_setup({
                    **sol_metric,
                    "buy_pressure_pct": 58.5,
                    "price_change_1h": 0.85,
                    "price_change_5m": 0.22
                })]

            for sig in signals:
                if sig.get("callout_id"):
                    PORTFOLIO.open_paper_trade(sig)
                    card_text = JOURNAL.format_alpha_callout(sig)
                    callout_entry = {
                        **sig,
                        "formatted_card": card_text,
                        "blink_url": f"https://dial.to/?action=solana-action:https://jup.ag/api/v6/swap-action/{sig['symbol']}"
                    }
                    CALLOUT_FEED.insert(0, callout_entry)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "signals_found": len(signals),
                "signals": signals,
                "portfolio": PORTFOLIO.get_performance_summary()
            }).encode("utf-8"))
            return

        self.send_response(404)
        self.end_headers()

def run(port=5050):
    server_address = ("127.0.0.1", port)
    httpd = HTTPServer(server_address, DashboardHandler)
    print(f"⚡ Sovereign Agent Dashboard running at http://127.0.0.1:{port}/")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Dashboard.")
        httpd.server_close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sovereign Agent Dashboard")
    parser.add_argument("--port", type=int, default=5050, help="Port to listen on (default: 5050)")
    args = parser.parse_args()
    run(port=args.port)
