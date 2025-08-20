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

PROMPT_TEMPLATE = """You are an intelligent assistant with deep knowledge across multiple domains. You excel at understanding complex information flows, identifying patterns, and providing insightful analysis. You can make reasonable assumptions based on your knowledge while staying grounded in facts.

**Your Core Capabilities:**
- Deep understanding of various subjects and their interconnections
- Ability to identify logical flows and patterns in information
- Skill at making educated assumptions when information is incomplete
- Commitment to factual accuracy while providing comprehensive insights
- Clear communication that distinguishes between facts and interpretations

**Context Information:**
{context}

**Analysis Guidelines:**
1. **Primary Source Focus**: Base your response primarily on the provided context
2. **Pattern Recognition**: Identify underlying patterns, trends, or logical flows in the information
3. **Knowledge Integration**: Apply your understanding of related concepts to enhance the analysis
4. **Assumption Framework**: When making assumptions:
   - Clearly label them as "Based on my understanding..." or "I can infer that..."
   - Ensure they are reasonable and logically sound
   - Explain the reasoning behind your assumptions
5. **Factual Grounding**: Always distinguish between:
   - **Facts**: Directly stated in the context
   - **Inferences**: Logical conclusions from the context
   - **Assumptions**: Reasonable extensions based on knowledge
6. **Comprehensive Response**: Provide:
   - Direct answer to the question
   - Relevant context and background
   - Logical flow of reasoning
   - Any important caveats or limitations

**Question:** {question}

**Response:**"""

class RAGPipeline:
    def __init__(self):
        self.vector_store = VectorStoreService(
            persist_directory=settings.vector_db_path,
            embedding_function=get_embedding_function()
        )
        self.llm = get_llm()
        self.prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        self.k = getattr(settings, "RETRIEVAL_TOP_K", 5)
        self.similarity_threshold = getattr(settings, "SIMILARITY_THRESHOLD", 0.7)

    def generate_answer(self, question: str, chat_history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """Generate an intelligent answer using enhanced RAG pipeline."""
        try:
            # Analyze and enhance the question
            enhanced_question = self._enhance_question(question, chat_history)
            
            # Retrieve relevant documents
            docs_with_scores = self._retrieve_documents(enhanced_question)
            
            # Generate enhanced context
            context = self._generate_context(docs_with_scores)
            
            # Generate intelligent response
            answer = self._generate_llm_response(question, context, chat_history)
            
            # Prepare sources with enhanced metadata
            sources = []
            for doc, score in docs_with_scores:
                sources.append({
                    "content": doc.page_content[:500] + "..." if len(doc.page_content) > 500 else doc.page_content,
                    "page": doc.metadata.get("page", 0),
                    "score": float(score),
                    "source": doc.metadata.get("source", "Unknown"),
                    "metadata": doc.metadata
                })
            
            return {
                "answer": answer,
                "sources": sources,
                "question_enhanced": enhanced_question,
                "context_length": len(context),
                "documents_retrieved": len(docs_with_scores)
            }
            
        except Exception as e:
            logger.error(f"Error in generate_answer: {str(e)}")
            return {
                "answer": f"I apologize, but I encountered an error while processing your question. Please try again or contact support if the issue persists.",
                "sources": [],
                "error": str(e)
            }

    def _enhance_question(self, question: str, chat_history: List[Dict[str, str]] = None) -> str:
        """Enhance the question with context from chat history and domain knowledge."""
        enhanced_question = question
        
        # Add context from recent chat history
        if chat_history:
            recent_context = []
            for turn in chat_history[-2:]:  # Last 2 turns
                if turn.get("role") == "user":
                    recent_context.append(turn.get("content", ""))
            
            if recent_context:
                context_text = " ".join(recent_context)
                enhanced_question = f"Context from recent conversation: {context_text}\n\nCurrent question: {question}"
        
        return enhanced_question

    def _retrieve_documents(self, query: str) -> List[tuple]:
        results = self.vector_store.similarity_search_with_score(query, k=self.k)
        
        # Filter results based on similarity threshold
        filtered_results = []
        for doc, score in results:
            if score >= self.similarity_threshold:
                filtered_results.append((doc, score))
        
        if not filtered_results:
            logger.warning(f"No documents met similarity threshold {self.similarity_threshold} for query: {query}")
            # Return top result even if below threshold
            filtered_results = results[:1] if results else []
        
        logger.info(f"Retrieved {len(filtered_results)} relevant documents for query: {query}")
        return filtered_results

    def _generate_context(self, docs_with_scores: List[tuple]) -> str:
        """Generate enhanced context with metadata and relevance information."""
        context_parts = []
        
        for i, (doc, score) in enumerate(docs_with_scores, 1):
            # Extract metadata
            metadata = doc.metadata
            source = metadata.get('source', 'Unknown')
            page = metadata.get('page', 'N/A')
            
            # Create context entry with relevance score
            context_entry = f"""Document {i} (Relevance: {score:.3f})
Source: {source}
Page: {page}
Content:
{doc.page_content}"""
            
            context_parts.append(context_entry)
        
        return "\n\n" + "="*50 + "\n\n".join(context_parts)

    def _generate_llm_response(self, question: str, context: str, chat_history: List[Dict[str, str]] = None) -> str:
        """Generate LLM response using the enhanced prompt template."""
        try:
            # Prepare conversation history if available
            messages = []
            
            # Add system message with enhanced prompt
            system_message = PROMPT_TEMPLATE.format(context=context, question=question)
            messages.append({"role": "system", "content": system_message})
            
            # Add conversation history if available
            if chat_history:
                for turn in chat_history[-3:]:  # Keep last 3 turns for context
                    role = turn.get("role", "user")
                    content = turn.get("content", "")
                    if role and content:
                        messages.append({"role": role, "content": content})
            
            # Generate response using the LLM
            if hasattr(self.llm, 'invoke'):
                # For LangChain LLMs
                response = self.llm.invoke(system_message)
                return getattr(response, "content", str(response))
            else:
                # For direct LLM calls
                response = self.llm(system_message)
                return str(response)
                
        except Exception as e:
            logger.error(f"Error generating LLM response: {str(e)}")
            return f"I apologize, but I encountered an error while processing your question. Please try rephrasing your question or contact support if the issue persists. Error: {str(e)}"
