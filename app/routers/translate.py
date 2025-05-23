from fastapi import APIRouter
from app.models.translate import TranslateRequest
from app.config import TRANSLATE_API
import requests

router = APIRouter()

@router.post("/translate-word")
async def translate_word(request: TranslateRequest):
    """
    Translates a word using LibreTranslate.
    """
    try:
        payload = {
            "q": request.word,
            "source": request.source_language or "de",
            "target": request.target_language or "en",
            "format": "text"
        }
        response = requests.post(TRANSLATE_API, data=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        return {
            "word": request.word,
            "translation": data.get("translatedText"),
            "source_language": payload["source"],
            "target_language": payload["target"],
            "source": "libretranslate"
        }
    except requests.RequestException:
        return {"error": "LibreTranslate service unavailable"}

@router.get("/translate-languages")
async def translate_languages():
    api_url = TRANSLATE_API.rsplit("/", 1)[0] + "/languages"
    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return {"error": "LibreTranslate service unavailable"}
