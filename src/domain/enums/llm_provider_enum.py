from enum import Enum

class LLMProviderEnum(str, Enum):
    OPENAI = "openai"
    COHERE = "cohere"