import logging
import os

from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

logger = logging.getLogger(__name__)


def init_chromadb(
    docs: list[Document], collection_name: str, embeddings: Embeddings, persistent_directory: str
) -> Chroma:

    if os.path.exists(persistent_directory):
        logger.info(f"ChromaDB with collection name: {collection_name} already exists at {persistent_directory}.")
        return Chroma(
            embedding_function=embeddings, collection_name=collection_name, persist_directory=persistent_directory
        )
    logger.info(f"Creating Vector Store at {persistent_directory}.")
    return Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        collection_name=collection_name,
        persist_directory=persistent_directory,
    )
