"""
FinBERT Financial Sentiment Analyzer with ultra-fast fallback.
Computes sentiment score = P(pos) - P(neg) in [-1.0, 1.0].
"""

import math
from typing import Dict, Any, Tuple

# Financial Lexicon for deterministic fast fallback
POSITIVE_FINANCIAL_WORDS = {
    "surge", "surging", "record", "beat", "beating", "boost", "growth", "accelerates",
    "profit", "gains", "gain", "breakout", "upgraded", "dividend", "outperform", "efficient",
    "exceeded", "higher", "bullish", "rally", "success", "expanded", "unveils"
}

NEGATIVE_FINANCIAL_WORDS = {
    "decline", "declining", "drop", "default", "bankruptcy", "warning", "investigation",
    "antitrust", "recall", "scrutiny", "loss", "losses", "cut", "downgrade", "crisis",
    "tension", "disruptions", "glitch", "fine", "tensions", "risk", "risks", "inflation",
    "tightening", "blockade", "outage", "lawsuit", "penalty"
}

class SentimentAnalyzer:
    """FinBERT sentiment analyzer with fallback mode for fast CPU execution."""
    
    def __init__(self, use_finbert: bool = True):
        self.use_finbert = use_finbert
        self.tokenizer = None
        self.model = None
        self.model_loaded = False
        
        if use_finbert:
            try:
                from transformers import AutoTokenizer, AutoModelForSequenceClassification
                model_name = "ProsusAI/finbert"
                # Load with local cache if available
                self.tokenizer = AutoTokenizer.from_pretrained(model_name)
                self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
                self.model_loaded = True
                print("[SentimentAnalyzer] Successfully loaded ProsusAI/finbert model.")
            except Exception as e:
                print(f"[SentimentAnalyzer] Note: FinBERT download/load bypassed ({e}). Using financial lexicon analyzer.")
                self.model_loaded = False

    def analyze(self, text: str) -> Tuple[float, float, str]:
        """Returns (sentiment_score, confidence, model_used) where score = P(pos) - P(neg)."""
        if self.model_loaded and self.tokenizer and self.model:
            try:
                import torch
                inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
                with torch.no_grad():
                    outputs = self.model(**inputs)
                    probs = torch.nn.functional.softmax(outputs.logits, dim=-1)[0]
                    # ProsusAI/finbert labels: 0 -> positive, 1 -> negative, 2 -> neutral
                    p_pos = float(probs[0])
                    p_neg = float(probs[1])
                    p_neu = float(probs[2])
                    
                    score = p_pos - p_neg
                    confidence = max(p_pos, p_neg, p_neu)
                    return round(score, 4), round(confidence, 4), "FinBERT (ProsusAI/finbert)"
            except Exception as e:
                pass
        
        # Rule-based / Lexicon fallback
        text_lower = text.lower()
        words = text_lower.split()
        pos_count = sum(1 for w in words if any(pw in w for pw in POSITIVE_FINANCIAL_WORDS))
        neg_count = sum(1 for w in words if any(nw in w for nw in NEGATIVE_FINANCIAL_WORDS))
        
        total = pos_count + neg_count
        if total == 0:
            return 0.0, 0.5, "Financial Lexicon Fallback"
        
        score = (pos_count - neg_count) / max(total, 1)
        confidence = min(0.95, 0.6 + 0.1 * total)
        return round(score, 4), round(confidence, 4), "Financial Lexicon Fallback"
