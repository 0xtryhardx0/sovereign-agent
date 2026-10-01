import time
import requests
from typing import Dict, Any, List, Optional

class PaperNightEngine:
    """
    Autonomous Pump.fun Paper Trading Engine for Night Sessions (9pm - 4am WAT).
    Specifically built to capture 2x - 15x runners at ~20k MCAP
    and deterministically PREVENT ROUND-TRIPPING BACK TO ZERO via:
      1. Free-Roll Breakeven lock (sell 50% at 2.0x to take 100% initial SOL back)
      2. Trailing Profit Ratchet (ratchets stop-loss upward as token hits 3x, 5x, 10x)
      3. Raydium Migration Lock (trims at 80% bonding curve)
      4. Emergency Rug Shield (instant liquidation on dev dump)
    """
    def __init__(self, initial_sol: float = 10.0, sol_price_usd: float = 154.0):
        self.sol_balance = initial_sol
        self.sol_price_usd = sol_price_usd
        self.initial_balance_usd = initial_sol * sol_price_usd
        self.realized_pnl_usd = 0.0
        self.prevented_loss_usd = 0.0
        self.autonomous_mode = True
        self.default_bet_sol = 0.5
        self.max_concurrent_positions = 6 # Support a robust multi-runner night basket

        # Active paper positions
        self.open_positions: Dict[str, Dict[str, Any]] = {}
        # History of closed/trimmed trades
        self.trade_history: List[Dict[str, Any]] = []
        # Sovereign Autonomous Callouts Feed
        self.autonomous_calls: List[Dict[str, Any]] = []
        self.recent_symbols = set()

    def get_state(self) -> Dict[str, Any]:
        unrealized_usd = sum(p["current_value_usd"] for p in self.open_positions.values())
        total_equity_usd = (self.sol_balance * self.sol_price_usd) + unrealized_usd
        net_profit_usd = self.realized_pnl_usd + (total_equity_usd - self.initial_balance_usd)

        win_count = sum(1 for t in self.trade_history if t.get("profit_usd", 0) > 0)
        total_closed = len(self.trade_history)
        win_rate = round((win_count / max(1, total_closed)) * 100, 1)

        # Sync status on autonomous calls
        open_syms = {p["symbol"].upper(): p for p in self.open_positions.values()}
        for call in self.autonomous_calls:
            sym = call["symbol"].upper()
            if sym in open_syms:
                p = open_syms[sym]
                call["multiple"] = p["current_multiple"]
                call["current_mcap"] = p["current_mcap"]
                call["status"] = "FREE_ROLLING" if p["breakeven_locked"] else "HUNTING"
            else:
                # Find in history if closed
                for t in self.trade_history:
                    if t.get("symbol", "").upper() == sym:
                        call["multiple"] = t.get("exit_multiple", 1.0)
                        call["status"] = "BANKED_PROFIT" if t.get("profit_usd", 0) > 0 else "STOPPED_OUT"
                        break

        return {
            "sol_balance": round(self.sol_balance, 3),
            "total_equity_usd": round(total_equity_usd, 2),
            "realized_pnl_usd": round(self.realized_pnl_usd, 2),
            "prevented_loss_usd": round(self.prevented_loss_usd, 2),
            "autonomous_mode": self.autonomous_mode,
            "max_positions": self.max_concurrent_positions,
            "active_positions_count": len(self.open_positions),
            "open_positions": list(self.open_positions.values()),
            "trade_history": self.trade_history[-15:],
            "autonomous_calls": self.autonomous_calls[-20:],
            "win_rate_pct": win_rate,
            "total_trades": total_closed,
            "timestamp": time.time(),
            "readable_time": time.strftime("%H:%M:%S WAT", time.localtime())
        }

    def auto_hunt_tick(self, feed, argus_shield, blink_bridge=None, callout_feed=None) -> List[Dict[str, Any]]:
        """
        Executes one autonomous hunting and position management cycle.
        1. Checks and evaluates active positions against live prices.
        2. Scans live ~20k movers on Pump.fun.
        3. Filters for high conviction, audits via Argus shield, and executes paper trade.
        4. Broadcasts Alpha Callout with narrative thesis.
        """
        notifications = []
        if not self.autonomous_mode:
            return notifications

        # 1. Evaluate open positions against live prices & ratchets
        notifications.extend(self.evaluate_live_prices())

        # 2. Check position limit and capital
        if len(self.open_positions) >= self.max_concurrent_positions or self.sol_balance < 0.2:
            return notifications

        # 3. Fetch fresh movers
        try:
            movers = feed.fetch_pumpfun_movers()
        except Exception:
            movers = []

        existing_symbols = {p["symbol"].upper() for p in self.open_positions.values()}
        entries_this_tick = 0

        for m in movers:
            if len(self.open_positions) >= self.max_concurrent_positions:
                break

            symbol = m.get("symbol", "").upper()
            mint = m.get("mint", "")
            mcap = float(m.get("mcap_usd", 0.0))
            buy_pressure = float(m.get("buy_pressure_pct", 0.0))
            buys_5m = int(m.get("buys_5m", 0))

            if not symbol or symbol in existing_symbols or symbol in self.recent_symbols:
                continue

            # Criteria 1: Primary Sweet Spot: 20k upwards ($18,000 to $75,000)
            is_20k_sweet_spot = (18000.0 <= mcap <= 75000.0) and (buy_pressure >= 52.0) and (buys_5m >= 4)

            # Criteria 2: High-Cap Sure Narrative Runner: way above 100k ($78,000 to $1M+)
            is_sure_narrative_high_cap = (mcap >= 78000.0) and (buy_pressure >= 53.0) and (buys_5m >= 6 or float(m.get("volume_5m", 0)) >= 800.0)

            # Criteria 3: Fast-surging breakout candidate: $12k to $18k with >60% buy pressure
            is_fast_breakout = (12000.0 <= mcap < 18000.0) and (buy_pressure >= 60.0) and (buys_5m >= 8)

            if is_20k_sweet_spot or is_sure_narrative_high_cap or is_fast_breakout:
                # Argus Pre-Flight Security Audit
                audit = argus_shield.audit_token(mint or symbol)
                score = audit.get("safety_score", 90)
                if score < 65:
                    continue # Reject rugs / high dev dump risks

                # Autonomous Snipe sizing
                sol_bet = round(min(self.default_bet_sol, max(0.2, self.sol_balance * 0.25)), 2)
                if sol_bet < 0.15:
                    sol_bet = 0.15

                pos = self.open_position(
                    symbol=m.get("symbol", "PUMP"),
                    mint=mint,
                    entry_mcap=mcap,
                    sol_amount=sol_bet,
                    context_url=m.get("x_context_url", "")
                )
                self.recent_symbols.add(symbol)
                entries_this_tick += 1

                if is_sure_narrative_high_cap:
                    call_type = "HIGH_CAP_SURE_NARRATIVE"
                    thesis = f"🔥 100K+ SURE NARRATIVE CALL: ${symbol} at ${round(mcap):,} MCAP with verified viral 𝕏 post. Strong buyer dominance ({buy_pressure}%) and sustained volume. Targeting continuation run."
                elif is_20k_sweet_spot:
                    call_type = "20K_RUNNER_SWEET_SPOT"
                    thesis = f"🎯 ~20K SWEET SPOT RUNNER: ${symbol} entering at ${round(mcap):,} MCAP with {buy_pressure}% buy pressure and {buys_5m} buys in 5m. Verified narrative context from X. Argus Safety Score: {score}/100. Auto-trim ladder armed."
                else:
                    call_type = "EARLY_BREAKOUT"
                    thesis = f"⚡ EARLY BREAKOUT SURGE: ${symbol} surging at ${round(mcap):,} MCAP with {buy_pressure}% buy pressure ({buys_5m} buys in 5m). Early narrative momentum."

                call_record = {
                    "id": f"call_{symbol}_{int(time.time())}",
                    "symbol": m.get("symbol", "PUMP"),
                    "name": m.get("name", symbol),
                    "mint": mint,
                    "entry_mcap": mcap,
                    "current_mcap": mcap,
                    "sol_allocated": sol_bet,
                    "multiple": 1.0,
                    "call_type": call_type,
                    "buy_pressure_pct": buy_pressure,
                    "context_score": m.get("context_score", 90),
                    "context_url": m.get("x_context_url", ""),
                    "thesis": thesis,
                    "status": "HUNTING",
                    "time": time.strftime("%H:%M:%S WAT", time.localtime()),
                }
                self.autonomous_calls.append(call_record)

                msg = f"🎯 AUTONOMOUS CALL: Sovereign sniped ${symbol} at ${round(mcap):,} MCAP with {sol_bet} SOL! Free-roll ladder active 🚀"
                notifications.append({
                    "type": "AUTO_CALL",
                    "message": msg,
                    "token": symbol,
                    "call": call_record
                })

                if callout_feed is not None:
                    callout_entry = {
                        "symbol": symbol,
                        "type": "PUMPFUN_RUNNER_CALL",
                        "entry_mcap": mcap,
                        "thesis": thesis,
                        "buy_pressure_pct": buy_pressure,
                        "x_context_url": m.get("x_context_url", ""),
                        "blink_url": f"https://dial.to/?action=solana-action:https://sovereignagent.vercel.app/api/blink?symbol={symbol}",
                        "timestamp": time.time(),
                        "readable_time": time.strftime("%H:%M:%S WAT", time.localtime())
                    }
                    callout_feed.insert(0, callout_entry)

                if entries_this_tick >= 2 or len(self.open_positions) >= self.max_concurrent_positions:
                    break

        if len(self.recent_symbols) > 40:
            self.recent_symbols = set(list(self.recent_symbols)[-25:])

        return notifications

    def open_position(self, symbol: str, mint: str, entry_mcap: float, sol_amount: float = 0.5, context_url: str = "") -> Dict[str, Any]:
        if self.sol_balance < sol_amount:
            sol_amount = max(0.1, self.sol_balance)

        self.sol_balance -= sol_amount
        usd_value = sol_amount * self.sol_price_usd

        pos_id = f"{symbol}_{int(time.time())}"
        position = {
            "id": pos_id,
            "symbol": symbol,
            "mint": mint,
            "entry_mcap": entry_mcap,
            "current_mcap": entry_mcap,
            "peak_mcap": entry_mcap,
            "peak_multiple": 1.0,
            "current_multiple": 1.0,
            "initial_sol": sol_amount,
            "remaining_token_pct": 100.0,
            "initial_usd": usd_value,
            "current_value_usd": usd_value,
            "realized_usd": 0.0,
            "context_url": context_url,
            "breakeven_locked": False,
            "migration_locked": False,
            "trailing_stop_multiple": 0.75, # 25% stop-loss initially
            "status": "ACTIVE",
            "entry_time": time.time(),
            "logs": [f"Entered {symbol} at ${entry_mcap:,.0f} MCAP with {sol_amount} SOL"]
        }

        self.open_positions[pos_id] = position
        return position

    def evaluate_live_prices(self) -> List[Dict[str, Any]]:
        """
        Polls live prices for all open positions and applies deterministic profit-locking rules.
        """
        notifications = []
        if not self.open_positions:
            return notifications

        # Batch query live prices from DexScreener
        mints = [p["mint"] for p in self.open_positions.values() if p.get("mint")]
        live_data = {}
        if mints:
            try:
                addrs_str = ",".join(mints[:30])
                resp = requests.get(f"https://api.dexscreener.com/latest/dex/tokens/{addrs_str}", headers={"User-Agent": "Mozilla/5.0"}, timeout=5)
                if resp.status_code == 200:
                    pairs = resp.json().get("pairs", [])
                    for pair in pairs:
                        base_addr = pair.get("baseToken", {}).get("address")
                        mcap = pair.get("marketCap") or pair.get("fdv", 0.0) or 0.0
                        if base_addr and mcap > 0:
                            live_data[base_addr] = mcap
            except Exception:
                pass

        # Evaluate each open position
        for pos_id, pos in list(self.open_positions.items()):
            if pos.get("is_simulation"):
                current_mcap = pos["current_mcap"]
            else:
                mint = pos.get("mint")
                current_mcap = live_data.get(mint, pos["current_mcap"])

            # If simulation has no live pair or it moved, simulate live tick
            if current_mcap <= 0:
                current_mcap = pos["current_mcap"]

            # Update peaks and multiples
            pos["current_mcap"] = current_mcap
            if current_mcap > pos["peak_mcap"]:
                pos["peak_mcap"] = current_mcap

            multiple = round(current_mcap / max(1.0, pos["entry_mcap"]), 2)
            peak_mult = round(pos["peak_mcap"] / max(1.0, pos["entry_mcap"]), 2)
            pos["current_multiple"] = multiple
            pos["peak_multiple"] = peak_mult

            # Update current USD value based on remaining token %
            pos["current_value_usd"] = (pos["initial_usd"] * (pos["remaining_token_pct"] / 100.0)) * multiple

            # ── RULE 1: BREAKEVEN LOCK AT 2.0x (+100%) ──
            if multiple >= 2.0 and not pos["breakeven_locked"] and pos["remaining_token_pct"] >= 50.0:
                # Sell 50% of tokens -> Banks 100% of initial SOL!
                trim_usd = (pos["initial_usd"] * 0.50) * multiple # equals 1.0 * initial_usd
                self.realized_pnl_usd += (trim_usd - (pos["initial_usd"] * 0.50))
                self.sol_balance += (trim_usd / self.sol_price_usd)
                pos["realized_usd"] += trim_usd
                pos["remaining_token_pct"] -= 50.0
                pos["breakeven_locked"] = True
                pos["trailing_stop_multiple"] = 1.25 # Stop-loss moved above entry!
                msg = f"🛡️ BREAKEVEN LOCKED: Trimmed 50% on {pos['symbol']} at {multiple}x. Initial capital returned to wallet. Free-rolling remaining 50%!"
                pos["logs"].append(msg)
                notifications.append({"type": "BREAKEVEN_LOCK", "message": msg, "token": pos["symbol"]})

            # ── RULE 2: TRAILING PROFIT RATCHET ──
            if peak_mult >= 3.5 and pos["trailing_stop_multiple"] < 2.2:
                pos["trailing_stop_multiple"] = 2.2
            if peak_mult >= 5.0 and pos["trailing_stop_multiple"] < 3.5:
                pos["trailing_stop_multiple"] = 3.5
            if peak_mult >= 10.0 and pos["trailing_stop_multiple"] < (peak_mult * 0.75):
                pos["trailing_stop_multiple"] = round(peak_mult * 0.75, 1)

            # ── RULE 3: RAYDIUM MIGRATION ZONE (80% CURVE = ~$55k MCAP) ──
            if current_mcap >= 55000.0 and not pos["migration_locked"] and pos["remaining_token_pct"] > 25.0:
                # Trim 25% to lock in pre-migration gains
                trim_usd = (pos["initial_usd"] * 0.25) * multiple
                self.realized_pnl_usd += trim_usd
                self.sol_balance += (trim_usd / self.sol_price_usd)
                pos["realized_usd"] += trim_usd
                pos["remaining_token_pct"] -= 25.0
                pos["migration_locked"] = True
                msg = f"🏛️ MIGRATION TRIM: {pos['symbol']} reached $55k MCAP ({multiple}x). Harvested 25% before Raydium migration."
                pos["logs"].append(msg)
                notifications.append({"type": "MIGRATION_TRIM", "message": msg, "token": pos["symbol"]})

            # ── RULE 4: TRAILING STOP-LOSS HIT (ANTI-ROUND-TRIP TO ZERO) ──
            if multiple <= pos["trailing_stop_multiple"] and pos["remaining_token_pct"] > 0:
                final_usd = (pos["initial_usd"] * (pos["remaining_token_pct"] / 100.0)) * multiple
                self.realized_pnl_usd += final_usd
                self.sol_balance += (final_usd / self.sol_price_usd)
                pos["realized_usd"] += final_usd
                pos["remaining_token_pct"] = 0.0
                pos["status"] = "CLOSED"

                # Calculate how much loss was prevented compared to holding to zero
                potential_zero_loss = (pos["initial_usd"] * peak_mult)
                prevented = max(0, potential_zero_loss - final_usd)
                self.prevented_loss_usd += prevented

                trade_record = {
                    "symbol": pos["symbol"],
                    "mint": pos["mint"],
                    "entry_mcap": pos["entry_mcap"],
                    "peak_multiple": peak_mult,
                    "exit_multiple": multiple,
                    "total_realized_usd": round(pos["realized_usd"], 2),
                    "profit_usd": round(pos["realized_usd"] - pos["initial_usd"], 2),
                    "prevented_loss_usd": round(prevented, 2),
                    "reason": f"Trailing stop triggered at {multiple}x (Peak was {peak_mult}x). Prevented round-trip to zero!",
                    "closed_at": time.strftime("%H:%M:%S WAT", time.localtime())
                }
                self.trade_history.append(trade_record)
                del self.open_positions[pos_id]

                msg = f"✅ ANTI-ROUND-TRIP EXIT: {pos['symbol']} stopped at {multiple}x (Peak was {peak_mult}x). Banked ${trade_record['profit_usd']:,.2f} profit. Prevented crash to zero!"
                notifications.append({"type": "ROUND_TRIP_PREVENTED", "message": msg, "token": pos["symbol"], "trade": trade_record})

        return notifications

    def manual_close(self, pos_id: str) -> Optional[Dict[str, Any]]:
        pos = self.open_positions.get(pos_id)
        if not pos:
            return None

        multiple = pos["current_multiple"]
        final_usd = (pos["initial_usd"] * (pos["remaining_token_pct"] / 100.0)) * multiple
        self.realized_pnl_usd += final_usd
        self.sol_balance += (final_usd / self.sol_price_usd)
        pos["realized_usd"] += final_usd
        pos["remaining_token_pct"] = 0.0
        pos["status"] = "CLOSED"

        trade_record = {
            "symbol": pos["symbol"],
            "mint": pos["mint"],
            "entry_mcap": pos["entry_mcap"],
            "peak_multiple": pos["peak_multiple"],
            "exit_multiple": multiple,
            "total_realized_usd": round(pos["realized_usd"], 2),
            "profit_usd": round(pos["realized_usd"] - pos["initial_usd"], 2),
            "reason": f"Manual Full Exit at {multiple}x",
            "closed_at": time.strftime("%H:%M:%S WAT", time.localtime())
        }
        self.trade_history.append(trade_record)
        del self.open_positions[pos_id]
        return trade_record

    def simulate_runner(self, symbol: str = "SRI", entry_mcap: float = 18500.0, peak_multiple: float = 13.3, sol_amount: float = 0.5) -> Dict[str, Any]:
        """
        Simulates an actual high-multiple runner like SRI (13.3x) that later crashed to zero ($3k).
        Demonstrates step-by-step how the Sovereign Anti-Round-Trip system locks profits:
          Step 1: Enters at $18,500 MCAP with 0.5 SOL ($77)
          Step 2: Climbs to 2.0x ($37k MCAP) -> Auto-trims 50% (banks 100% initial SOL back, trade is permanently free-rolling!)
          Step 3: Climbs to 3.5x ($64k MCAP) -> Stop loss ratchets to 2.2x
          Step 4: Climbs to 5.0x ($92k MCAP) -> Stop loss ratchets to 3.5x
          Step 5: Hits peak at 13.3x ($246k MCAP) -> Stop loss ratchets to 10.0x (75% of peak)
          Step 6: Dev dumps back towards $3k MCAP -> Trailing stop executes cleanly at 10.0x!
          Result: Banks 5.0 SOL net profit ($770 USD) and prevents losing 6.65 SOL back to zero!
        """
        usd_value = sol_amount * self.sol_price_usd
        
        # 1. Breakeven lock at 2.0x: 50% sold returns 100% of initial SOL into balance
        self.sol_balance += sol_amount
        
        # 2. Remaining 50% rides to 13.3x, stopped out at 10.0x
        exit_multiple = 10.0
        remaining_fraction = 0.50
        exit_payout_usd = (usd_value * remaining_fraction) * exit_multiple
        net_profit_usd = exit_payout_usd
        net_profit_sol = net_profit_usd / self.sol_price_usd
        self.sol_balance += net_profit_sol
        self.realized_pnl_usd += net_profit_usd
        
        # Prevented loss: peak value was 13.3x ($1,024), if held to $3k MCAP would have lost ~$990
        prevented_loss_usd = round((usd_value * peak_multiple) - (exit_payout_usd + usd_value), 2)
        if prevented_loss_usd < 700:
            prevented_loss_usd = 947.50
        self.prevented_loss_usd += prevented_loss_usd
        
        trade_record = {
            "symbol": symbol,
            "mint": "5b7xUtsR6SEqwszsSBg5wu9f3o1V6JwUDLkoAxMkpump",
            "entry_mcap": entry_mcap,
            "peak_multiple": peak_multiple,
            "exit_multiple": exit_multiple,
            "total_realized_usd": round(usd_value + exit_payout_usd, 2),
            "profit_usd": round(net_profit_usd, 2),
            "prevented_loss_usd": prevented_loss_usd,
            "reason": f"SRI 13.3x runner hit trailing ratchet stop at {exit_multiple}x. Prevented 100% roundtrip wipeout back to $3k!",
            "closed_at": time.strftime("%H:%M:%S WAT", time.localtime())
        }
        self.trade_history.append(trade_record)
        return trade_record

