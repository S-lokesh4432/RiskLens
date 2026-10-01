"""
Automated Stress Test Trigger Evaluator.
Triggers stress test when event_type matches configured rules AND impact_score > threshold.
"""

from typing import Tuple, List, Optional
from src.ingestion.schemas import StructuredRiskSignal

DEFAULT_TRIGGER_EVENTS = [
    "Geopolitical", "Macroeconomic", "Credit Event", "Regulatory", "Earnings", "Merger/Acquisition"
]

class StressTrigger:
    """Evaluates whether a risk signal satisfies stress test execution criteria."""

    def __init__(self, threshold: int = 7, allowed_events: Optional[List[str]] = None):
        self.threshold = threshold
        self.allowed_events = allowed_events or DEFAULT_TRIGGER_EVENTS

    def evaluate(self, signal: StructuredRiskSignal) -> Tuple[bool, str]:
        if signal.impact_score < self.threshold:
            return False, f"Impact score ({signal.impact_score}) below threshold ({self.threshold})."
        
        if signal.event_type not in self.allowed_events:
            return False, f"Event type '{signal.event_type}' not in monitored stress event list."

        return True, (
            f"AUTOMATED TRIGGER ACTIVATED: High Impact Signal Detected! "
            f"[{signal.event_type}] Impact: {signal.impact_score}/10 | Company: {signal.company} | Source: {signal.source}"
        )
