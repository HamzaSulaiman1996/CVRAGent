import logging
import os
import tempfile
from typing import Optional

from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

logger = logging.getLogger(__name__)


def init_chromadb(
    docs: list[Document],
    collection_name: str,
    embeddings: Embeddings,
    persistent_directory: Optional[str] = None,
) -> Chroma:
    if not persistent_directory:
        persistent_directory = tempfile.mkdtemp(prefix="chromadb_")
        logger.info(f"Created temporary directory for ChromaDB at {persistent_directory} (non-persistent).")
    elif os.path.exists(persistent_directory):
        logger.info(f"ChromaDB with collection name: {collection_name} already exists at {persistent_directory}.")
        return Chroma(
            embedding_function=embeddings,
            collection_name=collection_name,
            persist_directory=persistent_directory,
        )
    else:
        logger.info(f"Creating Vector Store at {persistent_directory}.")

    return Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        collection_name=collection_name,
        persist_directory=persistent_directory,
    )
