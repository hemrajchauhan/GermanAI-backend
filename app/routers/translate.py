from fastapi import APIRouter, Depends, HTTPException, Query
from app.auth.keycloak import verify_jwt_token
from app.models.llm import TranslateWordResponse, TranslateSentenceResponse, TranslateSentenceRequest
from app.services.llm_service import translate_word_all_meanings, translate_sentence

router = APIRouter(
    dependencies=[Depends(verify_jwt_token)]
)

@router.get("/translate-word/", response_model=TranslateWordResponse)
def translate_word_endpoint(word: str = Query(..., description="German word to translate")):
    result = translate_word_all_meanings(word)
    if "error" in result:
        # 502 = bad upstream, 400 = user input error
        raise HTTPException(status_code=502, detail=result["error"])
    if not result.get("meanings"):
        raise HTTPException(status_code=404, detail="No meanings found.")
    return result


@router.post("/translate-sentence/", response_model=TranslateSentenceResponse)
def translate_sentence_endpoint(request: TranslateSentenceRequest):
    result = translate_sentence(request.sentence)
    if "error" in result:
        if "long" in result["error"]:
            raise HTTPException(status_code=400, detail=result["error"])
        else:
            raise HTTPException(status_code=502, detail=result["error"])
    return result