"""
Unified Portfolio Stress Testing Engine.
Orchestrates portfolio revaluation, asset class/sector loss breakdowns, and waterfall analytics.
"""

import pandas as pd
from typing import Dict, Any, Optional

from src.ingestion.schemas import StructuredRiskSignal
from src.modules.stress_testing.portfolio import PortfolioManager
from src.modules.stress_testing.scenarios import ScenarioLibrary
from src.modules.stress_testing.trigger import StressTrigger
from src.modules.stress_testing.valuation import ValuationModels

class StressTestEngine:
    """Runs stress tests on the wholesale portfolio based on NLP Risk Engine signals."""

    def __init__(self, portfolio_path: str = "data/portfolio.csv", trigger_threshold: int = 7):
        self.pm = PortfolioManager(portfolio_path)
        self.trigger = StressTrigger(threshold=trigger_threshold)

    def run_stress_test(self, signal: StructuredRiskSignal) -> Dict[str, Any]:
        # 1. Evaluate trigger criteria
        triggered, trigger_msg = self.trigger.evaluate(signal)
        
        df = self.pm.load_portfolio()
        shocks = ScenarioLibrary.get_shocks(
            event_type=signal.event_type,
            sentiment_score=signal.sentiment_score,
            company=signal.company
        )
        
        # 2. Apply valuation model asset by asset
        revalued_rows = []
        for idx, row in df.iterrows():
            ac = row["asset_class"]
            sec = row["sector"]
            tkr = row["ticker"]
            val = float(row["current_value_usd"])
            
            # Additional targeted shock if specific company matched
            ticker_match_mult = 1.8 if (shocks["affected_ticker"] != "GENERAL" and tkr == shocks["affected_ticker"]) else 1.0
            
            eq_shock = shocks.get("equity_shock_pct", 0.0) * ticker_match_mult
            rate_bps = shocks.get("rate_shock_bps", 0) + shocks.get("credit_spread_shock_bps", 0)
            pd_mult = shocks.get("pd_multiplier", 1.0) * (1.3 if ticker_match_mult > 1.0 else 1.0)
            lgd_bump = shocks.get("lgd_bump", 0.0)
            
            if ac == "Bond":
                new_val = ValuationModels.revalue_bond(
                    current_val=val,
                    duration=float(row.get("duration", 4.0)),
                    convexity=float(row.get("convexity", 30.0)),
                    dy_bps=rate_bps
                )
            elif ac == "Loan":
                new_val = ValuationModels.revalue_loan(
                    current_val=val,
                    pd=float(row.get("pd", 0.02)),
                    lgd=float(row.get("lgd", 0.40)),
                    ead=float(row.get("ead", val)),
                    pd_mult=pd_mult,
                    lgd_bump=lgd_bump
                )
            elif ac == "Derivative":
                new_val = ValuationModels.revalue_derivative(
                    current_val=val,
                    delta=float(row.get("delta", 0.8)),
                    equity_shock_pct=eq_shock
                )
            else:  # Equity
                new_val = ValuationModels.revalue_equity(
                    current_val=val,
                    equity_shock_pct=eq_shock
                )
            
            pnl = new_val - val
            pnl_pct = (pnl / val) if val > 0 else 0.0
            
            revalued_rows.append({
                "asset_id": row["asset_id"],
                "asset_name": row["asset_name"],
                "asset_class": ac,
                "sector": sec,
                "ticker": tkr,
                "baseline_value_usd": val,
                "stressed_value_usd": new_val,
                "pnl_usd": pnl,
                "pnl_pct": pnl_pct
            })
            
        res_df = pd.DataFrame(revalued_rows)
        
        # 3. Aggregate results
        baseline_total = float(res_df["baseline_value_usd"].sum())
        stressed_total = float(res_df["stressed_value_usd"].sum())
        total_pnl = float(res_df["pnl_usd"].sum())
        total_pnl_pct = (total_pnl / baseline_total) if baseline_total > 0 else 0.0
        
        # Asset class breakdown
        ac_summary = res_df.groupby("asset_class").agg({
            "baseline_value_usd": "sum",
            "stressed_value_usd": "sum",
            "pnl_usd": "sum"
        }).to_dict(orient="index")
        
        # Sector breakdown
        sec_summary = res_df.groupby("sector").agg({
            "baseline_value_usd": "sum",
            "stressed_value_usd": "sum",
            "pnl_usd": "sum"
        }).to_dict(orient="index")

        return {
            "triggered": triggered,
            "trigger_message": trigger_msg,
            "trigger_signal": signal.model_dump(),
            "scenario_name": shocks["name"],
            "summary": {
                "baseline_total_usd": baseline_total,
                "stressed_total_usd": stressed_total,
                "total_loss_usd": abs(total_pnl) if total_pnl < 0 else -total_pnl,
                "loss_pct": abs(total_pnl_pct),
                "var_99_estimate_usd": round(abs(total_pnl) * 1.28, 2)  # Parametric VaR estimate
            },
            "by_asset_class": ac_summary,
            "by_sector": sec_summary,
            "detailed_assets": res_df.to_dict(orient="records")
        }
