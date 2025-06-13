from langchain_community.llms.ollama import Ollama
from langchain_google_genai import ChatGoogleGenerativeAI
from config import settings


def get_llm():
    provider = getattr(settings, "llm_provider", "ollama").lower()
    
    if provider == "ollama":
        return Ollama(
            model=settings.llm_model,
            base_url=settings.ollama_base_url,
            temperature=settings.llm_temperature
        )
    
    elif provider == "google":
        return ChatGoogleGenerativeAI(
            model=settings.llm_model,
            google_api_key=settings.google_api_key
        )
    
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")
