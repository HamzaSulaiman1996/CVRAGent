import logging

import streamlit as st
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate

import src.prompt_lists as prompts
from src.db.vector_store import init_chromadb
from src.embedding import init_embedding_model
from src.frontend.domain import check_job_length, format_output
from src.models.model_config import LLM_MODELS, GeneralModelConfig, ModelProvider
from src.models.models import init_model
from src.parser import PDFParser


@st.cache_data(show_spinner=False, max_entries=3)
def model_output(
    model_provider: str, model_name: str, resume_content: str, jd: str, which_button: bool = True, **kwargs
) -> str:
    """
    Cache the model output based on model name, job description, and resume content.
    """

    kwargs = {**GeneralModelConfig().model_dump(), **kwargs}
    model = init_model(
        provider=ModelProvider(model_provider),
        model_name=model_name,
        **kwargs,
    )

    result = model.invoke(st.session_state['messages'].invoke({"job_description": jd, "resume": resume_content}))

    return format_output(result.content)


def get_result_db_retriever(_chunks: list[Document]) -> list[Document]:
    embedding_model = init_embedding_model()
    chroma_retriever = init_chromadb(
        docs=_chunks,
        collection_name="cvragent",
        embeddings=embedding_model,
        persistent_directory=f"src/db/chromadb/{st.session_state['uploaded_file'].file_id}",
    )
    chroma = chroma_retriever.as_retriever(
        search_type="similarity_score_threshold", search_kwargs={"k": 10, "score_threshold": 0.2}
    )

    bm25 = BM25Retriever.from_documents(_chunks)
    bm25.k = 10
    return EnsembleRetriever(retrievers=[chroma, bm25], weights=[0.5, 0.5]).invoke(prompts.SKILLS_RETRIEVAL)


def initialize_session_state():
    states = ["uploaded_file", "job_desc", "messages", "choose_provider", "choose_model"]
    for state in states:
        if state not in st.session_state:
            st.session_state[state] = None


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


def main():

    initialize_session_state()

    st.title("CVRAGent :pencil:")
    st.write("An AI-powered CV Review Agent :robot_face:")

    with st.sidebar:
        st.header("Upload Your CV in pdf format")
        uploaded_file = st.file_uploader(
            label="Upload your CV",
            label_visibility='hidden',
            type=["pdf"],
            accept_multiple_files=False,
        )
        st.session_state["uploaded_file"] = uploaded_file

        choose_provider = st.selectbox(
            label="Select model provider",
            options=[model.value for model in ModelProvider],
            index=None,
        )
        if choose_provider:
            choose_model = st.selectbox(
                label="Select model",
                options=LLM_MODELS[ModelProvider(choose_provider)],
            )

    st.session_state["job_desc"] = st.text_area(
        "Enter the job description",
        placeholder="Paste the job description here...",
        height=300,
    )

    analyze_button, _, suggest_improv_button = st.columns(3)
    analyze_button = st.button(
        label="Analyze Resume",
        type="primary",
        icon="✅",
        use_container_width=True,
    )
    suggest_improv_button = st.button(
        label="Suggest Improvements",
        type="primary",
        icon="💡",
        use_container_width=True,
    )

    if not analyze_button and not suggest_improv_button:
        return

    if analyze_button or suggest_improv_button:
        if not st.session_state["uploaded_file"]:
            st.error("Please upload a CV in PDF format.")
            return
        if not st.session_state["job_desc"]:
            st.error("Please enter the job description.")
            return
        if not check_job_length(st.session_state["job_desc"]):
            st.error("Job description is too short. Please provide a more detailed job description.")
            return

    if suggest_improv_button:
        st.session_state['messages'] = ChatPromptTemplate(
            [SystemMessage(content=prompts.OPTIMIZATION_SYSTEM_MESSAGE), ("human", prompts.COMBINED_INPUT_TEMPLATE)]
        )

    if analyze_button:
        st.session_state['messages'] = ChatPromptTemplate(
            [SystemMessage(content=prompts.EVALUATION_SYSTEM_MESSAGE), ("human", prompts.COMBINED_INPUT_TEMPLATE)]
        )

    with st.spinner("Generating..."):
        # Parse the uploaded CV
        pdf_parser = PDFParser(file_path=st.session_state["uploaded_file"], chunk_size=1000)
        chunks = pdf_parser.get_chunks()

        resume_retriever = get_result_db_retriever(chunks)

        st.session_state["resume_content"] = "\n\n".join([doc.page_content for doc in resume_retriever])

        output = model_output(
            choose_provider,
            choose_model,
            st.session_state["resume_content"],
            st.session_state["job_desc"],
            suggest_improv_button,
        )
    st.write(output)


if __name__ == "__main__":
    main()
