from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_community.embeddings.bedrock import BedrockEmbeddings
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from config import settings

def get_embedding_function():
    provider = getattr(settings, "embedding_provider", "huggingface").lower()
    model_name = getattr(settings, "embedding_model", "all-MiniLM-L6-v2")

    if provider == "openai":
        return OpenAIEmbeddings(model=model_name, openai_api_key=settings.openai_api_key)
    elif provider == "ollama":
        return OllamaEmbeddings(model=model_name)
    elif provider == "bedrock":
        return BedrockEmbeddings(model_id=model_name)
    else:
        return HuggingFaceEmbeddings(model_name=model_name)
