from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class SubLemma(BaseModel):
    lemma: str
    hidx: Optional[str] = None

class DWDSWordEntry(BaseModel):
    articles: Optional[List[str]] = None         # e.g. ["der"], []
    genera: Optional[List[str]] = None           # e.g. ["mask."], []
    onlypl: Optional[str] = None                 # e.g. "nur im Plural"
    pos: Optional[str] = None                    # e.g. "Substantiv", "Verb", etc.
    sch: Optional[List[SubLemma]] = None         # e.g. [{"lemma": "%", "hidx": None}]
    url: Optional[str] = None                    # DWDS entry URL

class DWDSWordListResponse(BaseModel):
    level: str
    entries: List[DWDSWordEntry]

class VocabLevel(str, Enum):
    A1 = "A1"
    A2 = "A2"
    B1 = "B1"

class VocabPOS(str, Enum):
    substantiv = "Substantiv"
    verb = "Verb"
    adjektiv = "Adjektiv"
    adverb = "Adverb"
    praeposition = "Präposition"
    konjunktion = "Konjunktion"
    kardinalzahl = "Kardinalzahl"
    mehrwortausdruck = "Mehrwortausdruck"
    symbol = "Symbol"
    pronomen = "Pronomen"
    indefinitpronomen = "Indefinitpronomen"
    pronominaladverb = "Pronominaladverb"
    affix = "Affix"
    partizipiales_adjektiv = "partizipiales Adjektiv"
    unknown = ""  # fallback for empty or undefined