"""
grammar.py
Router for grammar checking endpoints using LanguageTool.
"""

from fastapi import APIRouter, HTTPException
import requests
from app.models.grammar import GrammarRequest
from app.config import LANGUAGETOOL_API  # <-- Import here

router = APIRouter()

@router.post("/check-grammar")
async def check_grammar(request: GrammarRequest):
    try:
        payload = {"text": request.text, "language": "de-DE"}
        response = requests.post(LANGUAGETOOL_API, data=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        raise HTTPException(status_code=502, detail="LanguageTool service unavailable.")

