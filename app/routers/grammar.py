from fastapi import APIRouter
import requests
from app.models.grammar import GrammarRequest

router = APIRouter()

# This line is key! Use the service name and container port.
LANGUAGETOOL_API = "http://languagetool:8010/v2/check"

@router.post("/check-grammar")
async def check_grammar(request: GrammarRequest):
    payload = {"text": request.text, "language": "de-DE"}
    response = requests.post(LANGUAGETOOL_API, data=payload)
    return response.json()
