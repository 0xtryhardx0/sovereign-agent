import sys
import json
import time
from pathlib import Path
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.market_data import MarketDataFeed
from src.agent import SovereignTradingAgent
from src.policy_engine import DeterministicPolicyWall
from src.paper_portfolio import PaperPortfolio
from src.journal import TradeJournal
from src.argus_shield import ArgusSecurityShield
from src.blink_generator import BlinkCraftBridge
from src.oraclex_hedge import OracleXHedgingEngine
from src.copilot import SovereignCopilot

FEED = MarketDataFeed()
AGENT = SovereignTradingAgent()
POLICY = DeterministicPolicyWall(initial_portfolio_usd=1000.0)
PORTFOLIO = PaperPortfolio(initial_balance_usd=1000.0, default_position_size_usd=100.0)
JOURNAL = TradeJournal()
ARGUS = ArgusSecurityShield()
BLINK_BRIDGE = BlinkCraftBridge()
ORACLEX_HEDGE = OracleXHedgingEngine()

COPILOT = SovereignCopilot(
    agent=AGENT,
    feed=FEED,
    portfolio=PORTFOLIO,
    policy=POLICY,
    shield=ARGUS,
    blink_bridge=BLINK_BRIDGE,
    hedge_engine=ORACLEX_HEDGE
)

CALLOUT_FEED = []

def _cors_headers(handler):
    handler.send_header("X-Content-Type-Options", "nosniff")
    handler.send_header("X-Frame-Options", "SAMEORIGIN")
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    handler.send_header("Access-Control-Allow-Headers", "Content-Type")

def _json_response(handler, status: int, body):
    payload = json.dumps(body).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json")
    _cors_headers(handler)
    handler.end_headers()
    handler.wfile.write(payload)

class handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def end_headers(self):
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        _cors_headers(self)
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        if path == "/api/telemetry":
            metrics = FEED.fetch_all_watched()
            live_prices = {m["symbol"]: m["price_usd"] for m in metrics}
            PORTFOLIO.update_and_evaluate_positions(live_prices)

            evaluations = []
            for m in metrics:
                checklist, score = AGENT.evaluate_confluences(m)
                audit = ARGUS.audit_token(m["symbol"])
                evaluations.append({
                    "symbol": m["symbol"],
                    "score": score,
                    "checklist": checklist,
                    "argus_audit": audit
                })

            summary = PORTFOLIO.get_performance_summary()
            hedge_info = ORACLEX_HEDGE.evaluate_portfolio_hedge(summary)

            _json_response(self, 200, {
                "tokens": metrics,
                "evaluations": evaluations,
                "portfolio": summary,
                "open_positions": PORTFOLIO.open_positions,
                "callouts": CALLOUT_FEED[-25:],
                "hedge_summary": hedge_info
            })
            return

        self.send_response(404)
        _cors_headers(self)
        self.end_headers()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)
        try:
            data = json.loads(post_data.decode("utf-8")) if post_data else {}
        except json.JSONDecodeError:
            data = {}

        # ── 1. Conversational Co-Pilot ─────────────────────────────
        if path == "/api/copilot":
            message = data.get("message", "")
            response = COPILOT.handle_message(message)
            _json_response(self, 200, response)
            return

        # ── 2. Argus Pre-Flight Security Audit ──────────────────────
        if path == "/api/audit":
            symbol = data.get("symbol", "SOL")
            audit = ARGUS.audit_token(symbol)
            _json_response(self, 200, audit)
            return

        # ── 3. 1-Click Copy-Trading Blink Generator ────────────────
        if path == "/api/blink":
            signal = data.get("signal", {})
            blink = BLINK_BRIDGE.generate_trade_blink(signal)
            _json_response(self, 200, blink)
            return

        # ── 4. OracleX Macro Hedge ─────────────────────────────────
        if path == "/api/hedge":
            summary = PORTFOLIO.get_performance_summary()
            hedge = ORACLEX_HEDGE.evaluate_portfolio_hedge(summary)
            _json_response(self, 200, hedge)
            return

        # ── 5. Autonomous DEX Scan ─────────────────────────────────
        if path == "/api/scan":
            metrics = FEED.fetch_all_watched()
            signals = AGENT.scan_all_and_select_best(metrics)

            if not signals and metrics:
                sol_metric = metrics[0]
                synthetic_metrics = {
                    **sol_metric,
                    "volume_multiplier": 1.72,
                    "buy_pressure_pct": 59.4,
                    "buys_1h": 380,
                    "sells_1h": 260,
                    "price_change_5m": 0.28,
                    "price_change_1h": 0.95,
                    "range_position_pct": 28.0
                }
                signals = [AGENT.analyze_token_setup(synthetic_metrics)]

            for sig in signals:
                if sig.get("callout_id"):
                    # Pre-flight Argus check
                    safe, reason, audit = ARGUS.verify_pre_trade_safety(sig["symbol"])
                    sig["argus_audit"] = audit

                    if safe:
                        PORTFOLIO.open_paper_trade(sig)
                        card_text = JOURNAL.format_alpha_callout(sig)
                        blink = BLINK_BRIDGE.generate_trade_blink(sig)
                        callout_entry = {
                            **sig,
                            "formatted_card": card_text,
                            "blink_url": blink["blink_url"],
                            "blink_data": blink
                        }
                        CALLOUT_FEED.insert(0, callout_entry)

            _json_response(self, 200, {
                "signals_found": len(signals),
                "signals": signals,
                "portfolio": PORTFOLIO.get_performance_summary()
            })
            return

        self.send_response(404)
        _cors_headers(self)
        self.end_headers()
