from collections import defaultdict
from typing import Literal

from pydantic import BaseModel

TaskType = Literal["text-generation", "question-answering", "summarization"]

ModelProvider = Literal["huggingface", "openai"]

LLM_MODELS: defaultdict[ModelProvider, list[str]] = defaultdict(
    list,
    {
        "huggingface": ["meta-llama/Llama-3.1-8B-Instruct", "deepseek-ai/DeepSeek-R1"],
        "openai": ["gpt-3.5-turbo", "gpt-4o-mini", "gpt-4o"],
    },
)


class GeneralModelConfig(BaseModel):
    temperature: float = 0.7
    max_tokens: int = 1024


class OpenAIModelConfig(GeneralModelConfig):
    model_name: str = "gpt-3.5-turbo"
    provider: ModelProvider = "openai"


class HuggingFaceModelConfig(GeneralModelConfig):
    model_name: str = "meta-llama/Llama-3.1-8B-Instruct"
    provider: ModelProvider = "huggingface"
    task: TaskType = "text-generation"
