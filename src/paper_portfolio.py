import time
from typing import Dict, Any, List

class PaperPortfolio:
    """
    Virtual Ledger and Performance Tracker for Unfunded 'Paper Trading' Mode.
    Simulates real execution without risking funds, while tracking a transparent,
    verifiable public track record of PnL and win rate.
    """
    def __init__(self, initial_balance_usd: float = 1000.0, position_size_usd: float = 100.0):
        self.initial_balance = initial_balance_usd
        self.current_balance = initial_balance_usd
        self.position_size_usd = position_size_usd
        self.open_positions: List[Dict[str, Any]] = []
        self.closed_positions: List[Dict[str, Any]] = []

    def open_paper_trade(self, signal: Dict[str, Any]) -> Dict[str, Any]:
        """Opens a virtual position based on an AI Alpha callout."""
        symbol = signal["symbol"]
        
        # Check if already holding position in this symbol
        for pos in self.open_positions:
            if pos["symbol"] == symbol:
                return {"status": "SKIPPED", "reason": f"Already holding active position in {symbol}."}

        if self.current_balance < self.position_size_usd:
            return {"status": "SKIPPED", "reason": "Insufficient cash balance for position sizing."}

        entry_price = signal["entry_price"]
        shares = self.position_size_usd / entry_price if entry_price > 0 else 0.0

        position = {
            "id": f"POS-{len(self.open_positions) + len(self.closed_positions) + 1:03d}",
            "symbol": symbol,
            "callout_id": signal["callout_id"],
            "entry_time": time.time(),
            "entry_readable": signal["readable_time"],
            "entry_price": entry_price,
            "shares": shares,
            "size_usd": self.position_size_usd,
            "target_price": signal["target_price"],
            "stop_price": signal["stop_price"],
            "current_price": entry_price,
            "unrealized_pnl_usd": 0.0,
            "unrealized_pnl_pct": 0.0,
            "rationale": signal["rationale"]
        }

        self.current_balance -= self.position_size_usd
        self.open_positions.append(position)
        return {"status": "OPENED", "position": position}

    def update_and_evaluate_positions(self, live_prices: Dict[str, float]) -> List[Dict[str, Any]]:
        """
        Updates open positions with latest live prices.
        Automatically triggers TP or SL closures when boundary conditions are met.
        """
        events = []
        still_open = []

        for pos in self.open_positions:
            sym = pos["symbol"]
            curr_price = live_prices.get(sym, pos["current_price"])
            pos["current_price"] = curr_price
            
            pnl_pct = ((curr_price - pos["entry_price"]) / pos["entry_price"]) * 100
            pnl_usd = (curr_price - pos["entry_price"]) * pos["shares"]
            pos["unrealized_pnl_pct"] = round(pnl_pct, 2)
            pos["unrealized_pnl_usd"] = round(pnl_usd, 2)

            # Check Take Profit
            if curr_price >= pos["target_price"]:
                pos["exit_price"] = curr_price
                pos["exit_time"] = time.time()
                pos["exit_readable"] = time.strftime("%H:%M:%S UTC", time.gmtime())
                pos["exit_reason"] = "🎯 TAKE PROFIT HIT"
                pos["realized_pnl_usd"] = round(pnl_usd, 2)
                pos["realized_pnl_pct"] = round(pnl_pct, 2)
                self.current_balance += (pos["size_usd"] + pnl_usd)
                self.closed_positions.append(pos)
                events.append({"event": "TAKE_PROFIT", "position": pos})

            # Check Stop Loss
            elif curr_price <= pos["stop_price"]:
                pos["exit_price"] = curr_price
                pos["exit_time"] = time.time()
                pos["exit_readable"] = time.strftime("%H:%M:%S UTC", time.gmtime())
                pos["exit_reason"] = "🛑 STOP LOSS HIT"
                pos["realized_pnl_usd"] = round(pnl_usd, 2)
                pos["realized_pnl_pct"] = round(pnl_pct, 2)
                self.current_balance += (pos["size_usd"] + pnl_usd)
                self.closed_positions.append(pos)
                events.append({"event": "STOP_LOSS", "position": pos})

            else:
                still_open.append(pos)

        self.open_positions = still_open
        return events

    def get_performance_summary(self) -> Dict[str, Any]:
        """Computes live track record analytics."""
        total_open_value = sum(p["size_usd"] + p["unrealized_pnl_usd"] for p in self.open_positions)
        total_portfolio_usd = self.current_balance + total_open_value
        net_return_usd = total_portfolio_usd - self.initial_balance
        net_return_pct = (net_return_usd / self.initial_balance) * 100

        total_closed = len(self.closed_positions)
        winning_trades = [p for p in self.closed_positions if p.get("realized_pnl_usd", 0) > 0]
        win_rate = (len(winning_trades) / total_closed * 100) if total_closed > 0 else 0.0

        return {
            "initial_balance": self.initial_balance,
            "cash_balance": round(self.current_balance, 2),
            "open_positions_value": round(total_open_value, 2),
            "total_portfolio_usd": round(total_portfolio_usd, 2),
            "net_pnl_usd": round(net_return_usd, 2),
            "net_return_pct": round(net_return_pct, 2),
            "open_count": len(self.open_positions),
            "closed_count": total_closed,
            "win_rate_pct": round(win_rate, 1)
        }
