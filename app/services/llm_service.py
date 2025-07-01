import os
import requests
import random

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434/api/generate")

def generate_sentence(word: str, model: str = "llama3") -> str:
    """
    Generate a German example sentence with the provided word.
    """
    prompt = f"Generate a German example sentence with the word '{word}'."
    payload = {
        "model": model,
        "prompt": prompt,
        "options": {"num_predict": 25}
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=15)
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
        "infinitiv": f"Give the infinitive form of the verb '{verb}'.",
        "praesens": f"Conjugate the verb '{verb}' in present tense (Präsens) for '{person}'.",
        "praeteritum": f"Conjugate the verb '{verb}' in simple past (Präteritum) for '{person}'.",
        "perfekt": f"Conjugate the verb '{verb}' in present perfect (Perfekt) for '{person}'.",
        "plusquamperfekt": f"Conjugate the verb '{verb}' in past perfect (Plusquamperfekt) for '{person}'.",
        "futur1": f"Conjugate the verb '{verb}' in future I (Futur I) for '{person}'.",
        "futur2": f"Conjugate the verb '{verb}' in future II (Futur II) for '{person}'.",
        "konjunktiv1": f"Conjugate the verb '{verb}' in subjunctive I (Konjunktiv I) for '{person}'.",
        "konjunktiv2": f"Conjugate the verb '{verb}' in subjunctive II (Konjunktiv II) for '{person}'.",
        "imperativ": f"Give the imperative form of the verb '{verb}' for '{person}'.",
        "partizip1": f"Give the present participle (Partizip I) of the verb '{verb}'.",
        "partizip2": f"Give the past participle (Partizip II) of the verb '{verb}'.",
    }
    prompt = prompts.get(form.lower())
    if not prompt:
        return "Unknown or unsupported verb form."

    payload = {
        "model": model,
        "prompt": prompt,
        "options": {"num_predict": 16}
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=15)
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
        f"Generate a multiple-choice question for a German learner. "
        f"The word is '{word}'. "
        f"Provide four English options for the meaning, exactly one of which is correct and three are plausible distractors. "
        f"Format your answer as a JSON with keys: 'options' (a list of four options) and 'answer' (the index of the correct one, 0-based)."
    )
    payload = {
        "model": model,
        "prompt": prompt,
        "options": {"num_predict": 150}
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=25)
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