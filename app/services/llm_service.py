from app.models.germangpt import (
    ExampleSentenceRequest, ExampleSentenceResponse,
    VerbFormRequest, VerbFormResponse, VerbForm
)
from app.services.engines.factory import get_llama_engine, get_transformers_engine

def _llama_chat_prompt(task_prompt: str) -> list:
    # Return as a chat message list, for chat models
    return [{"role": "user", "content": task_prompt}]

def generate_sentence(request: ExampleSentenceRequest) -> ExampleSentenceResponse:
    word = request.word.strip()
    if not word:
        return ExampleSentenceResponse(word=request.word, error="No word provided.")

    # Pick engine as needed
    # engine = get_llama_engine() 
    """
    or 
    """
    engine = get_transformers_engine()

    # Detect if engine needs a chat message or plain prompt
    is_chat = getattr(engine, "is_chat", False)
    task = f"Erzeuge einen deutschen Beispielsatz mit dem Wort '{word}'."
    prompt = _llama_chat_prompt(task) if is_chat else f"Beispielsatz mit '{word}':"

    try:
        text = engine.generate(prompt, max_tokens=100)
        return ExampleSentenceResponse(word=word, sentence=text)
    except Exception as e:
        return ExampleSentenceResponse(word=word, error=f"Generation error: {str(e)}")

def get_verb_form(request: VerbFormRequest) -> VerbFormResponse:
    prompts = {
        VerbForm.infinitiv: f"Gib die Infinitivform des Verbs '{request.verb}':",
        VerbForm.praesens: f"Konjugiere das Verb '{request.verb}' im Präsens für '{request.person.value}':",
        VerbForm.praeteritum: f"Konjugiere das Verb '{request.verb}' im Präteritum für '{request.person.value}':",
        VerbForm.perfekt: f"Konjugiere das Verb '{request.verb}' im Perfekt für '{request.person.value}':",
        VerbForm.plusquamperfekt: f"Konjugiere das Verb '{request.verb}' im Plusquamperfekt für '{request.person.value}':",
        VerbForm.futur1: f"Konjugiere das Verb '{request.verb}' im Futur I für '{request.person.value}':",
        VerbForm.futur2: f"Konjugiere das Verb '{request.verb}' im Futur II für '{request.person.value}':",
        VerbForm.konjunktiv1: f"Konjugiere das Verb '{request.verb}' im Konjunktiv I für '{request.person.value}':",
        VerbForm.konjunktiv2: f"Konjugiere das Verb '{request.verb}' im Konjunktiv II für '{request.person.value}':",
        VerbForm.imperativ: f"Gib die Imperativform des Verbs '{request.verb}' für '{request.person.value}':",
        VerbForm.partizip1: f"Gib das Partizip I (Partizip Präsens) des Verbs '{request.verb}':",
        VerbForm.partizip2: f"Gib das Partizip II (Partizip Perfekt) des Verbs '{request.verb}':"
    }
    task_prompt = prompts.get(request.form)
    if not task_prompt:
        return VerbFormResponse(
            verb=request.verb, form=request.form, person=request.person,
            error="Unknown or unsupported verb form."
        )

    # Pick engine as needed
    # engine = get_llama_engine() 
    """
    or 
    """
    engine = get_transformers_engine()

    is_chat = getattr(engine, "is_chat", False)
    prompt = _llama_chat_prompt(task_prompt) if is_chat else task_prompt

    try:
        text = engine.generate(prompt, max_tokens=60)
        return VerbFormResponse(
            verb=request.verb, form=request.form, person=request.person, result=text
        )
    except Exception as e:
        return VerbFormResponse(
            verb=request.verb, form=request.form, person=request.person,
            error=f"Generation error: {str(e)}"
        )
