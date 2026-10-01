"""
Scenario Shock Library mapping Risk Engine event types to quantitative macro/market shocks.
"""

from typing import Dict, Any

class ScenarioLibrary:
    """Defines parametric shocks based on event type and sentiment severity."""

    @staticmethod
    def get_shocks(event_type: str, sentiment_score: float, company: str = "GENERAL") -> Dict[str, Any]:
        abs_sent = abs(sentiment_score)
        direction = -1.0 if sentiment_score < 0 else 1.0
        
        # Base shock templates scaled by sentiment severity
        if event_type == "Geopolitical":
            return {
                "name": "Geopolitical Escalation & Supply Disruption",
                "equity_shock_pct": -0.12 * abs_sent,
                "commodity_shock_pct": 0.18 * abs_sent,
                "rate_shock_bps": 50 * abs_sent,
                "credit_spread_shock_bps": 150 * abs_sent,
                "pd_multiplier": 1.4,
                "affected_ticker": company
            }
        elif event_type == "Macroeconomic":
            return {
                "name": "Macroeconomic Tightening & Rate Hike",
                "equity_shock_pct": -0.08 * abs_sent,
                "rate_shock_bps": 200 * abs_sent,
                "credit_spread_shock_bps": 100 * abs_sent,
                "pd_multiplier": 1.3,
                "affected_ticker": company
            }
        elif event_type == "Credit Event":
            return {
                "name": "Counterparty Credit Default & Contagion",
                "equity_shock_pct": -0.15 * abs_sent,
                "rate_shock_bps": 25 * abs_sent,
                "credit_spread_shock_bps": 250 * abs_sent,
                "pd_multiplier": 2.2 if company != "GENERAL" else 1.6,
                "lgd_bump": 0.15,
                "affected_ticker": company
            }
        elif event_type == "Regulatory":
            return {
                "name": "Regulatory Action & Compliance Penalty",
                "equity_shock_pct": -0.10 * abs_sent,
                "rate_shock_bps": 0,
                "credit_spread_shock_bps": 75 * abs_sent,
                "pd_multiplier": 1.25,
                "affected_ticker": company
            }
        elif event_type in ["Earnings", "Product Launch", "Merger/Acquisition"]:
            return {
                "name": f"Corporate Action: {event_type}",
                "equity_shock_pct": direction * 0.10 * abs_sent,
                "rate_shock_bps": 0,
                "credit_spread_shock_bps": -25 * direction * abs_sent,
                "pd_multiplier": 1.1 if direction < 0 else 0.9,
                "affected_ticker": company
            }
        else:
            return {
                "name": "General Market Uncertainty",
                "equity_shock_pct": -0.05 * abs_sent,
                "rate_shock_bps": 25 * abs_sent,
                "credit_spread_shock_bps": 50 * abs_sent,
                "pd_multiplier": 1.15,
                "affected_ticker": company
            }
