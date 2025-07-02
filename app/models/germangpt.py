from pydantic import BaseModel
from enum import Enum
from typing import Optional

class VerbForm(str, Enum):
    infinitiv = "infinitiv"
    praesens = "praesens"
    praeteritum = "praeteritum"
    perfekt = "perfekt"
    plusquamperfekt = "plusquamperfekt"
    futur1 = "futur1"
    futur2 = "futur2"
    konjunktiv1 = "konjunktiv1"
    konjunktiv2 = "konjunktiv2"
    imperativ = "imperativ"
    partizip1 = "partizip1"
    partizip2 = "partizip2"

class Person(str, Enum):
    ich = "ich"
    du = "du"
    er_sie_es = "er/sie/es"
    wir = "wir"
    ihr = "ihr"
    sie_Sie = "sie/Sie"

class ExampleSentenceRequest(BaseModel):
    word: str

class ExampleSentenceResponse(BaseModel):
    word: str
    sentence: Optional[str] = None
    error: Optional[str] = None

class VerbFormRequest(BaseModel):
    verb: str
    form: VerbForm
    person: Optional[Person] = Person.ich

class VerbFormResponse(BaseModel):
    verb: str
    form: VerbForm
    person: Person
    result: Optional[str] = None
    error: Optional[str] = None
