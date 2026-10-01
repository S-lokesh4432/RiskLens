"""
Unit tests for Core NLP Risk Engine modules.
"""

import pytest
from src.ingestion.schemas import RawTextItem
from src.engine.entity import EntityExtractor
from src.engine.sentiment import SentimentAnalyzer
from src.engine.event_classifier import EventClassifier
from src.engine.impact import ImpactCalculator
from src.engine.pipeline import RiskPipeline

def test_entity_extractor():
    extractor = EntityExtractor()
    assert extractor.extract_company("NVIDIA announced new AI chips today") == "NVDA"
    assert extractor.extract_company("Apple released Vision Pro", hint=None) == "AAPL"
    assert extractor.extract_company("Random market text without company") == "GENERAL"

def test_sentiment_analyzer():
    analyzer = SentimentAnalyzer(use_finbert=False)
    score, conf, model = analyzer.analyze("JPMorgan Chase reports record Q1 earnings beating estimates")
    assert score > 0.0
    assert conf > 0.0

def test_event_classifier():
    classifier = EventClassifier(use_hf_zeroshot=False)
    event, conf, model = classifier.classify("Federal Reserve raises interest rates to curb inflation")
    assert event == "Macroeconomic"

def test_impact_calculator():
    score, exp = ImpactCalculator.calculate(
        sentiment_score=-0.85,
        event_type="Geopolitical",
        source="news",
        company="XOM"
    )
    assert 1 <= score <= 10
    assert score >= 7  # High impact expected for severe geopolitical news
    assert "Impact Score" in exp

def test_risk_pipeline():
    pipeline = RiskPipeline(use_finbert=False, use_zeroshot=False)
    item = RawTextItem(
        id="TEST-001",
        timestamp="2026-03-01 10:00:00",
        source="news",
        text="A major midstream energy contractor defaulted on $500 million in debt obligations",
        company_hint="CVX"
    )
    signal = pipeline.process_item(item)
    assert signal.company == "CVX"
    assert signal.sentiment_score < 0.0
    assert signal.event_type == "Credit Event"
    assert signal.impact_score >= 7
