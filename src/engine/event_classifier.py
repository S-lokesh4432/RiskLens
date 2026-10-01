"""
Zero-Shot Financial Event Classifier (Hugging Face BART MNLI + Financial Keyword Fallback).
Labels: Geopolitical, Macroeconomic, Credit Event, Merger/Acquisition, Product Launch, Regulatory, Earnings, Other.
"""

from typing import Tuple, List, Dict

EVENT_LABELS = [
    "Geopolitical",
    "Macroeconomic",
    "Credit Event",
    "Merger/Acquisition",
    "Product Launch",
    "Regulatory",
    "Earnings",
    "Other"
]

KEYWORD_MAP: Dict[str, List[str]] = {
    "Geopolitical": ["geopolitical", "strait", "hormuz", "war", "conflict", "sanctions", "blockade", "naval", "military", "tensions"],
    "Macroeconomic": ["federal reserve", "inflation", "interest rate", "gdp", "cpi", "macro", "rates", "economic", "central bank", "oil surge", "freight"],
    "Credit Event": ["bankruptcy", "default", "chapter 11", "credit risk", "downgrade", "debt obligation", "restructuring", "leverage", "liquidity", "contagion"],
    "Merger/Acquisition": ["acquire", "acquisition", "merger", "buyout", "takeover", "finalized purchase", "deal"],
    "Product Launch": ["unveils", "unveiled", "announces", "architecture", "product", "launch", "superchip", "recall", "vision pro", "software glitch"],
    "Regulatory": ["fda", "warning letter", "antitrust", "inquiry", "investigation", "eu commission", "compliance", "regulatory", "court", "fine"],
    "Earnings": ["earnings", "q1", "q2", "q3", "q4", "revenue", "profit", "dividend", "quarterly", "beat estimates", "fiscal", "guidance"]
}

class EventClassifier:
    """Classifies unstructured text into financial risk event categories."""
    
    def __init__(self, use_hf_zeroshot: bool = True):
        self.use_hf = use_hf_zeroshot
        self.pipeline = None
        self.pipeline_loaded = False
        
        if use_hf_zeroshot:
            try:
                from transformers import pipeline
                self.pipeline = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
                self.pipeline_loaded = True
                print("[EventClassifier] Successfully loaded facebook/bart-large-mnli zero-shot pipeline.")
            except Exception as e:
                print(f"[EventClassifier] Note: HF zero-shot model bypassed ({e}). Using keyword fallback matcher.")
                self.pipeline_loaded = False

    def classify(self, text: str) -> Tuple[str, float, str]:
        """Returns (event_type, confidence, model_name)."""
        if self.pipeline_loaded and self.pipeline:
            try:
                res = self.pipeline(text, candidate_labels=EVENT_LABELS)
                top_label = res["labels"][0]
                top_score = float(res["scores"][0])
                return top_label, round(top_score, 4), "HF Zero-Shot (BART-MNLI)"
            except Exception:
                pass

        # Rule-based Keyword Fallback
        text_lower = text.lower()
        best_event = "Other"
        max_matches = 0
        
        for event, keywords in KEYWORD_MAP.items():
            matches = sum(1 for kw in keywords if kw in text_lower)
            if matches > max_matches:
                max_matches = matches
                best_event = event

        conf = min(0.95, 0.55 + 0.15 * max_matches) if max_matches > 0 else 0.40
        return best_event, round(conf, 4), "Keyword Rule Fallback"
