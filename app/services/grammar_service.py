import requests
from app.models.grammar import GrammarRequest
from app.config import LANGUAGETOOL_API

def check_grammar(request: GrammarRequest):
    payload = {"text": request.text, "language": "de-DE"}
    try:
        response = requests.post(LANGUAGETOOL_API, data=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None