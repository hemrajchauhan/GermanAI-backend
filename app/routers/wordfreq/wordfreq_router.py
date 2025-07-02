from fastapi import APIRouter, HTTPException
from app.services.wordfreq_service import get_most_used_words, get_word_by_rank
from app.models.wordfreq import WordByRankResponse, WordFrequencySelection, MostUsedWordsResponse
from app.models.common import ErrorResponse

router = APIRouter()

@router.get(
    "/most-used/{selection}",
    response_model=MostUsedWordsResponse,
    responses={400: {"model": ErrorResponse, "description": "Invalid selection"}}
)
def most_used_words(selection: WordFrequencySelection):
    """
    Get a list of the N most-used German words, where N is selected by bucket (100, 500, 1000, etc).
    """
    result = get_most_used_words(selection)
    if result.error:
        raise HTTPException(status_code=400, detail=result.error)
    return result

@router.get(
    "/most-used/{selection}/rank/{rank}",
    response_model=WordByRankResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid selection or rank"},
        404: {"model": ErrorResponse, "description": "Word not found at this rank"}
    }
)
def most_used_word_by_rank(selection: WordFrequencySelection, rank: int):
    """
    Get the word at a specific rank (1-based) in the selected frequency bucket.
    """
    try:
        return get_word_by_rank(selection, rank)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except IndexError:
        raise HTTPException(status_code=404, detail="Rank out of range for this selection.")
