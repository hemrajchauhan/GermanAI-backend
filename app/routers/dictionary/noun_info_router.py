from fastapi import APIRouter, HTTPException, Query, status
from app.services.noun_info_service import get_noun_info
from app.models.dictionary import NounInfoResponse
from app.models.common import ErrorResponse

router = APIRouter()

@router.get(
    "/noun-info/",
    response_model=NounInfoResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        404: {"model": ErrorResponse, "description": "Noun not found"},
    },
)
def noun_info(noun: str = Query(..., description="German noun")):
    result = get_noun_info(noun)
    if result.error:
        # 404 for not found, 400 for other errors
        raise HTTPException(
            status_code=404 if "No data" in result.error else 400,
            detail=result.error
        )
    return result
