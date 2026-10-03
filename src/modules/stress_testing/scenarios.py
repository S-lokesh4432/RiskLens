"""
Scenario Shock Library mapping Risk Engine event types to strictly ADVERSE macro/market shocks.
All shocks reduce portfolio asset values (equities down, rates/spreads up, PD/LGD up).
PD multipliers use additive expansion (1.0 + X * abs_sent) so PD never shrinks under stress.
"""

from typing import Dict, Any

class ScenarioLibrary:
    """Defines parametric shocks based on event type and sentiment severity."""

    @staticmethod
    def get_shocks(event_type: str, sentiment_score: float, company: str = "GENERAL") -> Dict[str, Any]:
        # Sentiment severity scale [0.3, 1.0]
        abs_sent = max(0.3, min(1.0, abs(sentiment_score)))
        
        if event_type == "Geopolitical":
            return {
                "name": "Geopolitical Escalation & Supply Shock",
                "equity_shock_pct": -0.15 * abs_sent,           # -15% * sentiment severity
                "rate_shock_bps": int(75 * abs_sent),            # +75bps rate hike
                "credit_spread_shock_bps": int(175 * abs_sent),  # +175bps spread widening
                "pd_multiplier": 1.0 + (0.50 * abs_sent),        # 1.0 + 50% expansion
                "lgd_bump": 0.10 * abs_sent,                     # LGD increases by up to 10%
                "affected_ticker": company
            }
        elif event_type == "Macroeconomic":
            return {
                "name": "Macroeconomic Tightening & Interest Rate Shock",
                "equity_shock_pct": -0.10 * abs_sent,
                "rate_shock_bps": int(200 * abs_sent),           # +200bps rate shock
                "credit_spread_shock_bps": int(125 * abs_sent),
                "pd_multiplier": 1.0 + (0.40 * abs_sent),        # 1.0 + 40% expansion
                "lgd_bump": 0.05 * abs_sent,
                "affected_ticker": company
            }
        elif event_type == "Credit Event":
            return {
                "name": "Counterparty Credit Default & Contagion",
                "equity_shock_pct": -0.18 * abs_sent,
                "rate_shock_bps": int(35 * abs_sent),
                "credit_spread_shock_bps": int(275 * abs_sent),  # +275bps severe spread jump
                "pd_multiplier": 1.0 + (1.20 * abs_sent) if company != "GENERAL" else 1.0 + (0.70 * abs_sent),
                "lgd_bump": 0.18 * abs_sent,
                "affected_ticker": company
            }
        elif event_type == "Regulatory":
            return {
                "name": "Regulatory Enforcement & Fine Penalty",
                "equity_shock_pct": -0.12 * abs_sent,
                "rate_shock_bps": 0,
                "credit_spread_shock_bps": int(100 * abs_sent),
                "pd_multiplier": 1.0 + (0.30 * abs_sent),
                "lgd_bump": 0.08 * abs_sent,
                "affected_ticker": company
            }
        else: # Default adverse fallback
            return {
                "name": f"Adverse Market Shock ({event_type})",
                "equity_shock_pct": -0.08 * abs_sent,
                "rate_shock_bps": int(50 * abs_sent),
                "credit_spread_shock_bps": int(100 * abs_sent),
                "pd_multiplier": 1.0 + (0.25 * abs_sent),
                "lgd_bump": 0.05 * abs_sent,
                "affected_ticker": company
            }
