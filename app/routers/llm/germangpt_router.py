from fastapi import APIRouter, HTTPException, Query, status
from app.models.germangpt import (
    ExampleSentenceRequest,
    ExampleSentenceResponse,
    VerbFormRequest,
    VerbFormResponse,
    VerbForm,
    Person,
)
from app.models.common import ErrorResponse
from app.services.germangpt_service import generate_sentence, get_verb_form

router = APIRouter()

@router.get(
    "/example-sentence/",
    response_model=ExampleSentenceResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        502: {"model": ErrorResponse, "description": "Model Error"},
        503: {"model": ErrorResponse, "description": "Model Unavailable"},
    },
)
def example_sentence(
    word: str = Query(..., description="Word to use in the German example sentence"),
):
    result = generate_sentence(ExampleSentenceRequest(word=word))
    if result.error:
        detail = result.error.lower()
        if "unavailable" in detail:
            raise HTTPException(status_code=503, detail=result.error)
        elif "generation error" in detail:
            raise HTTPException(status_code=502, detail=result.error)
        else:
            raise HTTPException(status_code=400, detail=result.error)
    return result

@router.get(
    "/verb-form/",
    response_model=VerbFormResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        502: {"model": ErrorResponse, "description": "Model Error"},
        503: {"model": ErrorResponse, "description": "Model Unavailable"},
    },
)
def verb_form(
    verb: str = Query(..., description="German verb in any form (e.g., gehen)"),
    form: VerbForm = Query(..., description="Verb form"),
    person: Person = Query(Person.ich, description="Person for conjugation"),
):
    result = get_verb_form(VerbFormRequest(verb=verb, form=form, person=person))
    if result.error:
        detail = result.error.lower()
        if "unknown or unsupported" in detail:
            raise HTTPException(status_code=400, detail=result.error)
        elif "unavailable" in detail:
            raise HTTPException(status_code=503, detail=result.error)
        elif "generation error" in detail:
            raise HTTPException(status_code=502, detail=result.error)
        else:
            raise HTTPException(status_code=400, detail=result.error)
    return result
