"""
Automated Stress Test Trigger Evaluator.
Triggers stress test ONLY on adverse events:
1. event_type in monitored stress-worthy list (Geopolitical, Macroeconomic, Credit Event, Regulatory)
2. impact_score >= threshold (default 7)
3. sentiment_score <= -0.3 (strictly negative/adverse sentiment)
"""

from typing import Tuple, List, Optional
from src.ingestion.schemas import StructuredRiskSignal

DEFAULT_STRESS_EVENTS = [
    "Geopolitical", "Macroeconomic", "Credit Event", "Regulatory"
]

class StressTrigger:
    """Evaluates whether a risk signal satisfies adverse stress test execution criteria."""

    def __init__(self, threshold: int = 7, allowed_events: Optional[List[str]] = None, max_sentiment: float = -0.3):
        self.threshold = threshold
        self.allowed_events = allowed_events or DEFAULT_STRESS_EVENTS
        self.max_sentiment = max_sentiment

    def evaluate(self, signal: StructuredRiskSignal) -> Tuple[bool, str]:
        # 1. Sentiment check: Must be adverse (sentiment <= -0.3)
        if signal.sentiment_score > self.max_sentiment:
            return False, f"Non-adverse signal (sentiment {signal.sentiment_score:+.2f} > {self.max_sentiment}). Stress tests only trigger on adverse market news."

        # 2. Impact score check
        if signal.impact_score < self.threshold:
            return False, f"Impact score ({signal.impact_score}) below threshold ({self.threshold})."
        
        # 3. Event type check
        if signal.event_type not in self.allowed_events:
            return False, f"Event type '{signal.event_type}' not in stress-worthy adverse event list."

        return True, (
            f"AUTOMATED ADVERSE STRESS TRIGGER ACTIVATED: High Severity Signal Detected! "
            f"[{signal.event_type}] Impact: {signal.impact_score}/10 | Sentiment: {signal.sentiment_score:+.2f} | Ticker: {signal.company}"
        )
