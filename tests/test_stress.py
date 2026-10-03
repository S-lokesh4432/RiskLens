"""
Unit tests for Downstream Module B (Strategic Portfolio Stress Testing).
Checks adverse triggers, financial revaluation, and loss metrics.
"""

import pytest
from src.ingestion.schemas import StructuredRiskSignal
from src.modules.stress_testing.valuation import ValuationModels
from src.modules.stress_testing.trigger import StressTrigger
from src.modules.stress_testing.engine import StressTestEngine

def test_valuation_models():
    # Bond test: positive yield shift reduces bond price
    p_bond = ValuationModels.revalue_bond(1000000.0, duration=5.0, convexity=30.0, dy_bps=150)
    assert p_bond < 1000000.0

    # Loan test: higher PD/LGD increases expected loss, reducing carrying value
    p_loan = ValuationModels.revalue_loan(1000000.0, pd=0.02, lgd=0.40, ead=1000000.0, pd_mult=1.5, lgd_bump=0.10)
    assert p_loan < 1000000.0

    # Equity test: negative equity shock reduces value
    p_eq = ValuationModels.revalue_equity(1000000.0, equity_shock_pct=-0.10)
    assert p_eq == 900000.0

def test_stress_trigger():
    trigger = StressTrigger(threshold=7, max_sentiment=-0.3)
    
    high_adverse_signal = StructuredRiskSignal(
        id="SIG-01",
        timestamp="2026-03-01",
        source="news",
        text="High risk geopolitical crisis escalates in oil shipping lanes",
        company="XOM",
        sentiment_score=-0.80,
        event_type="Geopolitical",
        impact_score=9,
        confidence=0.90,
        explanation="Severe impact"
    )
    is_triggered, msg = trigger.evaluate(high_adverse_signal)
    assert is_triggered is True

    positive_news_signal = StructuredRiskSignal(
        id="SIG-02",
        timestamp="2026-03-01",
        source="news",
        text="Microsoft Azure revenue surged 31% beating expectations",
        company="MSFT",
        sentiment_score=0.85,
        event_type="Earnings",
        impact_score=8,
        confidence=0.90,
        explanation="Positive earnings beat"
    )
    is_triggered, msg = trigger.evaluate(positive_news_signal)
    assert is_triggered is False  # Positive news MUST NOT trigger a financial stress test

def test_stress_engine():
    engine = StressTestEngine()
    signal = StructuredRiskSignal(
        id="SIG-TEST",
        timestamp="2026-03-01",
        source="news",
        text="Default notice for energy provider following debt obligation breach",
        company="CVX",
        sentiment_score=-0.85,
        event_type="Credit Event",
        impact_score=8,
        confidence=0.88,
        explanation="Test credit event"
    )
    res = engine.run_stress_test(signal)
    assert res["triggered"] is True
    assert res["summary"]["total_loss_usd"] > 0
    assert res["summary"]["stressed_total_usd"] < res["summary"]["baseline_total_usd"]
    assert "Loan" in res["by_asset_class"]
