from collections import defaultdict
from enum import Enum
from typing import Literal

from pydantic import BaseModel

TaskType = Literal["text-generation", "question-answering", "summarization"]


class ModelProvider(str, Enum):
    HUGGINGFACE = "huggingface"
    OPENAI = "openai"


LLM_MODELS: defaultdict[ModelProvider, list[str]] = defaultdict(
    list,
    {
        ModelProvider.HUGGINGFACE: ["meta-llama/Llama-3.1-8B-Instruct", "deepseek-ai/DeepSeek-R1"],
        ModelProvider.OPENAI: ["gpt-3.5-turbo", "gpt-4o-mini", "gpt-4o"],
    },
)


class GeneralModelConfig(BaseModel):
    temperature: float = 0.7
    max_tokens: int = 1024
