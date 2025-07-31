import logging
import os

import streamlit as st
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

logger = logging.getLogger(__name__)


@st.cache_resource()
def init_chromadb(
    _docs: list[Document], _collection_name: str, _embeddings: Embeddings, _persistent_directory: str
) -> Chroma:

    if os.path.exists(_persistent_directory):
        logger.info(f"ChromaDB with collection name: {_collection_name} already exists at {_persistent_directory}.")
        return Chroma(
            embedding_function=_embeddings, collection_name=_collection_name, persist_directory=_persistent_directory
        )
    logger.info(f"Creating Vector Store at {_persistent_directory}.")
    return Chroma.from_documents(
        documents=_docs,
        embedding=_embeddings,
        collection_name=_collection_name,
        persist_directory=_persistent_directory,
    )
