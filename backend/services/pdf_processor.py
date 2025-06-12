import os
from typing import List, Dict, Any
from langchain.document_loaders.pdf import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from langchain_community.document_loaders import PyPDFLoader

from config import settings
import logging

logger = logging.getLogger(__name__)

class PDFProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=getattr(settings, "chunk_size", 800),
            chunk_overlap=getattr(settings, "chunk_overlap", 80),
            length_function=len,
            is_separator_regex=False,
        )

    def extract_text_from_pdf(self, file_path: str) -> List[Document]:
        """Extract text from PDF and return as list of Document objects with metadata."""
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        logger.info(f"Extracted {len(docs)} pages from {file_path}")
        return docs

    def split_into_chunks(self, documents: List[Document]) -> List[Document]:
        """Split page content into chunks."""
        chunks = self.text_splitter.split_documents(documents)
        logger.info(f"Split into {len(chunks)} chunks")
        return self._add_chunk_ids(chunks)

    def _add_chunk_ids(self, chunks: List[Document]) -> List[Document]:
        last_page_id = None
        current_chunk_index = 0
        for chunk in chunks:
            source = chunk.metadata.get("source")
            page = chunk.metadata.get("page")
            current_page_id = f"{source}:{page}"
            if current_page_id == last_page_id:
                current_chunk_index += 1
            else:
                current_chunk_index = 0
            chunk_id = f"{current_page_id}:{current_chunk_index}"
            last_page_id = current_page_id
            chunk.metadata["id"] = chunk_id
        return chunks

    def process_pdf(self, file_path: str) -> List[Document]:
        docs = self.extract_text_from_pdf(file_path)
        chunks = self.split_into_chunks(docs)
        return chunks
