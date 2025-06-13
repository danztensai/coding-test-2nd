from typing import List, Dict, Any
from langchain.schema import Document
from services.vector_store import VectorStoreService
from config import settings
import logging

from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
from utils.get_embedding_function import get_embedding_function
from utils.llm_provider import get_llm
from langchain_google_genai import ChatGoogleGenerativeAI


logger = logging.getLogger(__name__)

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

class RAGPipeline:
    def __init__(self):
        self.vector_store = VectorStoreService(
            persist_directory=settings.vector_db_path,
            embedding_function=get_embedding_function()
        )
        self.llm = get_llm()
        self.prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        self.k = getattr(settings, "RETRIEVAL_TOP_K", 5)

    def generate_answer(self, question: str, chat_history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        docs_with_scores = self._retrieve_documents(question)
        context = self._generate_context(docs_with_scores)
        answer = self._generate_llm_response(question, context, chat_history)
        sources = []
        for doc, score in docs_with_scores:
            sources.append({
                "content": doc.page_content,
                "page": doc.metadata.get("page", 0),
                "score": float(score),
                "metadata": doc.metadata
            })
        return {
            "answer": answer,
            "sources": sources
        }

    def _retrieve_documents(self, query: str) -> List[tuple]:
        results = self.vector_store.similarity_search_with_score(query, k=self.k)
        logger.info(f"Retrieved {len(results)} documents for query: {query}")
        return results

    def _generate_context(self, docs_with_scores: List[tuple]) -> str:
        return "\n\n---\n\n".join([doc.page_content for doc, _score in docs_with_scores])

    def _generate_llm_response(self, question: str, context: str, chat_history: List[Dict[str, str]] = None) -> str:
        history_text = ""
        if chat_history:
            for turn in chat_history:
                role = turn.get("role", "user").capitalize()
                content = turn.get("content", "")
                history_text += f"{role}: {content}\n"
        prompt = f"{history_text}\nContext:\n{context}\n\nQuestion: {question}\nAnswer:"

        response = self.llm.invoke(prompt)

        # Safely extract string
        return getattr(response, "content", response)
