"""
Replay Stream Manager for Offline / Real-Time Streaming Demonstration.
Merges multi-source feeds (News + Twitter) chronologically and streams items.
"""

from typing import List, Generator
from src.ingestion.base import BaseConnector
from src.ingestion.connectors import NewsCSVConnector, TweetsCSVConnector, NewsAPIConnector
from src.ingestion.schemas import RawTextItem

class ReplayStreamer:
    """Combines news and twitter feeds, sorts chronologically, and streams items."""
    
    def __init__(self, mode: str = "REPLAY", news_csv: str = "data/sample_news.csv", tweets_csv: str = "data/sample_tweets.csv"):
        self.mode = mode
        self.connectors: List[BaseConnector] = []
        
        if mode == "LIVE":
            self.connectors.append(NewsAPIConnector())
            self.connectors.append(TweetsCSVConnector(tweets_csv))
        else:
            self.connectors.append(NewsCSVConnector(news_csv))
            self.connectors.append(TweetsCSVConnector(tweets_csv))

    def get_all_items(self) -> List[RawTextItem]:
        all_items: List[RawTextItem] = []
        for conn in self.connectors:
            all_items.extend(conn.fetch_items())
        
        # Sort chronologically by timestamp
        all_items.sort(key=lambda x: str(x.timestamp))
        return all_items

    def stream(self, delay_seconds: float = 0.5) -> Generator[RawTextItem, None, None]:
        items = self.get_all_items()
        for item in items:
            yield item
