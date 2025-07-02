from fastapi import APIRouter, HTTPException, status
from app.models.grammar import GrammarRequest
from app.models.common import ErrorResponse
from app.services.grammar_service import check_grammar

router = APIRouter()

@router.post(
    "/check-grammar",
    responses={
        502: {"model": ErrorResponse, "description": "LanguageTool service unavailable"},
    },
)
async def check_grammar_endpoint(request: GrammarRequest):
    result = check_grammar(request)
    if result is None:
        raise HTTPException(status_code=502, detail="LanguageTool service unavailable.")
    return result