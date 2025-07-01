import requests
import random
from app.config import OLLAMA_URL

def generate_sentence(word: str, model: str = "llama3") -> str:
    """
    Generate a German example sentence with the provided word.
    """
    prompt = f"Erzeuge einen deutschen Beispielsatz mit dem Wort '{word}'."
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"num_predict": 150}
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "").strip() or "No response from the language model."
    except requests.exceptions.ConnectionError:
        return "Error: Could not connect to the LLM service (Ollama)."
    except requests.exceptions.Timeout:
        return "Error: The request to the LLM service timed out."
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

def get_verb_form(verb: str, form: str, person: str = "ich", model: str = "llama3") -> str:
    """
    Generate a specific verb form for a given German verb and person.
    """
    prompts = {
        "infinitiv": f"Gib die Infinitivform des Verbs '{verb}'.",
        "praesens": f"Konjugiere das Verb '{verb}' im Präsens für '{person}'.",
        "praeteritum": f"Konjugiere das Verb '{verb}' im Präteritum für '{person}'.",
        "perfekt": f"Konjugiere das Verb '{verb}' im Perfekt für '{person}'.",
        "plusquamperfekt": f"Konjugiere das Verb '{verb}' im Plusquamperfekt für '{person}'.",
        "futur1": f"Konjugiere das Verb '{verb}' im Futur I für '{person}'.",
        "futur2": f"Konjugiere das Verb '{verb}' im Futur II für '{person}'.",
        "konjunktiv1": f"Konjugiere das Verb '{verb}' im Konjunktiv I für '{person}'.",
        "konjunktiv2": f"Konjugiere das Verb '{verb}' im Konjunktiv II für '{person}'.",
        "imperativ": f"Gib die Imperativform des Verbs '{verb}' für '{person}'.",
        "partizip1": f"Gib das Partizip I (Partizip Präsens) des Verbs '{verb}'.",
        "partizip2": f"Gib das Partizip II (Partizip Perfekt) des Verbs '{verb}'.",
    }
    prompt = prompts.get(form.lower())
    if not prompt:
        return "Unknown or unsupported verb form."

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"num_predict": 100}
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "").strip() or "No response from the language model."
    except requests.exceptions.ConnectionError:
        return "Error: Could not connect to the LLM service (Ollama)."
    except requests.exceptions.Timeout:
        return "Error: The request to the LLM service timed out."
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

def generate_mcq_meaning(word: str, model: str = "llama3") -> dict:
    """
    Generates a multiple-choice question (MCQ) for the meaning of a German word (verb, noun, etc.).
    Returns a dict with the options (shuffled) and the index of the correct answer.
    """
    prompt = (
    f"Erstelle eine Multiple-Choice-Frage für das deutsche Wort '{word}'. "
    f"Gib vier Antwortmöglichkeiten auf Englisch für die Bedeutung dieses Wortes an. "
    f"Jede Antwortmöglichkeit soll nur ein einzelnes englisches Wort oder eine sehr kurze Phrase sein, KEINE Beispielsätze. "
    f"Nur eine Antwort ist korrekt, die anderen drei sind plausible Ablenker. "
    f"Formatiere die Antwort als JSON mit den Schlüsseln: 'options' (eine Liste von vier Optionen) und 'answer' (der Index der richtigen Option, beginnend bei 0)."
    )
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"num_predict": 150}
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        answer_text = data.get("response", "").strip()

        import json
        try:
            # Extract JSON part from LLM output
            start = answer_text.find('{')
            end = answer_text.rfind('}') + 1
            if start != -1 and end != -1:
                answer_text = answer_text[start:end]
            parsed = json.loads(answer_text)
            options = parsed.get("options", [])
            correct_idx = parsed.get("answer", 0)
            if not options or not (0 <= correct_idx < len(options)):
                raise ValueError("Could not parse options/answer.")

            # --- SHUFFLING LOGIC ---
            indices = list(range(len(options)))
            random.shuffle(indices)
            shuffled_options = [options[i] for i in indices]
            new_answer = indices.index(correct_idx)
            # --- END SHUFFLING ---

            return {
                "word": word,
                "options": shuffled_options,
                "answer": new_answer
            }
        except Exception:
            # If JSON parse fails, return as a text block for manual QA
            return {
                "word": word,
                "options": [],
                "answer": -1,
                "raw_response": answer_text
            }
    except requests.exceptions.ConnectionError:
        return {"error": "Error: Could not connect to the LLM service (Ollama)."}
    except requests.exceptions.Timeout:
        return {"error": "Error: The request to the LLM service timed out."}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}
