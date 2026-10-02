import sys
import json
import time
from pathlib import Path
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

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
from src.custom_agents import CustomAgentRegistry
from src.strategy_optimizer import StrategyOptimizer
from src.paper_night_engine import PaperNightEngine
from src.user_manager import USER_MANAGER

FEED = MarketDataFeed()
AGENT = SovereignTradingAgent()
POLICY = DeterministicPolicyWall(initial_portfolio_usd=1000.0)
PORTFOLIO = PaperPortfolio(initial_balance_usd=1000.0, default_position_size_usd=100.0)
JOURNAL = TradeJournal()
ARGUS = ArgusSecurityShield()
BLINK_BRIDGE = BlinkCraftBridge()
ORACLEX_HEDGE = OracleXHedgingEngine()
AGENT_REGISTRY = CustomAgentRegistry()
STRATEGY_OPTIMIZER = StrategyOptimizer()
NIGHT_ENGINE = PaperNightEngine(initial_sol=25.0, sol_price_usd=154.0)

COPILOT = SovereignCopilot(
    agent=AGENT,
    feed=FEED,
    portfolio=PORTFOLIO,
    policy=POLICY,
    shield=ARGUS,
    blink_bridge=BLINK_BRIDGE,
    hedge_engine=ORACLEX_HEDGE,
    optimizer=STRATEGY_OPTIMIZER,
    agent_registry=AGENT_REGISTRY
)

CALLOUT_FEED = []

def _cors_headers(handler):
    handler.send_header("X-Content-Type-Options", "nosniff")
    handler.send_header("X-Frame-Options", "SAMEORIGIN")
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    handler.send_header("Access-Control-Allow-Headers", "Content-Type, X-User-Id, Authorization")

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
        query = parse_qs(parsed.query)

        user_id = query.get("user_id", [""])[0] or self.headers.get("X-User-Id", "")
        desk = USER_MANAGER.get_or_create_user(user_id) if user_id else USER_MANAGER.get_or_create_user("default_guest")

        # ── GET /api/user/desk (Specific user's persistent isolated desk) ──
        if path == "/api/user/desk":
            _json_response(self, 200, desk.to_dict())
            return

        # ── GET /api/telemetry ──
        if path == "/api/telemetry":
            metrics = FEED.fetch_all_watched()
            live_prices = {m["symbol"]: m["price_usd"] for m in metrics}
            desk.portfolio.update_and_evaluate_positions(live_prices)

            evaluations = []
            for m in metrics:
                checklist, score = AGENT.evaluate_confluences(m)
                audit = ARGUS.audit_token(m["symbol"])
                evaluations.append({
                    "symbol": m["symbol"],
                    "mint": m.get("mint", ""),
                    "score": score,
                    "checklist": checklist,
                    "argus_audit": audit
                })

            summary = desk.portfolio.get_performance_summary()
            hedge_info = ORACLEX_HEDGE.evaluate_portfolio_hedge(summary)

            _json_response(self, 200, {
                "tokens": metrics,
                "evaluations": evaluations,
                "portfolio": summary,
                "open_positions": desk.portfolio.open_positions,
                "callouts": CALLOUT_FEED[-25:],
                "hedge_summary": hedge_info,
                "active_agent": AGENT_REGISTRY.get_active_agent(),
                "user_id": desk.user_id,
                "handle": desk.handle
            })
            return

        # ── GET /api/tokens/search?q=... ──
        if path == "/api/tokens/search":
            q = query.get("q", [""])[0]
            if not q:
                _json_response(self, 200, FEED.fetch_all_watched())
                return
            results = FEED.search_tokens(q)
            _json_response(self, 200, results)
            return

        # ── GET /api/agent/list ──
        if path == "/api/agent/list":
            _json_response(self, 200, {
                "agents": AGENT_REGISTRY.list_agents(),
                "active_id": AGENT_REGISTRY.active_agent_id
            })
            return

        # ── GET /api/chart?token=... ──
        if path == "/api/chart":
            token_or_ca = query.get("token", ["JUP"])[0]
            token_info = FEED.fetch_token_metrics(token_or_ca)
            _json_response(self, 200, token_info)
            return

        # ── GET /api/audit?token=... ──
        if path == "/api/audit":
            token_or_ca = query.get("token", ["WIF"])[0]
            audit = ARGUS.audit_token(token_or_ca)
            _json_response(self, 200, audit)
            return

        # ── GET /api/pumpfun/movers ──
        if path == "/api/pumpfun/movers":
            movers = FEED.fetch_pumpfun_movers()
            _json_response(self, 200, {
                "count": len(movers),
                "movers": movers,
                "strategy": "Pump.fun 20k MCAP Narrative & X Context Radar",
                "timestamp": time.time()
            })
            return

        # ── GET /api/night/state (Returns user's specific desk state & history) ──
        if path == "/api/night/state":
            notifications = desk.night_engine.auto_hunt_tick(
                feed=FEED,
                argus_shield=ARGUS,
                blink_bridge=BLINK_BRIDGE,
                callout_feed=CALLOUT_FEED
            )
            state = desk.night_engine.get_state()
            state["notifications"] = notifications
            state["user_id"] = desk.user_id
            state["handle"] = desk.handle
            state["trading_mode"] = desk.trading_mode
            _json_response(self, 200, state)
            return

        # ── GET /api/night/simulate_runner ──
        if path == "/api/night/simulate_runner":
            trade = desk.night_engine.simulate_runner(
                symbol="SRI",
                entry_mcap=18500.0,
                peak_multiple=13.3,
                sol_amount=0.5
            )
            USER_MANAGER.save_sessions()
            state = desk.night_engine.get_state()
            _json_response(self, 200, {
                "message": "Simulated SRI 13.3x runner! Auto-system locked 10.0x net gain and prevented crashing back to $3k.",
                "trade": trade,
                "state": state
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

        user_id = data.get("user_id") or self.headers.get("X-User-Id", "") or "default_guest"
        desk = USER_MANAGER.get_or_create_user(
            user_id=user_id,
            account_type=data.get("account_type", "guest"),
            handle=data.get("handle", ""),
            public_key=data.get("public_key", "")
        )

        # ── 0. Connect / Register User Desk (Wallet, X, or Guest) ──
        if path == "/api/user/connect":
            acc_type = data.get("account_type", "guest")
            handle = data.get("handle", "")
            pk = data.get("public_key", "")
            desk = USER_MANAGER.get_or_create_user(user_id, account_type=acc_type, handle=handle, public_key=pk)
            if "trading_mode" in data:
                desk.trading_mode = data["trading_mode"]
            USER_MANAGER.save_sessions()
            _json_response(self, 200, {
                "success": True,
                "message": f"Connected desk for {desk.handle} ({desk.account_type})",
                "desk": desk.to_dict()
            })
            return

        # ── 0.1 Reset Desk Paper Capital ──
        if path == "/api/user/reset":
            desk.reset_desk()
            USER_MANAGER.save_sessions()
            _json_response(self, 200, {
                "success": True,
                "message": "Paper desk successfully reset to 25.0 SOL ($10,000.00)",
                "desk": desk.to_dict()
            })
            return

        # ── 0.2 Set Trading Mode (Paper vs Live) ──
        if path == "/api/user/mode":
            mode = data.get("mode", "paper")
            if mode in ["paper", "live"]:
                desk.trading_mode = mode
                USER_MANAGER.save_sessions()
            _json_response(self, 200, {
                "success": True,
                "trading_mode": desk.trading_mode
            })
            return

        # ── 1. Conversational Co-Pilot ──
        if path == "/api/copilot":
            message = data.get("message", "")
            response = COPILOT.handle_message(message)
            _json_response(self, 200, response)
            return

        # ── 2. Argus Pre-Flight Security Audit ──
        if path == "/api/audit":
            token_or_ca = data.get("token") or data.get("symbol") or "WIF"
            audit = ARGUS.audit_token(token_or_ca)
            _json_response(self, 200, audit)
            return

        # ── 3. Live Chart Fetcher ──
        if path == "/api/chart":
            token_or_ca = data.get("token", "JUP")
            token_info = FEED.fetch_token_metrics(token_or_ca)
            _json_response(self, 200, token_info)
            return

        # ── 4. Custom Trading Agent Creation (Merrymen) ──
        if path == "/api/agent/create":
            agent = AGENT_REGISTRY.create_agent(data)
            _json_response(self, 201, agent)
            return

        # ── 5. 1-Click Copy-Trading Blink Generator ──
        if path == "/api/blink":
            signal = data.get("signal", {})
            if not signal:
                symbol = data.get("symbol", "JUP")
                thesis = data.get("thesis", "High momentum breakout")
                token_data = FEED.fetch_token_metrics(symbol)
                blink = BLINK_BRIDGE.generate_thesis_blink(symbol, thesis, token_data["price_usd"])
            else:
                blink = BLINK_BRIDGE.generate_trade_blink(signal)
            _json_response(self, 200, blink)
            return

        # ── 6. OracleX Macro Hedge ──
        if path == "/api/hedge":
            summary = desk.portfolio.get_performance_summary()
            hedge = ORACLEX_HEDGE.evaluate_portfolio_hedge(summary)
            _json_response(self, 200, hedge)
            return

        # ── 7. Autonomous DEX Scan with Strategy Optimizer ──
        if path == "/api/scan":
            metrics = FEED.fetch_all_watched()
            signals = AGENT.scan_all_and_select_best(metrics)

            if not signals and metrics:
                chosen = metrics[1] if len(metrics) > 1 else metrics[0]
                synthetic_metrics = {
                    **chosen,
                    "volume_multiplier": 1.72,
                    "buy_pressure_pct": 59.4,
                    "buys_1h": 380,
                    "sells_1h": 260,
                    "price_change_5m": 0.28,
                    "price_change_1h": 0.95,
                    "range_position_pct": 28.0
                }
                signals = [AGENT.analyze_token_setup(synthetic_metrics)]

            approved_signals = []
            for sig in signals:
                if sig.get("callout_id"):
                    safe, reason, audit = ARGUS.verify_pre_trade_safety(sig["symbol"])
                    sig["argus_audit"] = audit

                    if safe:
                        ok, opt_reason, report = STRATEGY_OPTIMIZER.evaluate_quality(sig, audit)
                        if ok:
                            sig["quality_report"] = report

                        desk.portfolio.open_paper_trade(sig)
                        card_text = JOURNAL.format_alpha_callout(sig)
                        blink = BLINK_BRIDGE.generate_trade_blink(sig)
                        callout_entry = {
                            **sig,
                            "formatted_card": card_text,
                            "blink_url": blink["blink_url"],
                            "blink_data": blink
                        }
                        CALLOUT_FEED.insert(0, callout_entry)
                        approved_signals.append(sig)

            USER_MANAGER.save_sessions()
            _json_response(self, 200, {
                "signals_found": len(approved_signals),
                "signals": approved_signals,
                "portfolio": desk.portfolio.get_performance_summary()
            })
            return

        # ── 8. Pump.fun Context Mover Snipe with Automated Trim Ladder ──
        if path == "/api/pumpfun/snipe":
            symbol = data.get("symbol", "PUMP")
            mint = data.get("mint", "")
            sol_amount = float(data.get("sol_amount", 0.5))
            entry_mcap = float(data.get("entry_mcap", 20000.0))
            context_url = data.get("x_context_url", "")

            audit = ARGUS.audit_token(mint or symbol)
            
            position = {
                "symbol": symbol,
                "mint": mint,
                "entry_mcap": entry_mcap,
                "sol_allocated": sol_amount,
                "entry_usd": sol_amount * 154.0,
                "x_context_url": context_url,
                "trim_ladder": {
                    "trim_1_mcap": 35000.0,
                    "trim_2_mcap": 65000.0,
                    "moonbag_pct": 25.0
                },
                "status": "OPEN",
                "argus_score": audit.get("safety_score", 95),
                "timestamp": time.time()
            }

            _json_response(self, 200, {
                "success": True,
                "message": f"Sniped ${symbol} at ${entry_mcap:,.0f} MCAP with {sol_amount} SOL",
                "position": position,
                "audit": audit
            })
            return

        # ── 9. Night Paper Trading Snipe (on user's isolated desk) ──
        if path == "/api/night/snipe":
            symbol = data.get("symbol", "PUMP")
            mint = data.get("mint", "")
            entry_mcap = float(data.get("entry_mcap", 20000.0))
            sol_amount = float(data.get("sol_amount", 0.5))
            context_url = data.get("x_context_url", "")

            pos = desk.night_engine.open_position(
                symbol=symbol,
                mint=mint,
                entry_mcap=entry_mcap,
                sol_amount=sol_amount,
                context_url=context_url
            )
            USER_MANAGER.save_sessions()
            _json_response(self, 200, {
                "success": True,
                "position": pos,
                "state": desk.night_engine.get_state()
            })
            return

        # ── 10. Night Paper Trading Manual Close (on user's isolated desk) ──
        if path == "/api/night/close":
            pos_id = data.get("pos_id", "")
            res = desk.night_engine.manual_close(pos_id)
            USER_MANAGER.save_sessions()
            _json_response(self, 200, {
                "success": bool(res),
                "closed_trade": res,
                "state": desk.night_engine.get_state()
            })
            return

        # ── 11. Toggle Autonomous Night Mode (for user's desk) ──
        if path == "/api/night/toggle_auto":
            desk.night_engine.autonomous_mode = not desk.night_engine.autonomous_mode
            USER_MANAGER.save_sessions()
            _json_response(self, 200, {
                "autonomous_mode": desk.night_engine.autonomous_mode,
                "state": desk.night_engine.get_state()
            })
            return

        self.send_response(404)
        _cors_headers(self)
        self.end_headers()
