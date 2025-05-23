from pydantic import BaseModel
from typing import Optional

class TranslateRequest(BaseModel):
    word: str
    part_of_speech: Optional[str] = None
    language: Optional[str] = "de"
