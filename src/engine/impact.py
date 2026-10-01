"""
Transparent Market Severity Impact Score Engine (Scale 1-10).

Formula:
Impact Score = min(10, max(1, round(10 * |sentiment_score| * w_event * w_source * w_entity)))

Weights:
- w_event: Event Severity (Geopolitical: 1.25, Credit Event: 1.30, Regulatory: 1.15, Macroeconomic: 1.15, M&A: 1.05, Earnings: 0.95, Product Launch: 0.85, Other: 0.70)
- w_source: Source Credibility (news: 1.00, twitter: 0.85)
- w_entity: Entity Prominence (Specific S&P 100 Ticker: 1.00, General Market: 0.80)
"""

from typing import Dict, Tuple

EVENT_SEVERITY_WEIGHTS: Dict[str, float] = {
    "Geopolitical": 1.25,
    "Credit Event": 1.30,
    "Regulatory": 1.15,
    "Macroeconomic": 1.15,
    "Merger/Acquisition": 1.05,
    "Earnings": 0.95,
    "Product Launch": 0.85,
    "Other": 0.70
}

SOURCE_CREDIBILITY_WEIGHTS: Dict[str, float] = {
    "news": 1.00,
    "twitter": 0.85
}

class ImpactCalculator:
    """Calculates transparent impact score and text explanation."""

    @staticmethod
    def calculate(sentiment_score: float, event_type: str, source: str, company: str) -> Tuple[int, str]:
        abs_sent = abs(sentiment_score)
        w_event = EVENT_SEVERITY_WEIGHTS.get(event_type, 0.70)
        w_source = SOURCE_CREDIBILITY_WEIGHTS.get(source.lower(), 0.85)
        w_entity = 1.00 if company != "GENERAL" else 0.80
        
        raw_score = 10.0 * abs_sent * w_event * w_source * w_entity
        impact_score = min(10, max(1, int(round(raw_score))))
        
        explanation = (
            f"Impact Score {impact_score}/10 derived from |sentiment|={abs_sent:.2f}, "
            f"event weight ({event_type})={w_event:.2f}, source ({source})={w_source:.2f}, "
            f"entity ({company})={w_entity:.2f}."
        )
        return impact_score, explanation
