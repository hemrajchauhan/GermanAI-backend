from .llama_engine import LlamaCppEngine
from .transformers_engine import TransformersEngine

def get_llama_engine():
    """Return a Llama.cpp engine instance (GGUF model)."""
    return LlamaCppEngine()

def get_transformers_engine():
    """Return a Transformers engine instance (HuggingFace model)."""
    return TransformersEngine()