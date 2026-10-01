"""
Index Component Data Loader for Module A (15 S&P 100 stocks).
"""

import os
import pandas as pd
from typing import List, Dict

TOP15_TICKERS = [
    "NVDA", "AAPL", "MSFT", "GOOGL", "JPM", "BAC", "GS", "XOM",
    "CVX", "PFE", "JNJ", "TSLA", "AMZN", "META", "PG"
]

class IndexDataManager:
    """Manages historical price feeds for 15 top S&P 100 index components."""
    
    def __init__(self, csv_path: str = "data/stock_prices.csv"):
        self.csv_path = csv_path

    def load_price_matrix(self) -> pd.DataFrame:
        if not os.path.exists(self.csv_path):
            raise FileNotFoundError(f"Stock prices CSV not found at {self.csv_path}")
        
        df = pd.read_csv(self.csv_path)
        pivot_df = df.pivot(index="date", columns="ticker", values="close")
        return pivot_df[TOP15_TICKERS].dropna()
