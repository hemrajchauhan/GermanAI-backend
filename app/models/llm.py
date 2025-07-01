from pydantic import BaseModel
from typing import List

class TranslateWordResponse(BaseModel):
    word: str
    meanings: List[str]

class TranslateSentenceRequest(BaseModel):
    sentence: str

class TranslateSentenceResponse(BaseModel):
    sentence: str
    translation: str

class ExampleSentenceResponse(BaseModel):
    word: str
    sentence: str

class VerbFormResponse(BaseModel):
    verb: str
    form: str
    person: str
    result: str

class MCQMeaningResponse(BaseModel):
    word: str
    options: List[str]
    answer: int