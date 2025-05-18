from abc import ABC, abstractmethod
from helpers.llm_config import llm_config

class LLMProvider(ABC):
    def __init__(self, *args, **kwargs):
        self.generation_model = None
        self.embedding_model = None
        self.llm_config = llm_config
        self.max_input_chars = getattr(llm_config, "max_input_chars", 4096)
        self.max_generated_tokens = getattr(llm_config, "max_generated_tokens", 512)

    @abstractmethod
    def set_generation_model(self, model_name: str):
        pass

    @abstractmethod
    def set_embedding_model(self, model_name: str):
        pass

    def _validate_input(self, text: str):
        if len(text) > self.max_input_chars:
            raise ValueError(f"Input text exceeds max allowed characters ({self.max_input_chars})")

    def _validate_tokens(self, tokens: int):
        if tokens > self.max_generated_tokens:
            raise ValueError(f"Requested tokens exceed max allowed ({self.max_generated_tokens})")

    @abstractmethod
    async def generate_text(self, prompt: str, max_tokens: int = 128) -> str:
        pass

    @abstractmethod
    async def embed(self, text: str) -> list[float]:
        pass

    @abstractmethod
    async def batch_embed(self, texts: list[str]) -> list[list[float]]:
        pass