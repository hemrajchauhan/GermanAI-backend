from transformers import pipeline
from app.models.germangpt import (
    ExampleSentenceRequest,
    ExampleSentenceResponse,
    VerbFormRequest,
    VerbFormResponse,
    VerbForm,
    Person,
)

try:
    generator = pipeline(
        "text-generation",
        model="dbmdz/german-gpt2",
        tokenizer="dbmdz/german-gpt2",
        max_length=50
    )
    load_error = None
except Exception as e:
    generator = None
    load_error = str(e)

def generate_sentence(request: ExampleSentenceRequest) -> ExampleSentenceResponse:
    """
    Generate a German example sentence with the provided word.
    """
    word = request.word.strip()
    if not word:
        return ExampleSentenceResponse(word=request.word, error="No word provided.")
    if generator is None:
        return ExampleSentenceResponse(word=request.word, error=f"Model unavailable: {load_error}")
    prompt = f"Beispielsatz mit '{word}':"
    #prompt = f"Erzeuge einen deutschen Beispielsatz mit dem Wort '{word}'."
    try:
        result = generator(prompt, num_return_sequences=1)
        sentence = result[0]["generated_text"].strip()
        return ExampleSentenceResponse(word=word, sentence=sentence)
    except Exception as e:
        return ExampleSentenceResponse(word=word, error=f"Generation error: {str(e)}")

def get_verb_form(request: VerbFormRequest) -> VerbFormResponse:
    """
    Generate a specific verb form for a given German verb and person.
    """
    prompts = {
        VerbForm.infinitiv: f"Gib die Infinitivform des Verbs '{request.verb}'.",
        VerbForm.praesens: f"Konjugiere das Verb '{request.verb}' im Präsens für '{request.person.value}'.",
        VerbForm.praeteritum: f"Konjugiere das Verb '{request.verb}' im Präteritum für '{request.person.value}'.",
        VerbForm.perfekt: f"Konjugiere das Verb '{request.verb}' im Perfekt für '{request.person.value}'.",
        VerbForm.plusquamperfekt: f"Konjugiere das Verb '{request.verb}' im Plusquamperfekt für '{request.person.value}'.",
        VerbForm.futur1: f"Konjugiere das Verb '{request.verb}' im Futur I für '{request.person.value}'.",
        VerbForm.futur2: f"Konjugiere das Verb '{request.verb}' im Futur II für '{request.person.value}'.",
        VerbForm.konjunktiv1: f"Konjugiere das Verb '{request.verb}' im Konjunktiv I für '{request.person.value}'.",
        VerbForm.konjunktiv2: f"Konjugiere das Verb '{request.verb}' im Konjunktiv II für '{request.person.value}'.",
        VerbForm.imperativ: f"Gib die Imperativform des Verbs '{request.verb}' für '{request.person.value}'.",
        VerbForm.partizip1: f"Gib das Partizip I (Partizip Präsens) des Verbs '{request.verb}'.",
        VerbForm.partizip2: f"Gib das Partizip II (Partizip Perfekt) des Verbs '{request.verb}'."
    }
    prompt = prompts.get(request.form)
    if not prompt:
        return VerbFormResponse(
            verb=request.verb, form=request.form, person=request.person,
            error="Unknown or unsupported verb form."
        )
    if generator is None:
        return VerbFormResponse(
            verb=request.verb, form=request.form, person=request.person,
            error=f"Model unavailable: {load_error}"
        )
    try:
        result = generator(prompt, num_return_sequences=1)
        output = result[0]["generated_text"].strip()
        return VerbFormResponse(
            verb=request.verb, form=request.form, person=request.person, result=output
        )
    except Exception as e:
        return VerbFormResponse(
            verb=request.verb, form=request.form, person=request.person,
            error=f"Generation error: {str(e)}"
        )
