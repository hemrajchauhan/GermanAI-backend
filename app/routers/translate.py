from fastapi import APIRouter
import json
from pathlib import Path
from app.models.translate import TranslateRequest

router = APIRouter()

DICT_PATH = Path(__file__).parent.parent / "static" / "dictionary.json"

with open(DICT_PATH, encoding="utf-8") as f:
    DICTIONARY = json.load(f)

@router.post("/translate-word")
async def translate_word(request: TranslateRequest):
    word = request.word.lower()
    entry = DICTIONARY.get(word)
    if entry:
        # For future: filter by part_of_speech, etc.
        return entry
    return {"error": "Word not found"}
