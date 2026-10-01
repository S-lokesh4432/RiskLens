"""
Signal Logger Daemon for writing structured signals to JSONL and CSV storage.
"""

import os
import json
import pandas as pd
from typing import List
from src.ingestion.schemas import StructuredRiskSignal

JSONL_PATH = "data/signals.jsonl"
CSV_PATH = "data/signals.csv"

class SignalLogger:
    """Persists risk signals into data/signals.jsonl and data/signals.csv."""

    @staticmethod
    def log_signal(signal: StructuredRiskSignal):
        os.makedirs("data", exist_ok=True)
        sig_dict = signal.model_dump()
        
        # Append to JSONL
        with open(JSONL_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(sig_dict) + "\n")

        # Sync/update CSV
        SignalLogger.sync_csv()

    @staticmethod
    def sync_csv():
        if not os.path.exists(JSONL_PATH):
            return
        
        records = []
        with open(JSONL_PATH, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    records.append(json.loads(line))
        
        if records:
            df = pd.DataFrame(records)
            df.to_csv(CSV_PATH, index=False)

    @staticmethod
    def get_all_signals() -> List[dict]:
        if not os.path.exists(JSONL_PATH):
            return []
        records = []
        with open(JSONL_PATH, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    records.append(json.loads(line))
        return records

    @staticmethod
    def get_signals_by_ticker(ticker: str) -> List[dict]:
        all_sig = SignalLogger.get_all_signals()
        return [s for s in all_sig if s.get("company", "").upper() == ticker.upper()]
