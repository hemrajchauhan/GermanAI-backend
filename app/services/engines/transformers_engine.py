import ast
from transformers import pipeline
from app.config import TRANSFORMERS_MODEL_NAME, TRANSFORMERS_MAX_LENGTH
from .engine_base import TextGenerationEngine

def extract_assistant_content(generated):
    """
    Handles:
    - stringified list of dicts (Qwen-style)
    - plain string
    - dict (rare)
    """
    # If it's already a dict
    if isinstance(generated, dict):
        if generated.get("role") == "assistant":
            return generated.get("content", "").strip()
    # If it's a list
    if isinstance(generated, list):
        for msg in generated:
            if isinstance(msg, dict) and msg.get("role") == "assistant":
                return msg.get("content", "").strip()
    # If it's a string, check if it looks like a list of dicts
    if isinstance(generated, str):
        s = generated.strip()
        if s.startswith("[") and s.endswith("]"):
            try:
                messages = ast.literal_eval(s)
                for msg in messages:
                    if isinstance(msg, dict) and msg.get("role") == "assistant":
                        return msg.get("content", "").strip()
            except Exception:
                pass  # fall through to next
        # Otherwise, try regex as last resort
        import re
        match = re.search(r"'role': 'assistant', 'content': '([^']+)'", s)
        if match:
            return match.group(1).strip()
        return s
    # Fallback
    return str(generated).strip()

class TransformersEngine(TextGenerationEngine):
    def __init__(self):
        try:
            self.generator = pipeline(
                "text-generation",
                model=TRANSFORMERS_MODEL_NAME,
                tokenizer=TRANSFORMERS_MODEL_NAME,
                trust_remote_code=True  # needed for Phi and Llama chat models
            )
            self.load_error = None

            # Identify if model is a chat/instruct model (Phi-4, Phi-3, Llama-3, Instruct models, etc)
            self.is_chat = any(
                k in TRANSFORMERS_MODEL_NAME.lower()
                for k in ["phi-4", "phi-3", "llama-3", "instruct"]
            )
        except Exception as e:
            self.generator = None
            self.load_error = str(e)
            self.is_chat = False

    def generate(self, prompt, max_tokens: int = TRANSFORMERS_MAX_LENGTH) -> str:
        """
        Supports both plain prompts (str) and chat messages (list of dict).
        Uses max_new_tokens for chat models, max_length for plain models.
        """
        if self.generator is None:
            raise RuntimeError(f"Model unavailable: {self.load_error}")

        if self.is_chat or isinstance(prompt, list):
            input_data = [{"role": "user", "content": prompt}] if isinstance(prompt, str) else prompt
            result = self.generator(
                input_data,
                num_return_sequences=1,
                max_new_tokens=max_tokens
            )
        else:
            result = self.generator(
                prompt,
                num_return_sequences=1,
                max_length=max_tokens
            )

        generated = result[0].get("generated_text", result[0])
        return extract_assistant_content(generated)
