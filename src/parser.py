import tempfile
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Iterable

from langchain_community.document_loaders.pdf import BaseLoader
from langchain_core.documents import Document
from langchain_pymupdf4llm import PyMuPDF4LLMLoader
from langchain_text_splitters import MarkdownTextSplitter, RecursiveCharacterTextSplitter
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
    parser: Callable[..., BaseLoader] = field(default=PyMuPDF4LLMLoader)
    text_splitter: Callable[..., RecursiveCharacterTextSplitter] = field(default=MarkdownTextSplitter)
    chunk_size: int = 500
    lazy: bool = False

    def __post_init__(self):
        if isinstance(self.file_path, Path):
            if not self.file_path.exists():
                raise FileNotFoundError(f"{self.file_path} does not exist.")

        elif isinstance(self.file_path, UploadedFile):
            self.file_path = Path(self._save_temp_pdf(self.file_path))

        assert self.file_path.suffix.lower() == '.pdf', "File must be a PDF."

        self._text_splitter = self.text_splitter(
            chunk_size=self.chunk_size,
            chunk_overlap=50,
            length_function=len,
        )

        self._parser_instance = self.parser(file_path=self.file_path)

    def get_chunks(self):
        """
        Get text chunks from the PDF file.

        Returns:
            list[Document]: A list of text chunks as Document objects.
        """
        text_content = self._parse_file()
        return self._text_splitter.split_documents(text_content)

    def _parse_file(self):
        return self._parser_instance.lazy_load() if self.lazy else self._parser_instance.load()

    def _save_temp_pdf(self, uploaded_file: UploadedFile) -> str:
        """
        Save uploaded PDF to a temporary location in /tmp.
        """
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getbuffer())
            tmp_path = tmp_file.name
        return tmp_path
