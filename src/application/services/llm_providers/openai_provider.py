from typing import List
from .llm_provider import LLMProvider
import openai

class OpenAIProvider(LLMProvider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        openai.api_key = self.llm_config.OPENAI_API_KEY

    def set_generation_model(self, model_name: str):
        self.generation_model = model_name

    def set_embedding_model(self, model_name: str):
        self.embedding_model = model_name

    async def generate_text(self, prompt: str, max_tokens: int = 128) -> str:
        self._validate_input(prompt)
        self._validate_tokens(max_tokens)
        response = openai.ChatCompletion.create(
            model=self.generation_model or self.llm_config.OPENAI_GENERATION_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
        )
        return response.choices[0].message["content"]

    async def embed(self, text: str) -> list[float]:
        self._validate_input(text)
        response = openai.Embedding.create(
            model=self.embedding_model or self.llm_config.OPENAI_EMBEDDING_MODEL,
            input=text,
        )
        return response["data"][0]["embedding"]

    async def batch_embed(self, texts: List[str]) -> List[List[float]]:
        for text in texts:
            self._validate_input(text)
        response = openai.Embedding.create(
            model=self.embedding_model or self.llm_config.OPENAI_EMBEDDING_MODEL,
            input=texts,
        )
        return [item["embedding"] for item in response["data"]]