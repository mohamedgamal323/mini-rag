from typing import List
from .llm_provider import LLMProvider
import cohere

class CoHereProvider(LLMProvider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = cohere.Client(self.llm_config.cohere_api_key)

    def set_generation_model(self, model_name: str):
        self.generation_model = model_name

    def set_embedding_model(self, model_name: str):
        self.embedding_model = model_name

    async def generate_text(self, prompt: str, max_tokens: int = 128) -> str:
        self._validate_input(prompt)
        self._validate_tokens(max_tokens)
        response = self.client.generate(
            model=self.generation_model or self.llm_config.cohere_generation_model,
            prompt=prompt,
            max_tokens=max_tokens,
        )
        return response.generations[0].text

    async def embed(self, text: str) -> list[float]:
        self._validate_input(text)
        response = self.client.embed(
            model=self.embedding_model or self.llm_config.cohere_embedding_model,
            texts=[text],
        )
        return response.embeddings[0]

    async def batch_embed(self, texts: List[str]) -> List[List[float]]:
        for text in texts:
            self._validate_input(text)
        response = self.client.embed(
            model=self.embedding_model or self.llm_config.cohere_embedding_model,
            texts=texts,
        )
        return response.embeddings