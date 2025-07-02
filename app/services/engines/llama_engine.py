from llama_cpp import Llama
from app.config import LLAMA_GGUF_PATH, LLAMA_N_CTX, LLAMA_N_THREADS
from .engine_base import TextGenerationEngine

class LlamaCppEngine(TextGenerationEngine):
    def __init__(self):
        try:
            self.llm = Llama(
                model_path=LLAMA_GGUF_PATH,
                n_ctx=LLAMA_N_CTX,
                n_threads=LLAMA_N_THREADS
            )
            self.load_error = None
        except Exception as e:
            self.llm = None
            self.load_error = str(e)

    def generate(self, prompt: str, max_tokens: int = 60) -> str:
        if self.llm is None:
            raise RuntimeError(f"Model unavailable: {self.load_error}")
        output = self.llm(
            prompt,
            max_tokens=max_tokens,
            stop=["<|user|>", "<|assistant|>", "<|endoftext|>", "\n\n"],
            temperature=0.85,
            top_p=0.95,
        )
        return output["choices"][0]["text"].strip()