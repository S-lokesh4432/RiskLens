"""
Company Detection and Entity Extraction for S&P 100 Stocks.
"""

import re
from typing import Optional, Dict

SP100_DICTIONARY: Dict[str, list] = {
    "NVDA": ["NVIDIA", "Nvidia", "NVDA", "$NVDA", "Blackwell"],
    "AAPL": ["Apple", "Apple Inc", "AAPL", "$AAPL", "iPhone", "Vision Pro"],
    "MSFT": ["Microsoft", "MSFT", "$MSFT", "Azure", "Windows"],
    "GOOGL": ["Google", "Alphabet", "GOOGL", "GOOG", "$GOOGL", "$GOOG"],
    "AMZN": ["Amazon", "Amazon.com", "AMZN", "$AMZN", "AWS"],
    "JPM": ["JPMorgan", "JPMorgan Chase", "JPM", "$JPM", "Chase Bank"],
    "BAC": ["Bank of America", "BofA", "BAC", "$BAC"],
    "GS": ["Goldman Sachs", "Goldman", "GS", "$GS"],
    "MS": ["Morgan Stanley", "MS", "$MS"],
    "WFC": ["Wells Fargo", "WFC", "$WFC"],
    "C": ["Citigroup", "Citi", "C", "$C"],
    "XOM": ["ExxonMobil", "Exxon", "XOM", "$XOM"],
    "CVX": ["Chevron", "CVX", "$CVX"],
    "JNJ": ["Johnson & Johnson", "J&J", "JNJ", "$JNJ"],
    "PFE": ["Pfizer", "PFE", "$PFE"],
    "UNH": ["UnitedHealth", "UNH", "$UNH"],
    "TSLA": ["Tesla", "TSLA", "$TSLA", "Elon Musk"],
    "META": ["Meta", "Meta Platforms", "Facebook", "META", "$META"],
    "DIS": ["Disney", "Walt Disney", "DIS", "$DIS"],
    "PG": ["Procter & Gamble", "P&G", "PG", "$PG"]
}

class EntityExtractor:
    """Extracts target company/ticker from text or metadata hint."""
    
    def __init__(self):
        self.dict = SP100_DICTIONARY

    def extract_company(text: str, hint: Optional[str] = None) -> str:
        # Check hint first if valid ticker
        if hint and hint.upper() in self.dict:
            return hint.upper()
        
        # Regex check for cashtags e.g. $NVDA
        cashtag_match = re.search(r'\$([A-Z]{1,5})\b', text)
        if cashtag_match:
            ticker = cashtag_match.group(1)
            if ticker in self.dict:
                return ticker

        # Search for matched keywords in dictionary
        text_lower = text.lower()
        for ticker, keywords in self.dict.items():
            for kw in keywords:
                # Word boundary match
                pattern = r'\b' + re.escape(kw.lower()) + r'\b'
                if re.search(pattern, text_lower):
                    return ticker

        return "GENERAL"
