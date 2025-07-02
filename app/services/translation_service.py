from transformers import pipeline
from app.models.translation import (
    WordTranslationRequest,
    SentenceTranslationRequest,
    TranslationResponse,
)

try:
    translator = pipeline("translation", model="Helsinki-NLP/opus-mt-de-en")
except Exception as e:
    translator = None
    load_error = str(e)

def translate_word(request: WordTranslationRequest) -> TranslationResponse:
    """
    Translate a German word to English (max 2 words because of Artikel).
    """
    word = request.word.strip()
    if not word:
        return TranslationResponse(source=word, error="No word provided.")
    # Enforce 1 or 2 words max (e.g., "Katze" or "die Katze")
    if len(word.split()) > 2:
        return TranslationResponse(
            source=word,
            error="Please enter only one word or a noun with its article (max 2 words)."
        )
    if translator is None:
        return TranslationResponse(source=word, error=f"Translation pipeline unavailable: {load_error}")
    try:
        result = translator(word)
        if not result or "translation_text" not in result[0]:
            return TranslationResponse(source=word, error="No translation found.")
        return TranslationResponse(source=word, translation=result[0]["translation_text"])
    except Exception as e:
        return TranslationResponse(source=word, error=f"Translation error: {str(e)}")

def translate_sentence(request: SentenceTranslationRequest, max_words: int = 50) -> TranslationResponse:
    """
    Translate a German sentence to English (with a word limit for resource control).
    """
    sentence = request.sentence.strip()
    if not sentence:
        return TranslationResponse(source=sentence, error="No sentence provided.")
    if len(sentence.split()) > max_words:
        return TranslationResponse(
            source=sentence,
            error=f"Sentence too long (max {max_words} words)."
        )
    if translator is None:
        return TranslationResponse(source=sentence, error=f"Translation pipeline unavailable: {load_error}")
    try:
        result = translator(sentence)
        if not result or "translation_text" not in result[0]:
            return TranslationResponse(source=sentence, error="No translation found.")
        return TranslationResponse(source=sentence, translation=result[0]["translation_text"])
    except Exception as e:
        return TranslationResponse(source=sentence, error=f"Translation error: {str(e)}")