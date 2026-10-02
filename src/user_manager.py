import os
import json
import time
from pathlib import Path
from typing import Dict, Any, Optional

from src.paper_night_engine import PaperNightEngine
from src.paper_portfolio import PaperPortfolio

DATA_DIR = Path(__file__).parent.parent / "data"
SESSIONS_FILE = DATA_DIR / "user_sessions.json"

class UserDesk:
    """Represents an isolated trader desk for a user (via Solana wallet, X handle, or Guest ID)."""
    def __init__(self, user_id: str, account_type: str = "guest", handle: str = "", public_key: str = ""):
        self.user_id = user_id
        self.account_type = account_type # "wallet", "x", "guest"
        self.handle = handle or user_id
        self.public_key = public_key
        self.created_at = time.time()
        self.last_active = time.time()
        self.trading_mode = "paper" # "paper" or "live"
        self.career_rank = "INTERN"
        self.career_xp = 25
        
        # Dedicated engine & portfolio instances for complete multi-user isolation
        self.night_engine = PaperNightEngine(initial_sol=25.0, sol_price_usd=154.0)
        self.portfolio = PaperPortfolio(initial_balance_usd=10000.0, default_position_size_usd=1000.0)

    def to_dict(self) -> Dict[str, Any]:
        engine_state = self.night_engine.get_state()
        portfolio_summary = self.portfolio.get_performance_summary()
        
        return {
            "user_id": self.user_id,
            "account_type": self.account_type,
            "handle": self.handle,
            "public_key": self.public_key,
            "created_at": self.created_at,
            "last_active": self.last_active,
            "trading_mode": self.trading_mode,
            "career_rank": self.career_rank,
            "career_xp": self.career_xp,
            "desk_summary": {
                "sol_balance": engine_state["sol_balance"],
                "total_equity_usd": engine_state["total_equity_usd"],
                "realized_pnl_usd": engine_state["realized_pnl_usd"],
                "win_rate_pct": engine_state["win_rate_pct"],
                "total_trades": engine_state["total_trades"],
                "prevented_loss_usd": engine_state["prevented_loss_usd"],
                "open_positions": engine_state["open_positions"],
                "trade_history": engine_state["trade_history"],
                "autonomous_mode": engine_state["autonomous_mode"]
            },
            "portfolio_summary": portfolio_summary
        }

    def reset_desk(self):
        """Resets the user's paper desk back to clean initial capital."""
        self.night_engine = PaperNightEngine(initial_sol=25.0, sol_price_usd=154.0)
        self.portfolio = PaperPortfolio(initial_balance_usd=10000.0, default_position_size_usd=1000.0)
        self.last_active = time.time()


class UserManager:
    """Manages multi-tenant desk isolation across all users."""
    def __init__(self):
        self.users: Dict[str, UserDesk] = {}
        self._load_sessions()

    def _load_sessions(self):
        try:
            DATA_DIR.mkdir(parents=True, exist_ok=True)
            if SESSIONS_FILE.exists():
                with open(SESSIONS_FILE, "r", encoding="utf-8") as f:
                    raw = json.load(f)
                    for uid, udata in raw.items():
                        desk = UserDesk(
                            user_id=uid,
                            account_type=udata.get("account_type", "guest"),
                            handle=udata.get("handle", ""),
                            public_key=udata.get("public_key", "")
                        )
                        desk.trading_mode = udata.get("trading_mode", "paper")
                        desk.career_rank = udata.get("career_rank", "INTERN")
                        desk.career_xp = udata.get("career_xp", 25)
                        
                        # Restore engine trade history if present
                        history = udata.get("desk_summary", {}).get("trade_history", [])
                        desk.night_engine.trade_history = history
                        desk.night_engine.realized_pnl_usd = udata.get("desk_summary", {}).get("realized_pnl_usd", 0.0)
                        desk.night_engine.sol_balance = udata.get("desk_summary", {}).get("sol_balance", 25.0)
                        
                        self.users[uid] = desk
        except Exception as e:
            print(f"[UserManager] Note: Starting with fresh session cache ({e})")

    def save_sessions(self):
        try:
            DATA_DIR.mkdir(parents=True, exist_ok=True)
            serializable = {uid: u.to_dict() for uid, u in self.users.items()}
            with open(SESSIONS_FILE, "w", encoding="utf-8") as f:
                json.dump(serializable, f, indent=2)
        except Exception as e:
            # Fallback for serverless read-only filesystems
            pass

    def get_or_create_user(self, user_id: Optional[str], account_type: str = "guest", handle: str = "", public_key: str = "") -> UserDesk:
        if not user_id or user_id.strip() == "":
            user_id = "default_guest"
        
        user_id = user_id.strip()
        if user_id not in self.users:
            desk = UserDesk(
                user_id=user_id,
                account_type=account_type,
                handle=handle or user_id,
                public_key=public_key
            )
            self.users[user_id] = desk
            self.save_sessions()
        else:
            desk = self.users[user_id]
            if handle:
                desk.handle = handle
            if public_key:
                desk.public_key = public_key
            desk.last_active = time.time()
            
        return desk

    def get_user(self, user_id: str) -> Optional[UserDesk]:
        return self.users.get(user_id)


# Global singleton instance
USER_MANAGER = UserManager()
