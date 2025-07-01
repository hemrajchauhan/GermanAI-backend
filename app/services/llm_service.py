import requests
import random
import json
from app.config import OLLAMA_URL, OLLAMA_MODEL

def generate_sentence(word: str, model: str = None) -> str:
    """
    Generate a German example sentence with the provided word.
    """
    model = model or OLLAMA_MODEL
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

def get_verb_form(verb: str, form: str, person: str = "ich", model: str = None) -> str:
    """
    Generate a specific verb form for a given German verb and person.
    """
    model = model or OLLAMA_MODEL
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

def generate_mcq_meaning(word: str, model: str = None) -> dict:
    """
    Generates a multiple-choice question (MCQ) for the meaning of a German word (verb, noun, etc.).
    Returns a dict with the options (shuffled) and the index of the correct answer.
    """
    model = model or OLLAMA_MODEL
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
    

def translate_word_all_meanings(word: str, model: str = None) -> dict:
    """
    Get all possible English meanings of a German word.
    """
    model = model or OLLAMA_MODEL
    prompt = (
        f"List all possible English meanings for the German word '{word}'. "
        "Respond as a JSON array of strings, with no extra explanation."
    )
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"num_predict": 80}
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        meanings_text = data.get("response", "").strip()
        # Try to parse JSON array first
        try:
            meanings = json.loads(meanings_text)
            if not isinstance(meanings, list) or not meanings:
                raise ValueError
        except Exception:
            # fallback: try to split by lines/bullets if not JSON
            lines = [m.strip("-•;:. ") for m in meanings_text.splitlines() if m.strip()]
            meanings = [l for l in lines if l and len(l) < 128]
        if not meanings:
            return {"error": "No meanings found in the LLM response."}
        return {"word": word, "meanings": meanings}
    except requests.exceptions.ConnectionError:
        return {"error": "Could not connect to the LLM service (Ollama)."}
    except requests.exceptions.Timeout:
        return {"error": "The request to the LLM service timed out."}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}
    

def translate_sentence(sentence: str, model: str = None, max_words: int = 50) -> dict:
    """
    Translate a German sentence to English (with a word limit for resource control).
    """
    model = model or OLLAMA_MODEL
    if not sentence or not sentence.strip():
        return {"error": "No sentence provided."}
    if len(sentence.split()) > max_words:
        return {"error": f"Sentence too long (max {max_words} words)."}

    prompt = (
        f"Translate the following German sentence into English:\n\n{sentence}\n\n"
        "Only return the English translation, no extra explanation."
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
        translation = data.get("response", "").strip()
        if not translation:
            return {"error": "No translation found in the LLM response."}
        return {"sentence": sentence, "translation": translation}
    except requests.exceptions.ConnectionError:
        return {"error": "Could not connect to the LLM service (Ollama)."}
    except requests.exceptions.Timeout:
        return {"error": "The request to the LLM service timed out."}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}
