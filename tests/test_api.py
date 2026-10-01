"""
Unit tests for FastAPI Service endpoints.
"""

from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"

def test_analyze_endpoint():
    payload = {
        "text": "Microsoft Azure cloud revenue surged 31% beating expectations",
        "source": "news",
        "company_hint": "MSFT"
    }
    response = client.post("/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["company"] == "MSFT"
    assert data["sentiment_score"] > 0
    assert 1 <= data["impact_score"] <= 10

def test_replay_start():
    response = client.post("/replay/start?mode=REPLAY")
    assert response.status_code == 200
    data = response.json()
    assert data["signals_count"] > 0

def test_get_signals():
    response = client.get("/signals")
    assert response.status_code == 200
    signals = response.json()
    assert isinstance(signals, list)
