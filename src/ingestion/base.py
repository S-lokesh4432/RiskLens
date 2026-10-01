"""
Abstract Base Class for Data Ingestion Connectors.
"""

from abc import ABC, abstractmethod
from typing import List, Generator
from src.ingestion.schemas import RawTextItem

class BaseConnector(ABC):
    """Abstract interface for all data connectors (News CSV, Twitter CSV, NewsAPI, GDELT, etc.)."""
    
    @abstractmethod
    def fetch_items(self) -> List[RawTextItem]:
        """Fetch all available items from source."""
        pass

    @abstractmethod
    def stream_items(self, delay_seconds: float = 0.5) -> Generator[RawTextItem, None, None]:
        """Stream items sequentially with a simulated delay."""
        pass
