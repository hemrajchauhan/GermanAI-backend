from fastapi import APIRouter, HTTPException, status
from app.services.dictionary_service import translate_word_all_meanings
from app.models.dictionary import DictionaryMeaningResponse
from app.models.common import ErrorResponse

router = APIRouter()

@router.get(
    "/dictionary/{word}",
    response_model=DictionaryMeaningResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Missing or empty word parameter"},
        404: {"model": ErrorResponse, "description": "Word not found or no meanings"},
    }
)
def get_dictionary_meanings(word: str):
    if not word or not word.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing or empty word parameter."
        )
    result = translate_word_all_meanings(word)
    if result.error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=result.error
        )
    return result