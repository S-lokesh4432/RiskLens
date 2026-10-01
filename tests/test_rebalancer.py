"""
Unit tests for Downstream Module A (Tactical Index Rebalancer).
"""

import pytest
from src.modules.rebalancer.rebalancer import SentimentRebalancer
from src.modules.rebalancer.backtest import IndexBacktester

def test_sentiment_rebalancer():
    rebalancer = SentimentRebalancer(min_weight=0.02, max_weight=0.15)
    sentiments = {
        "NVDA": 0.90, "MSFT": 0.50, "AAPL": 0.10, "GOOGL": -0.40, "TSLA": -0.80,
        "JPM": 0.60, "BAC": 0.20, "GS": 0.30, "XOM": 0.40, "CVX": 0.10,
        "PFE": -0.30, "JNJ": -0.20, "AMZN": 0.50, "META": 0.70, "PG": -0.10
    }
    weights = rebalancer.calculate_weights(sentiments)
    
    # Check weights sum to ~1.0
    assert abs(sum(weights.values()) - 1.0) < 0.01
    
    # Positive sentiment stock (NVDA) should get higher weight than negative stock (TSLA)
    assert weights["NVDA"] > weights["TSLA"]
    
    # Boundary checks for 15 tickers
    for t, w in weights.items():
        assert w >= 0.02
        assert w <= 0.15

def test_index_backtester():
    backtester = IndexBacktester()
    res = backtester.run_backtest()
    assert "summary" in res
    assert "strategy_return_pct" in res["summary"]
    assert "benchmark_return_pct" in res["summary"]
    assert len(res["timeline"]["dates"]) > 0
