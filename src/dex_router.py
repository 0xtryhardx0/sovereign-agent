import time
import requests
from typing import Dict, Any, Optional
from config import NETWORK_CONFIG

class JupiterRouter:
    """
    Interfaces with Jupiter V6 Aggregator API for optimal routing
    across all Solana DEXes (Orca Whirlpools, Raydium, Meteora, Phoenix).
    """
    def __init__(self, is_simulation: bool = True):
        self.is_simulation = is_simulation
        self.quote_endpoint = f"{NETWORK_CONFIG.jupiter_quote_api}/quote"

    def get_swap_quote(
        self,
        input_mint: str,
        output_mint: str,
        amount_lamports: int,
        slippage_bps: int = 50
    ) -> Dict[str, Any]:
        """Fetch real-time routing quote from Jupiter."""
        if self.is_simulation:
            # Deterministic simulation response
            simulated_rate = 145.50 if "EPjF" in output_mint else (1.0 / 145.50)
            out_amount = int(amount_lamports * simulated_rate)
            return {
                "inputMint": input_mint,
                "outputMint": output_mint,
                "inAmount": str(amount_lamports),
                "outAmount": str(out_amount),
                "priceImpactPct": "0.02",
                "marketInfos": [{"label": "Orca Whirlpool (Simulated)"}],
                "slippageBps": slippage_bps
            }

        params = {
            "inputMint": input_mint,
            "outputMint": output_mint,
            "amount": str(amount_lamports),
            "slippageBps": str(slippage_bps)
        }
        try:
            resp = requests.get(self.quote_endpoint, params=params, timeout=5)
            if resp.status_code == 200:
                return resp.json()
            return {"error": f"Quote API returned status {resp.status_code}"}
        except Exception as e:
            return {"error": f"Network exception: {str(e)}"}

    def execute_swap(self, quote: Dict[str, Any], user_public_key: str) -> Dict[str, Any]:
        """Execute swap transaction on Solana."""
        if self.is_simulation:
            # Simulated transaction signature
            sim_tx = f"sim_tx_{int(time.time())}_{user_public_key[:6]}...{user_public_key[-4:]}"
            return {
                "success": True,
                "tx_signature": sim_tx,
                "in_amount": quote.get("inAmount"),
                "out_amount": quote.get("outAmount"),
                "explorer_url": f"https://solscan.io/tx/{sim_tx}?cluster=devnet"
            }
        
        # Real execution placeholder for mainnet/devnet wallet signing
        return {
            "success": False,
            "error": "Live signing requires loaded Keypair in non-simulation mode."
        }
