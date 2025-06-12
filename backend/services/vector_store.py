from typing import List, Tuple
from langchain.schema import Document
from langchain.vectorstores.chroma import Chroma
from config import settings
import logging

logger = logging.getLogger(__name__)

class VectorStoreService:
    def __init__(self, persist_directory: str = None, embedding_function=None):
        self.persist_directory = persist_directory or settings.vector_db_path
        self.embedding_function = embedding_function or settings.get_embedding_function()
        self.db = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embedding_function
        )

    def add_documents(self, documents: List[Document], batch_size: int = 100) -> None:
        """Add documents to the vector store in batches to avoid exceeding max batch size."""
        ids = [doc.metadata.get("id") for doc in documents]
        for i in range(0, len(documents), batch_size):
            batch_docs = documents[i:i+batch_size]
            batch_ids = ids[i:i+batch_size]
            self.db.add_documents(batch_docs, ids=batch_ids)
        self.db.persist()
        logger.info(f"Added {len(documents)} documents to vector store.")

    def similarity_search_with_score(self, query: str, k: int = 5) -> List[Tuple[Document, float]]:
        results = self.db.similarity_search_with_score(query, k=k)
        logger.info(f"Similarity search returned {len(results)} results for query: {query}")
        return results

    def similarity_search(self, query: str, k: int = 5) -> List[Document]:
        docs = self.db.similarity_search(query, k=k)
        logger.info(f"Similarity search returned {len(docs)} documents for query: {query}")
        return docs

    def delete_documents(self, document_ids: List[str]) -> None:
        self.db.delete(ids=document_ids)
        self.db.persist()
        logger.info(f"Deleted {len(document_ids)} documents from vector store.")

    def get_document_count(self) -> int:
        items = self.db.get(include=[])
        count = len(items["ids"])
        logger.info(f"Vector store contains {count} documents.")
        return count
