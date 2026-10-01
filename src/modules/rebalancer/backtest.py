"""
Backtest Engine for Tactical Index Rebalancer.
Simulates historical performance: Sentiment Tilt Strategy vs Equal Weight Benchmark.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any

from src.modules.rebalancer.data import IndexDataManager, TOP15_TICKERS
from src.modules.rebalancer.rebalancer import SentimentRebalancer

class IndexBacktester:
    """Backtests sentiment-tilted index against benchmark over historical price data."""
    
    def __init__(self, price_csv: str = "data/stock_prices.csv"):
        self.data_mgr = IndexDataManager(price_csv)
        self.rebalancer = SentimentRebalancer()

    def run_backtest(self, mock_sentiment_dict: Dict[str, float] = None) -> Dict[str, Any]:
        prices_df = self.data_mgr.load_price_matrix()
        daily_returns = prices_df.pct_change().dropna()
        
        tickers = list(prices_df.columns)
        num_days = len(daily_returns)
        
        # Default sentiment if none provided
        if not mock_sentiment_dict:
            mock_sentiment_dict = {
                "NVDA": 0.85, "MSFT": 0.70, "AAPL": 0.50, "JPM": 0.65, "AMZN": 0.40,
                "GOOGL": -0.30, "TSLA": -0.45, "CVX": 0.20, "XOM": 0.35, "PFE": -0.50,
                "BAC": 0.10, "GS": 0.25, "JNJ": -0.15, "META": 0.60, "PG": -0.10
            }
            
        # Equal Weight Allocation
        eq_weights = np.array([1.0 / len(tickers)] * len(tickers))
        
        # Sentiment Tilted Allocation
        tilt_weights_dict = self.rebalancer.calculate_weights(mock_sentiment_dict)
        tilt_weights = np.array([tilt_weights_dict[t] for t in tickers])

        # Daily Portfolio Returns
        eq_daily_ret = daily_returns.values.dot(eq_weights)
        tilt_daily_ret = daily_returns.values.dot(tilt_weights)

        # Cumulative Returns
        eq_cum_ret = np.cumprod(1.0 + eq_daily_ret) - 1.0
        tilt_cum_ret = np.cumprod(1.0 + tilt_daily_ret) - 1.0

        dates = daily_returns.index.tolist()
        
        # Performance Summary Metrics
        eq_total_ret = float(eq_cum_ret[-1])
        tilt_total_ret = float(tilt_cum_ret[-1])
        alpha = tilt_total_ret - eq_total_ret

        eq_sharpe = float((np.mean(eq_daily_ret) / max(np.std(eq_daily_ret), 1e-6)) * np.sqrt(252))
        tilt_sharpe = float((np.mean(tilt_daily_ret) / max(np.std(tilt_daily_ret), 1e-6)) * np.sqrt(252))

        # Weight timeline for visualization
        weight_history = []
        for i, dt in enumerate(dates):
            w_row = {"date": dt}
            w_row.update(tilt_weights_dict)
            weight_history.append(w_row)

        return {
            "summary": {
                "benchmark_return_pct": round(eq_total_ret * 100, 2),
                "strategy_return_pct": round(tilt_total_ret * 100, 2),
                "alpha_outperformance_pct": round(alpha * 100, 2),
                "benchmark_sharpe": round(eq_sharpe, 2),
                "strategy_sharpe": round(tilt_sharpe, 2)
            },
            "tickers": tickers,
            "constituent_weights": tilt_weights_dict,
            "sentiment_scores": mock_sentiment_dict,
            "timeline": {
                "dates": dates,
                "benchmark_cum_returns": [round(float(x)*100, 2) for x in eq_cum_ret],
                "strategy_cum_returns": [round(float(x)*100, 2) for x in tilt_cum_ret]
            },
            "weight_history": weight_history
        }
