"""
Unified NLP Risk Engine Pipeline.
Consumes RawTextItem and outputs StructuredRiskSignal.
"""

from src.ingestion.schemas import RawTextItem, StructuredRiskSignal
from src.engine.entity import EntityExtractor
from src.engine.sentiment import SentimentAnalyzer
from src.engine.event_classifier import EventClassifier
from src.engine.impact import ImpactCalculator

class RiskPipeline:
    """Unified AI/NLP Risk Engine pipeline."""
    
    def __init__(self, use_finbert: bool = True, use_zeroshot: bool = True):
        self.entity_extractor = EntityExtractor()
        self.sentiment_analyzer = SentimentAnalyzer(use_finbert=use_finbert)
        self.event_classifier = EventClassifier(use_hf_zeroshot=use_zeroshot)

    def process_item(self, item: RawTextItem) -> StructuredRiskSignal:
        # 1. Company Detection / Entity Extraction
        company = self.entity_extractor.extract_company(item.text, hint=item.company_hint)
        
        # 2. Sentiment Score
        sentiment_score, sent_conf, sent_model = self.sentiment_analyzer.analyze(item.text)
        
        # 3. Event Classification
        event_type, event_conf, event_model = self.event_classifier.classify(item.text)
        
        # 4. Impact Score & Explanation
        impact_score, explanation = ImpactCalculator.calculate(
            sentiment_score=sentiment_score,
            event_type=event_type,
            source=item.source,
            company=company
        )
        
        # 5. Combined Confidence
        combined_confidence = round((sent_conf + event_conf) / 2.0, 4)
        
        full_explanation = f"{explanation} [Models: {sent_model} | {event_model}]"

        return StructuredRiskSignal(
            id=item.id,
            timestamp=item.timestamp,
            source=item.source,
            text=item.text,
            company=company,
            sentiment_score=sentiment_score,
            event_type=event_type,
            impact_score=impact_score,
            confidence=combined_confidence,
            explanation=full_explanation
        )
