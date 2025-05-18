from domain.enums.llm_provider_enum import LLMProviderEnum
from .openai_provider import OpenAIProvider
from .cohere_provider import CoHereProvider
from .llm_provider import LLMProvider

class LLMProviderFactory:
    @staticmethod
    def create(provider: LLMProviderEnum) -> LLMProvider:
        if provider == LLMProviderEnum.OPENAI.value:
            return OpenAIProvider()
        elif provider == LLMProviderEnum.COHERE.value:
            return CoHereProvider()
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")