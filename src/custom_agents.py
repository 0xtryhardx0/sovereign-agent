"""
Custom Trading Agent Engine for Sovereign Agent (The Merrymen Capability).
Enables users to create, customize, and deploy their own autonomous trading agents
with unique strategy styles, risk rules, and auto-Blink syndication.
"""

import time
import uuid
from typing import Dict, Any, List

DEFAULT_AGENTS = [
    {
        "id": "agent-sovereign-alpha",
        "name": "Sovereign Prime",
        "avatar": "⚡",
        "style": "Breakout Momentum",
        "description": "Scans for 5-pillar volume and price velocity breakouts across top Solana liquidity pools.",
        "max_trade_sol": 1.0,
        "stop_loss_pct": 5.0,
        "take_profit_pct": 10.0,
        "auto_blink": True,
        "status": "ACTIVE",
        "created_at": "System Default"
    },
    {
        "id": "agent-merry-scalper",
        "name": "Merry Scalper",
        "avatar": "🏹",
        "style": "High-Frequency Scalp",
        "description": "Specialized in 15m order flow aggression and tight 3% risk/reward scalping.",
        "max_trade_sol": 0.5,
        "stop_loss_pct": 3.0,
        "take_profit_pct": 6.5,
        "auto_blink": True,
        "status": "READY",
        "created_at": "System Preset"
    }
]

class CustomAgentRegistry:
    """
    Registry managing custom user-created AI trading agents.
    """
    def __init__(self):
        self.agents: Dict[str, Dict[str, Any]] = {a["id"]: a for a in DEFAULT_AGENTS}
        self.active_agent_id = "agent-sovereign-alpha"

    def list_agents(self) -> List[Dict[str, Any]]:
        return list(self.agents.values())

    def get_active_agent(self) -> Dict[str, Any]:
        return self.agents.get(self.active_agent_id, DEFAULT_AGENTS[0])

    def set_active_agent(self, agent_id: str) -> bool:
        if agent_id in self.agents:
            self.active_agent_id = agent_id
            return True
        return False

    def create_agent(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a custom AI trading agent configured by the user.
        """
        name = config.get("name", "Custom Alpha Agent").strip()
        style = config.get("style", "Breakout Momentum")
        avatar = config.get("avatar", "🤖")
        max_sol = float(config.get("max_trade_sol", 1.0))
        sl_pct = float(config.get("stop_loss_pct", 5.0))
        tp_pct = float(config.get("take_profit_pct", 10.0))
        auto_blink = bool(config.get("auto_blink", True))
        custom_thesis = config.get("custom_thesis", "Prioritize tokens with positive RSI momentum and locked liquidity.")

        agent_id = f"agent-{uuid.uuid4().hex[:8]}"

        agent = {
            "id": agent_id,
            "name": name,
            "avatar": avatar,
            "style": style,
            "description": custom_thesis,
            "max_trade_sol": max_sol,
            "stop_loss_pct": sl_pct,
            "take_profit_pct": tp_pct,
            "auto_blink": auto_blink,
            "status": "ACTIVE",
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())
        }

        self.agents[agent_id] = agent
        self.active_agent_id = agent_id
        return agent
