import logging
from collections import defaultdict
from enum import Enum

from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_core.embeddings import Embeddings
from langchain_openai import OpenAIEmbeddings

logger = logging.getLogger(__name__)


class EmbeddingProvider(Enum):
    FastEmbed = "fastembed"
    OPENAI = "openai"


EMBEDDING_MODELS: defaultdict[EmbeddingProvider, list[str]] = defaultdict(
    list,
    {
        EmbeddingProvider.FastEmbed: ["BAAI/bge-small-en-v1.5"],
        EmbeddingProvider.OPENAI: ["text-embedding-ada-002", "text-embedding-3-small"],
    },
)


def init_embedding_model(
    provider: EmbeddingProvider = EmbeddingProvider.FastEmbed,
    embedding_model_name: str = "BAAI/bge-small-en-v1.5",
    **kwargs,
) -> Embeddings:

    if embedding_model_name not in EMBEDDING_MODELS[provider]:
        raise ValueError(
            f"embedding model: {embedding_model_name} is not available for provider {provider.value}."
            f"Available embedding models: {EMBEDDING_MODELS[provider]}"
        )

    logger.info(f"Initializing embedding model: {embedding_model_name} from provider: {provider.value}")
    embedding_init_fn = {
        EmbeddingProvider.FastEmbed: FastEmbedEmbeddings,
        EmbeddingProvider.OPENAI: OpenAIEmbeddings,
    }

    if provider == EmbeddingProvider.OPENAI:
        return embedding_init_fn[provider](model=embedding_model_name, **kwargs)
    else:
        return embedding_init_fn[provider](model_name=embedding_model_name, **kwargs)
