"""
Portfolio Data Loader & Manager for Wholesale Banking Assets.
"""

import os
import pandas as pd
from typing import List, Dict, Any

class PortfolioManager:
    """Loads and manages wholesale banking portfolio data."""
    
    def __init__(self, csv_path: str = "data/portfolio.csv"):
        self.csv_path = csv_path

    def load_portfolio(self) -> pd.DataFrame:
        if not os.path.exists(self.csv_path):
            raise FileNotFoundError(f"Portfolio file not found at {self.csv_path}")
        return pd.read_csv(self.csv_path)

    def get_summary(self) -> Dict[str, Any]:
        df = self.load_portfolio()
        return {
            "total_assets": len(df),
            "total_value_usd": float(df["current_value_usd"].sum()),
            "by_asset_class": df.groupby("asset_class")["current_value_usd"].sum().to_dict(),
            "by_sector": df.groupby("sector")["current_value_usd"].sum().to_dict()
        }
