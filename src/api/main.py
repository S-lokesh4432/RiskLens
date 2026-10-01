"""
FastAPI REST API Service for Unified NLP Risk Engine.
Endpoints:
- GET /              : Health check & system status
- GET /signals       : Query all structured risk signals
- GET /signals/{ticker} : Query risk signals filtered by company ticker
- POST /analyze      : Real-time analysis of custom text item
- POST /replay/start : Trigger batch processing of replay feeds
"""

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import datetime

from src.ingestion.schemas import StructuredRiskSignal, RawTextItem
from src.ingestion.replay import ReplayStreamer
from src.engine.pipeline import RiskPipeline
from src.engine.logger import SignalLogger

app = FastAPI(
    title="S&P Global & Crisil Hackathon - Unified Risk Engine API",
    description="Real-time NLP Risk Extraction Engine REST Service",
    version="1.0.0"
)

pipeline = RiskPipeline(use_finbert=True, use_zeroshot=True)

class AnalyzeRequest(BaseModel):
    text: str = Field(..., description="Unstructured news article or social media text")
    source: str = Field("news", description="Source channel: news or twitter")
    headline: Optional[str] = None
    company_hint: Optional[str] = None

@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "Unified NLP Risk Engine API",
        "version": "1.0.0",
        "timestamp": datetime.datetime.now().isoformat(),
        "endpoints": ["/signals", "/signals/{ticker}", "/analyze", "/replay/start"]
    }

@app.get("/signals", response_model=List[Dict[str, Any]])
def get_signals(limit: int = Query(50, ge=1, le=500)):
    """Retrieve processed structured risk signals."""
    signals = SignalLogger.get_all_signals()
    return signals[-limit:]

@app.get("/signals/{ticker}", response_model=List[Dict[str, Any]])
def get_signals_by_ticker(ticker: str):
    """Retrieve structured risk signals for a specific ticker."""
    signals = SignalLogger.get_signals_by_ticker(ticker)
    if not signals:
        return []
    return signals

@app.post("/analyze", response_model=StructuredRiskSignal)
def analyze_text(req: AnalyzeRequest):
    """Analyze a single text item and produce a structured risk signal."""
    raw_item = RawTextItem(
        id=f"API-{int(datetime.datetime.now().timestamp()*1000)}",
        timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        source=req.source,
        text=req.text,
        headline=req.headline,
        company_hint=req.company_hint
    )
    
    signal = pipeline.process_item(raw_item)
    SignalLogger.log_signal(signal)
    return signal

@app.post("/replay/start")
def start_replay(mode: str = "REPLAY"):
    """Runs ingestion replay and processes all items into signals.jsonl."""
    streamer = ReplayStreamer(mode=mode)
    items = streamer.get_all_items()
    
    processed = []
    for item in items:
        signal = pipeline.process_item(item)
        SignalLogger.log_signal(signal)
        processed.append(signal.model_dump())
        
    return {
        "message": f"Successfully processed {len(processed)} items in {mode} mode.",
        "signals_count": len(processed)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8000, reload=True)
