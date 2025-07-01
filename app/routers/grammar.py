from fastapi import APIRouter, Depends, HTTPException, Query
import requests
from app.auth.keycloak import verify_jwt_token
from app.models.grammar import GrammarRequest
from app.config import LANGUAGETOOL_API
from app.models.llm import ExampleSentenceResponse, VerbFormResponse, MCQMeaningResponse
from app.models.verb_form_enum import VerbForm
from app.models.person_enum import Person
from app.services.llm_service import generate_sentence, get_verb_form, generate_mcq_meaning

router = APIRouter(
    dependencies=[Depends(verify_jwt_token)]
)

@router.post("/check-grammar")
async def check_grammar(request: GrammarRequest):
    try:
        payload = {"text": request.text, "language": "de-DE"}
        response = requests.post(LANGUAGETOOL_API, data=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        raise HTTPException(status_code=502, detail="LanguageTool service unavailable.")


@router.get("/example-sentence/", response_model=ExampleSentenceResponse)
def example_sentence(
    word: str = Query(..., description="Word to use in the German example sentence")
):
    result = generate_sentence(word)
    if result.startswith("Error: Could not connect to the LLM service"):
        raise HTTPException(status_code=503, detail=result)
    if result.startswith("Error: The request to the LLM service timed out."):
        raise HTTPException(status_code=504, detail=result)
    if result.startswith("No response from the language model."):
        raise HTTPException(status_code=502, detail=result)
    if result.startswith("An unexpected error occurred"):
        raise HTTPException(status_code=500, detail=result)
    return ExampleSentenceResponse(word=word, sentence=result)

@router.get("/verb-form/", response_model=VerbFormResponse)
def verb_form(
    verb: str = Query(..., description="German verb in any form (e.g., gehen)"),
    form: VerbForm = Query(..., description="Verb form"),
    person: Person = Query(Person.ich, description="Person for conjugation (ich, du, er/sie/es, wir, ihr, sie/Sie)")
):
    result = get_verb_form(verb, form.value, person.value)
    if result.startswith("Unknown or unsupported verb form."):
        raise HTTPException(status_code=400, detail=result)
    if result.startswith("Error: Could not connect to the LLM service"):
        raise HTTPException(status_code=503, detail=result)
    if result.startswith("Error: The request to the LLM service timed out."):
        raise HTTPException(status_code=504, detail=result)
    if result.startswith("No response from the language model."):
        raise HTTPException(status_code=502, detail=result)
    if result.startswith("An unexpected error occurred"):
        raise HTTPException(status_code=500, detail=result)
    return VerbFormResponse(verb=verb, form=form.value, person=person.value, result=result)

@router.get("/mcq-meaning/", response_model=MCQMeaningResponse)
def mcq_meaning(
    word: str = Query(..., description="German word (noun, verb, adjective, etc.)")
):
    result = generate_mcq_meaning(word)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    if not result.get("options"):
        raise HTTPException(
            status_code=502,
            detail="Could not generate multiple choice options. Try another word or rephrase your prompt."
        )
    return MCQMeaningResponse(
        word=result["word"],
        options=result["options"],
        answer=result["answer"]
    )
