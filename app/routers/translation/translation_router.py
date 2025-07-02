from fastapi import APIRouter, HTTPException, status
from app.models.translation import (
    WordTranslationRequest,
    SentenceTranslationRequest,
    TranslationResponse,
)
from app.models.common import ErrorResponse
from app.services.translation_service import translate_word, translate_sentence

router = APIRouter()

@router.post(
    "/translate/word",
    response_model=TranslationResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        503: {"model": ErrorResponse, "description": "Translation Service Unavailable"},
    },
)
def translate_word_endpoint(req: WordTranslationRequest):
    if not req.word or not req.word.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No word provided."
        )
    result = translate_word(req)
    if result.error:
        if "pipeline unavailable" in result.error.lower():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=result.error
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.error
            )
    return result

@router.post(
    "/translate/sentence",
    response_model=TranslationResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        503: {"model": ErrorResponse, "description": "Translation Service Unavailable"},
    },
)
def translate_sentence_endpoint(req: SentenceTranslationRequest):
    if not req.sentence or not req.sentence.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No sentence provided."
        )
    if len(req.sentence.strip().split()) > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sentence too long (max 100 words)."
        )
    result = translate_sentence(req)
    if result.error:
        if "pipeline unavailable" in result.error.lower():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=result.error
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.error
            )
    return result