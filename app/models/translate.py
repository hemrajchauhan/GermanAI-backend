from pydantic import BaseModel
from typing import Optional

class TranslateRequest(BaseModel):
    word: str
    source_language: Optional[str] = "de"   # Default German
    target_language: Optional[str] = "en"   # Default English
