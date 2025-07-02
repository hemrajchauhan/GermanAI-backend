from typing import List, Optional
from pydantic import BaseModel
from enum import Enum

class MostUsedWordsResponse(BaseModel):
    count: int
    words: List[str]
    error: Optional[str] = None

class WordFrequencySelection(str, Enum):
    top_100 = "100"
    top_500 = "500"
    top_1000 = "1000"
    top_5000 = "5000"
    top_10000 = "10000"

class WordByRankResponse(BaseModel):
    rank: int
    word: str
    selection: WordFrequencySelection