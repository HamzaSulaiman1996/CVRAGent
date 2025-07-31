import logging
from functools import partial
from typing import Callable, Dict

from dotenv import load_dotenv
from langchain_core.language_models import BaseChatModel
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_openai import ChatOpenAI

from .model_config import LLM_MODELS, ModelProvider, TaskType

logger = logging.getLogger(__name__)


def hugging_face_model(model: str, task: TaskType, verbose: bool = True, **kwargs) -> ChatHuggingFace:
    """
    Create a HuggingFace chat model with the specified parameters.

    Args:
        model (str): The name of the HuggingFace model.
        tasks (TaskType): The task type for the model.
        verbose (bool): Whether to enable verbose logging.
        **kwargs: Additional keyword arguments for endpoint configuration.

    Returns:
        ChatHuggingFace: Configured HuggingFace chat model.
    """
    kwargs["max_new_tokens"] = kwargs.get("max_tokens", 512)
    kwargs.pop("max_tokens", None)
    end_point = HuggingFaceEndpoint(model=model, task=task, **kwargs)
    return ChatHuggingFace(llm=end_point, verbose=verbose)


def init_model(provider: ModelProvider, model_name: str, uses_api_key: bool = True, **kwargs) -> BaseChatModel:

    if model_name not in LLM_MODELS[provider]:
        raise ValueError(
            f"Model {model_name} is not available for provider {provider}. " f"Available models: {LLM_MODELS[provider]}"
        )

    logger.info(f"Initializing model: {model_name} from provider: {provider}")
    model_init_fn: Dict[ModelProvider, Callable[..., BaseChatModel]] = {
        "huggingface": partial(hugging_face_model, **kwargs),
        "openai": partial(ChatOpenAI, **kwargs),
    }

    if uses_api_key:
        logger.info("Authenticating with API Key.")
        load_dotenv()

    return model_init_fn[provider](model=model_name)
