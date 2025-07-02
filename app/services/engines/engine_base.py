from abc import ABC, abstractmethod

class TextGenerationEngine(ABC):
    @abstractmethod
    def generate(self, prompt: str, max_tokens: int = 100) -> str:
        pass