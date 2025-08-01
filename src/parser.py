# from langchain_community.document_loaders import PyPDFLoader
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter, TextSplitter
from pypdf import PdfReader
from streamlit.runtime.uploaded_file_manager import UploadedFile


class BaseParser(ABC):
    @abstractmethod
    def get_chunks(self) -> list[Document]:
        """
        Abstract method to get text chunks from a file.
        """
        pass

    @abstractmethod
    def _parse_file(self) -> Iterable[Document] | list[Document]:
        """
        Abstract method to parse the file and return text content.
        """
        pass


@dataclass
class PDFParser(BaseParser):
    file_path: Path | UploadedFile
    text_splitter: TextSplitter = field(default_factory=RecursiveCharacterTextSplitter)
    chunk_size: int = 500
    lazy: bool = False

    def __post_init__(self):
        if isinstance(self.file_path, Path):
            if not self.file_path.exists():
                raise FileNotFoundError(f"{self.file_path} does not exist.")

            assert self.file_path.suffix.lower() == '.pdf', "File must be a PDF."

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=50,
            length_function=len,
        )

    def get_chunks(self) -> list[Document]:
        """
        Get text chunks from the PDF file.

        Returns:
            list[Document]: A list of text chunks as Document objects.
        """
        text_content = self._parse_file()
        return self.text_splitter.split_documents(text_content)

    def _parse_file(self) -> Iterable[Document] | list[Document]:
        pdf_reader = PdfReader(self.file_path)
        pdf_text = ""
        for page in pdf_reader.pages:
            pdf_text += page.extract_text()
        documents = [Document(page_content=pdf_text, metadata={"source": str(self.file_path)})]

        return documents
