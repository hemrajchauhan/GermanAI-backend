from wiktionaryparser import WiktionaryParser
from app.models.dictionary import DictionaryMeaningResponse

parser = WiktionaryParser()
parser.set_default_language('german')

def translate_word_all_meanings(word: str) -> DictionaryMeaningResponse:
    """
    Get all possible English meanings of a German word using Wiktionary.
    """
    try:
        entries = parser.fetch(word)
        meanings = []
        for entry in entries:
            for definition in entry.get("definitions", []):
                if definition.get("partOfSpeech", ""):
                    for meaning in definition.get("text", []):
                        if meaning and meaning not in meanings:
                            meanings.append(meaning)
        if not meanings:
            return DictionaryMeaningResponse(
                word=word,
                meanings=[],
                error="No meanings found for the provided word."
            )
        return DictionaryMeaningResponse(word=word, meanings=meanings)
    except Exception as e:
        # You can add logging here for traceability!
        return DictionaryMeaningResponse(
            word=word,
            meanings=[],
            error=f"An error occurred during lookup: {str(e)}"
        )