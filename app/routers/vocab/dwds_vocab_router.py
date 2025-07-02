from fastapi import APIRouter, HTTPException, Query
from app.models.dictionary import DWDSWordEntry, VocabLevel, VocabPOS
from app.services.dwds_vocab_service import DWDS_VOCAB
from app.models.common import ErrorResponse
from typing import Optional

router = APIRouter()

@router.get(
    "/vocab/word",
    response_model=DWDSWordEntry,
    responses={400: {"model": ErrorResponse}, 404: {"model": ErrorResponse}}
)
def get_vocab_word(
    level: VocabLevel = Query(..., description="Vocabulary level (A1, A2, B1)"),
    index: int = Query(..., description="Zero-based index in filtered list"),
    pos: Optional[VocabPOS] = Query(None, description="Part of speech to filter by (see documentation for options)")
):
    entries = DWDS_VOCAB[level.value]
    if pos:
        filtered = [e for e in entries if e.get("pos", "").lower() == pos.value.lower()]
    else:
        filtered = entries
    if not filtered:
        raise HTTPException(
            status_code=404,
            detail=f"No entries found for level {level.value} and pos '{pos.value if pos else None}'"
        )
    if not (0 <= index < len(filtered)):
        raise HTTPException(
            status_code=404,
            detail=f"Index {index} out of range for {level.value} and pos '{pos.value if pos else None}' (max {len(filtered)-1})"
        )
    return filtered[index]

@router.get(
    "/vocab/word-count",
    responses={400: {"model": ErrorResponse}}
)
def get_vocab_count(
    level: VocabLevel = Query(...),
    pos: Optional[VocabPOS] = Query(None, description="Optional part of speech")
):
    entries = DWDS_VOCAB[level.value]
    if pos:
        filtered = [e for e in entries if e.get("pos", "").lower() == pos.value.lower()]
    else:
        filtered = entries
    return {"level": level.value, "pos": pos.value if pos else None, "count": len(filtered)}
