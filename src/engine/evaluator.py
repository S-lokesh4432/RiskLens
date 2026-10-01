"""
Evaluation Engine for NLP Risk Engine.
Compares FinBERT Engine vs VADER/Lexicon Baseline against ground-truth labels.
Computes Accuracy, Precision, Recall, F1 Score, and Event Classification accuracy.
"""

import os
import json
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

from src.ingestion.schemas import RawTextItem
from src.engine.pipeline import RiskPipeline
from src.engine.sentiment import SentimentAnalyzer

class ModelEvaluator:
    """Evaluates sentiment and event classification models against ground truth."""
    
    def __init__(self):
        self.pipeline = RiskPipeline(use_finbert=True, use_zeroshot=True)
        self.baseline = SentimentAnalyzer(use_finbert=False)

    def run_evaluation(self, news_csv: str = "data/sample_news.csv", tweets_csv: str = "data/sample_tweets.csv") -> dict:
        records = []
        if os.path.exists(news_csv):
            df_news = pd.read_csv(news_csv)
            records.extend(df_news.to_dict(orient="records"))
        if os.path.exists(tweets_csv):
            df_tweets = pd.read_csv(tweets_csv)
            records.extend(df_tweets.to_dict(orient="records"))

        if not records:
            return {"error": "No ground truth dataset found"}

        y_true_sent = []
        y_pred_finbert = []
        y_pred_baseline = []
        
        y_true_event = []
        y_pred_event = []

        for r in records:
            text = f"{r.get('headline', '')}. {r.get('text', '')}" if r.get('headline') and pd.notna(r.get('headline')) else str(r['text'])
            gt_sent = str(r['ground_truth_sentiment']).lower()
            gt_event = str(r['ground_truth_event'])

            # Engine Prediction
            raw_item = RawTextItem(
                id="EVAL",
                timestamp=str(r.get('timestamp', '2026-03-01 00:00:00')),
                source=str(r.get('source', 'news')),
                text=text,
                company_hint=str(r['company']) if pd.notna(r.get('company')) else None
            )
            sig = self.pipeline.process_item(raw_item)
            
            # Map sentiment float score to class
            if sig.sentiment_score > 0.05:
                pred_sent = "positive"
            elif sig.sentiment_score < -0.05:
                pred_sent = "negative"
            else:
                pred_sent = "neutral"

            # Baseline Prediction
            base_score, _, _ = self.baseline.analyze(text)
            if base_score > 0.05:
                base_sent = "positive"
            elif base_score < -0.05:
                base_sent = "negative"
            else:
                base_sent = "neutral"

            y_true_sent.append(gt_sent)
            y_pred_finbert.append(pred_sent)
            y_pred_baseline.append(base_sent)

            y_true_event.append(gt_event)
            y_pred_event.append(sig.event_type)

        # Compute Sentiment Metrics (FinBERT Engine)
        acc_fb = accuracy_score(y_true_sent, y_pred_finbert)
        p_fb, r_fb, f1_fb, _ = precision_recall_fscore_support(y_true_sent, y_pred_finbert, average="weighted", zero_division=0)

        # Compute Sentiment Metrics (Baseline)
        acc_base = accuracy_score(y_true_sent, y_pred_baseline)
        p_base, r_base, f1_base, _ = precision_recall_fscore_support(y_true_sent, y_pred_baseline, average="weighted", zero_division=0)

        # Compute Event Metrics
        acc_event = accuracy_score(y_true_event, y_pred_event)

        results = {
            "total_samples": len(records),
            "finbert_engine": {
                "accuracy": round(float(acc_fb), 4),
                "precision": round(float(p_fb), 4),
                "recall": round(float(r_fb), 4),
                "f1_score": round(float(f1_fb), 4)
            },
            "vader_baseline": {
                "accuracy": round(float(acc_base), 4),
                "precision": round(float(p_base), 4),
                "recall": round(float(r_base), 4),
                "f1_score": round(float(f1_base), 4)
            },
            "event_classifier": {
                "accuracy": round(float(acc_event), 4)
            },
            "improvement_vs_baseline": f"{((acc_fb - acc_base) / max(acc_base, 0.01))*100:.1f}%"
        }

        os.makedirs("data", exist_ok=True)
        with open("data/eval_results.json", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)

        return results
