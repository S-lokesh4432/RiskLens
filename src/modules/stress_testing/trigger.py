"""
Automated Stress Test Trigger Evaluator.
Triggers stress test ONLY on adverse high-impact risk events:
1. event_type in monitored stress-worthy list (Geopolitical, Macroeconomic, Credit Event, Regulatory)
2. impact_score > threshold (strictly greater than 7)
3. sentiment_score <= -0.3 (strictly adverse/negative sentiment)
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
        reasons = []
        
        # 1. Sentiment check: Must be adverse (sentiment <= -0.3)
        if signal.sentiment_score > self.max_sentiment:
            reasons.append(f"Non-adverse sentiment ({signal.sentiment_score:+.2f} > {self.max_sentiment})")

        # 2. Strict Impact score check (impact_score > threshold)
        if signal.impact_score <= self.threshold:
            reasons.append(f"Impact score ({signal.impact_score}) is not strictly > {self.threshold}")
        
        # 3. Event type check
        if signal.event_type not in self.allowed_events:
            reasons.append(f"Event type '{signal.event_type}' not in monitored stress list {self.allowed_events}")

        if reasons:
            return False, f"Stress trigger criteria not met: {'; '.join(reasons)}."

        return True, (
            f"AUTOMATED ADVERSE STRESS TRIGGER ACTIVATED: High Severity Signal Detected! "
            f"[{signal.event_type}] Impact: {signal.impact_score}/10 | Sentiment: {signal.sentiment_score:+.2f} | Ticker: {signal.company}"
        )

    def is_triggerable(self, signal: StructuredRiskSignal) -> bool:
        """Helper method returning True if signal satisfies all trigger rules."""
        return self.evaluate(signal)[0]
