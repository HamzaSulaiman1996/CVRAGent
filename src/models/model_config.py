from collections import defaultdict
from enum import Enum
from typing import Any, Literal, Optional

from pydantic import BaseModel

TaskType = Literal["text-generation", "question-answering", "summarization"]


class ModelProvider(str, Enum):
    HUGGINGFACE = "huggingface"
    OPENAI = "openai"


LLM_MODELS: defaultdict[ModelProvider, list[str]] = defaultdict(
    list,
    {
        ModelProvider.HUGGINGFACE: ["meta-llama/Llama-3.1-8B-Instruct", "deepseek-ai/DeepSeek-R1"],
        ModelProvider.OPENAI: ["gpt-3.5-turbo", "gpt-4o-mini", "gpt-4o", "gpt-5-nano"],
    },
)


class GeneralModelConfig(BaseModel):
    model_name: Optional[str] = None
    temperature: float = 0.2
    max_tokens: int = 2048

    def model_post_init(self, context: Any) -> None:
        self.temperature = 1.0 if self.model_name == "gpt-5-nano" else 0.2
        self.max_tokens = int(1e5) if self.model_name == "gpt-5-nano" else 2048
