"""
Data Schemas for Ingestion and Core Signal Pipeline.
"""

from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from datetime import datetime

class RawTextItem(BaseModel):
    """Raw unstructured text item ingested from news or social media."""
    id: str = Field(..., description="Unique identifier for the item")
    timestamp: str = Field(..., description="ISO or standard timestamp string")
    source: str = Field(..., description="Source type: 'news' or 'twitter'")
    text: str = Field(..., description="Full text content or headline + body")
    headline: Optional[str] = Field(None, description="Article headline if available")
    company_hint: Optional[str] = Field(None, description="Optional target ticker or entity hint")
    raw_metadata: Dict[str, Any] = Field(default_factory=dict, description="Raw source metadata")

class StructuredRiskSignal(BaseModel):
    """Structured Risk Signal produced by the NLP Engine."""
    id: str
    timestamp: str
    source: str  # news | twitter
    text: str
    company: str  # Entity extracted ticker e.g. NVDA, JPM
    sentiment_score: float = Field(..., ge=-1.0, le=1.0, description="FinBERT P(pos) - P(neg)")
    event_type: str = Field(..., description="Geopolitical | Macroeconomic | Credit Event | Merger/Acquisition | Product Launch | Regulatory | Earnings | Other")
    impact_score: int = Field(..., ge=1, le=10, description="Predicted market severity 1-10")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Combined classification confidence")
    explanation: str = Field(..., description="Short explanation of impact calculation and drivers")
