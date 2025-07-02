from pydantic import BaseModel
from typing import Optional

class WordTranslationRequest(BaseModel):
    word: str

class SentenceTranslationRequest(BaseModel):
    sentence: str

class TranslationResponse(BaseModel):
    source: str
    translation: Optional[str] = None
    error: Optional[str] = None