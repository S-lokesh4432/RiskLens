"""
Concrete Ingestion Connectors for Financial News, Tweets, and NewsAPI.
"""

import os
import time
import pandas as pd
import requests
import uuid
from typing import List, Generator, Optional
from dotenv import load_dotenv

from src.ingestion.base import BaseConnector
from src.ingestion.schemas import RawTextItem

load_dotenv()

class NewsCSVConnector(BaseConnector):
    """Ingests news articles from CSV dataset."""
    
    def __init__(self, csv_path: str = "data/sample_news.csv"):
        self.csv_path = csv_path

    def fetch_items(self) -> List[RawTextItem]:
        if not os.path.exists(self.csv_path):
            return []
        
        df = pd.read_csv(self.csv_path)
        items = []
        for idx, row in df.iterrows():
            item_id = f"NEWS-{idx+1:04d}"
            text_full = f"{row['headline']}. {row['text']}" if 'headline' in row and pd.notna(row['headline']) else str(row['text'])
            items.append(RawTextItem(
                id=item_id,
                timestamp=str(row['timestamp']),
                source="news",
                text=text_full,
                headline=str(row['headline']) if 'headline' in row and pd.notna(row['headline']) else None,
                company_hint=str(row['company']) if 'company' in row and pd.notna(row['company']) else None,
                raw_metadata=row.to_dict()
            ))
        return items

    def stream_items(self, delay_seconds: float = 0.5) -> Generator[RawTextItem, None, None]:
        items = self.fetch_items()
        for item in items:
            yield item
            time.sleep(delay_seconds)


class TweetsCSVConnector(BaseConnector):
    """Ingests tweets from stock tweets CSV dataset."""
    
    def __init__(self, csv_path: str = "data/sample_tweets.csv"):
        self.csv_path = csv_path

    def fetch_items(self) -> List[RawTextItem]:
        if not os.path.exists(self.csv_path):
            return []
        
        df = pd.read_csv(self.csv_path)
        items = []
        for idx, row in df.iterrows():
            item_id = f"TWEET-{idx+1:04d}"
            items.append(RawTextItem(
                id=item_id,
                timestamp=str(row['timestamp']),
                source="twitter",
                text=str(row['text']),
                company_hint=str(row['company']) if 'company' in row and pd.notna(row['company']) else None,
                raw_metadata=row.to_dict()
            ))
        return items

    def stream_items(self, delay_seconds: float = 0.5) -> Generator[RawTextItem, None, None]:
        items = self.fetch_items()
        for item in items:
            yield item
            time.sleep(delay_seconds)


class NewsAPIConnector(BaseConnector):
    """Fetches real-time live financial news from NewsAPI. Falls back to NewsCSVConnector if key missing/invalid."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("NEWSAPI_KEY")
        self.fallback = NewsCSVConnector()

    def fetch_items(self) -> List[RawTextItem]:
        if not self.api_key or self.api_key == "your_newsapi_key_here":
            print("[NewsAPIConnector] No valid NEWSAPI_KEY found in environment. Falling back to CSV REPLAY mode.")
            return self.fallback.fetch_items()
        
        url = f"https://newsapi.org/v2/everything?q=stocks+OR+earnings+OR+fed&language=en&sortBy=publishedAt&pageSize=15&apiKey={self.api_key}"
        try:
            res = requests.get(url, timeout=5)
            if res.status_code == 200:
                data = res.json()
                articles = data.get("articles", [])
                items = []
                for idx, art in enumerate(articles):
                    title = art.get("title", "")
                    desc = art.get("description", "") or ""
                    full_text = f"{title}. {desc}"
                    items.append(RawTextItem(
                        id=f"LIVE-{idx+1:04d}",
                        timestamp=art.get("publishedAt", time.strftime("%Y-%m-%d %H:%M:%S")),
                        source="news",
                        text=full_text,
                        headline=title,
                        raw_metadata=art
                    ))
                return items
            else:
                print(f"[NewsAPIConnector] API HTTP {res.status_code}. Falling back to CSV.")
                return self.fallback.fetch_items()
        except Exception as e:
            print(f"[NewsAPIConnector] Request failed: {e}. Falling back to CSV.")
            return self.fallback.fetch_items()

    def stream_items(self, delay_seconds: float = 0.5) -> Generator[RawTextItem, None, None]:
        items = self.fetch_items()
        for item in items:
            yield item
            time.sleep(delay_seconds)
