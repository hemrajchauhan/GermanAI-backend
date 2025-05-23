"""
grammar.py
Router for grammar checking endpoints using LanguageTool.
"""

from fastapi import APIRouter
import requests
from app.models.grammar import GrammarRequest
from fastapi import HTTPException

router = APIRouter()

LANGUAGETOOL_API = "http://languagetool:8010/v2/check"

@router.post("/check-grammar")
async def check_grammar(request: GrammarRequest):
    """
    Checks the grammar of the provided German text using LanguageTool.
    """
    try:
        payload = {"text": request.text, "language": "de-DE"}
        response = requests.post(LANGUAGETOOL_API, data=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail="LanguageTool service unavailable.")

