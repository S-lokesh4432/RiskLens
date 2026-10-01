"""
Tactical Index Sentiment Tilt Rebalancing Engine.
Tilts portfolio weights based on rolling sentiment with min/max caps and turnover limit.
"""

import numpy as np
import pandas as pd
from typing import Dict, List

class SentimentRebalancer:
    """Calculates sentiment-tilted index weights for 15 constituent stocks."""
    
    def __init__(self, min_weight: float = 0.02, max_weight: float = 0.15, max_turnover: float = 0.10, tilt_sensitivity: float = 0.50):
        self.min_weight = min_weight
        self.max_weight = max_weight
        self.max_turnover = max_turnover
        self.tilt_sensitivity = tilt_sensitivity

    def calculate_weights(self, sentiment_scores: Dict[str, float], prev_weights: Dict[str, float] = None) -> Dict[str, float]:
        tickers = list(sentiment_scores.keys())
        N = len(tickers)
        if N == 0:
            return {}
        
        base_weight = 1.0 / N
        
        # 1. Compute raw tilted weights
        raw_weights = {}
        for t, sent in sentiment_scores.items():
            tilt = 1.0 + (self.tilt_sensitivity * sent)
            raw_weights[t] = max(0.001, base_weight * tilt)
            
        # 2. Normalize raw weights
        total_raw = sum(raw_weights.values())
        norm_weights = {t: w / total_raw for t, w in raw_weights.items()}

        eff_max_weight = max(self.max_weight, 1.0 / N)
        
        # 3. Apply min/max boundary constraints
        bounded_weights = {}
        for t, w in norm_weights.items():
            bounded_weights[t] = min(eff_max_weight, max(self.min_weight, w))
            
        # Re-normalize after capping
        total_bounded = sum(bounded_weights.values())
        final_weights = {t: round(w / total_bounded, 4) for t, w in bounded_weights.items()}

        # 4. Apply turnover limit constraint if previous weights exist
        if prev_weights:
            turnover = sum(abs(final_weights[t] - prev_weights.get(t, base_weight)) for t in tickers)
            if turnover > self.max_turnover:
                scale = self.max_turnover / turnover
                constrained_weights = {}
                for t in tickers:
                    pw = prev_weights.get(t, base_weight)
                    nw = final_weights[t]
                    constrained_weights[t] = pw + (nw - pw) * scale
                
                # Re-normalize
                tot_c = sum(constrained_weights.values())
                final_weights = {t: round(w / tot_c, 4) for t, w in constrained_weights.items()}

        return final_weights
