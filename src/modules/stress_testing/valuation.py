"""
Financial Valuation Models for Wholesale Portfolio Stress Testing.
Strictly adverse revaluation under macro shocks:
- Bond: Duration & Convexity Taylor expansion (rate/spread rise reduces bond price)
- Loan: Expected Loss shift (EL = PD * LGD * EAD; PD/LGD rise increases EL, reducing carrying value)
- Derivative: Delta sensitivity approximation (negative equity shock reduces value)
- Equity: Direct downward shock percentage
"""

import math
from typing import Dict, Any

class ValuationModels:
    """Calculates asset-level value changes under adverse macro shocks."""

    @staticmethod
    def revalue_bond(current_val: float, duration: float, convexity: float, dy_bps: float) -> float:
        """Bond price change via Duration/Convexity Taylor Series: dP = P * (-ModDur * dy + 0.5 * Conv * (dy)^2)"""
        dy = dy_bps / 10000.0  # bps to decimal
        mod_duration = duration / 1.05  # Approximate modified duration assuming 5% yield
        pct_change = (-mod_duration * dy) + (0.5 * convexity * (dy ** 2))
        new_val = max(0.0, current_val * (1.0 + pct_change))
        return round(new_val, 2)

    @staticmethod
    def revalue_loan(current_val: float, pd: float, lgd: float, ead: float, pd_mult: float, lgd_bump: float = 0.0) -> float:
        """Loan value shift based on Expected Loss shift: EL = PD * LGD * EAD"""
        baseline_el = pd * lgd * ead
        stressed_pd = min(0.99, max(pd, pd * pd_mult))
        stressed_lgd = min(0.99, max(lgd, lgd + lgd_bump))
        stressed_el = stressed_pd * stressed_lgd * ead
        
        el_increase = max(0.0, stressed_el - baseline_el)
        new_val = max(0.0, current_val - el_increase)
        return round(new_val, 2)

    @staticmethod
    def revalue_derivative(current_val: float, delta: float, equity_shock_pct: float) -> float:
        """Derivative revaluation via Delta sensitivity: dV = Notional * Delta * equity_shock_pct"""
        # Ensure adverse direction
        adverse_shock = -abs(equity_shock_pct)
        pct_change = delta * adverse_shock
        new_val = max(0.0, current_val * (1.0 + pct_change))
        return round(new_val, 2)

    @staticmethod
    def revalue_equity(current_val: float, equity_shock_pct: float) -> float:
        """Direct equity downward shock model."""
        adverse_shock = -abs(equity_shock_pct)
        new_val = max(0.0, current_val * (1.0 + adverse_shock))
        return round(new_val, 2)
