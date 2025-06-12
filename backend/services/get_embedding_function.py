from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_community.embeddings.bedrock import BedrockEmbeddings
from langchain_openai.embeddings import OpenAIEmbeddings  # Add this import
from langchain_community.embeddings import HuggingFaceEmbeddings

def get_embedding_function():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return embeddings
