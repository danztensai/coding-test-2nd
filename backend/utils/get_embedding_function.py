from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_community.embeddings.bedrock import BedrockEmbeddings
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from config import settings
import torch
import logging
from typing import Optional

logger = logging.getLogger(__name__)

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
        return _get_optimized_huggingface_embeddings(model_name)

def _get_optimized_huggingface_embeddings(model_name: str) -> HuggingFaceEmbeddings:
    """
    Create an optimized HuggingFaceEmbeddings instance with better performance settings.
    
    Args:
        model_name: The name of the HuggingFace model to use
        
    Returns:
        HuggingFaceEmbeddings: Configured embedding model
    """
    try:
        # Determine the best device to use
        device = _get_optimal_device()
        
        # Get model-specific configurations
        model_config = _get_model_config(model_name)
        
        # Create embeddings with optimized settings
        embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={
                'device': device,
                'trust_remote_code': True,
                **model_config.get('model_kwargs', {})
            },
            encode_kwargs={
                'batch_size': model_config.get('batch_size', 32),
                'normalize_embeddings': True,  # Important for cosine similarity
                **model_config.get('encode_kwargs', {})
            },
            cache_folder=model_config.get('cache_folder', None)
        )
        
        logger.info(f"Initialized HuggingFace embeddings with model: {model_name} on device: {device}")
        return embeddings
        
    except Exception as e:
        logger.error(f"Failed to initialize HuggingFace embeddings with model {model_name}: {str(e)}")
        # Fallback to basic configuration
        logger.info("Falling back to basic HuggingFace embeddings configuration")
        return HuggingFaceEmbeddings(model_name=model_name)

def _get_optimal_device() -> str:
    """
    Determine the optimal device for running the embedding model.
    
    Returns:
        str: Device identifier ('cuda', 'mps', or 'cpu')
    """
    if torch.cuda.is_available():
        return 'cuda'
    elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
        return 'mps'
    else:
        return 'cpu'

def _get_model_config(model_name: str) -> dict:
    """
    Get model-specific configuration for optimal performance.
    
    Args:
        model_name: The name of the HuggingFace model
        
    Returns:
        dict: Model-specific configuration
    """
    # Default configuration
    default_config = {
        'batch_size': 32,
        'model_kwargs': {},
        'encode_kwargs': {},
        'cache_folder': None
    }
    
    # Model-specific optimizations
    model_configs = {
        # Sentence Transformers models
        'all-MiniLM-L6-v2': {
            'batch_size': 64,  # Smaller model, can handle larger batches
            'model_kwargs': {},
            'encode_kwargs': {'convert_to_tensor': True}
        },
        'all-mpnet-base-v2': {
            'batch_size': 32,
            'model_kwargs': {},
            'encode_kwargs': {'convert_to_tensor': True}
        },
        'sentence-transformers/all-MiniLM-L6-v2': {
            'batch_size': 64,
            'model_kwargs': {},
            'encode_kwargs': {'convert_to_tensor': True}
        },
        'sentence-transformers/all-mpnet-base-v2': {
            'batch_size': 32,
            'model_kwargs': {},
            'encode_kwargs': {'convert_to_tensor': True}
        },
        # BGE models
        'BAAI/bge-small-en-v1.5': {
            'batch_size': 32,
            'model_kwargs': {},
            'encode_kwargs': {'convert_to_tensor': True}
        },
        'BAAI/bge-base-en-v1.5': {
            'batch_size': 16,
            'model_kwargs': {},
            'encode_kwargs': {'convert_to_tensor': True}
        },
        'BAAI/bge-large-en-v1.5': {
            'batch_size': 8,
            'model_kwargs': {},
            'encode_kwargs': {'convert_to_tensor': True}
        },
        # E5 models
        'intfloat/e5-small-v2': {
            'batch_size': 32,
            'model_kwargs': {},
            'encode_kwargs': {'convert_to_tensor': True}
        },
        'intfloat/e5-base-v2': {
            'batch_size': 16,
            'model_kwargs': {},
            'encode_kwargs': {'convert_to_tensor': True}
        },
        'intfloat/e5-large-v2': {
            'batch_size': 8,
            'model_kwargs': {},
            'encode_kwargs': {'convert_to_tensor': True}
        }
    }
    
    # Return model-specific config or default
    return model_configs.get(model_name, default_config)

def get_embedding_dimensions(model_name: str) -> Optional[int]:
    """
    Get the embedding dimensions for a given model.
    
    Args:
        model_name: The name of the HuggingFace model
        
    Returns:
        int: Number of embedding dimensions, or None if unknown
    """
    dimension_map = {
        'all-MiniLM-L6-v2': 384,
        'all-mpnet-base-v2': 768,
        'sentence-transformers/all-MiniLM-L6-v2': 384,
        'sentence-transformers/all-mpnet-base-v2': 768,
        'BAAI/bge-small-en-v1.5': 384,
        'BAAI/bge-base-en-v1.5': 768,
        'BAAI/bge-large-en-v1.5': 1024,
        'intfloat/e5-small-v2': 384,
        'intfloat/e5-base-v2': 768,
        'intfloat/e5-large-v2': 1024
    }
    
    return dimension_map.get(model_name)

def get_recommended_model(use_case: str = "general", performance_priority: str = "balanced") -> str:
    """
    Get a recommended embedding model based on use case and performance requirements.
    
    Args:
        use_case: The intended use case ('general', 'multilingual', 'semantic_search', 'classification')
        performance_priority: Performance priority ('speed', 'balanced', 'quality')
        
    Returns:
        str: Recommended model name
    """
    recommendations = {
        'general': {
            'speed': 'all-MiniLM-L6-v2',
            'balanced': 'all-mpnet-base-v2',
            'quality': 'BAAI/bge-base-en-v1.5'
        },
        'multilingual': {
            'speed': 'BAAI/bge-small-en-v1.5',
            'balanced': 'BAAI/bge-base-en-v1.5',
            'quality': 'BAAI/bge-large-en-v1.5'
        },
        'semantic_search': {
            'speed': 'all-MiniLM-L6-v2',
            'balanced': 'intfloat/e5-base-v2',
            'quality': 'intfloat/e5-large-v2'
        },
        'classification': {
            'speed': 'all-MiniLM-L6-v2',
            'balanced': 'all-mpnet-base-v2',
            'quality': 'BAAI/bge-base-en-v1.5'
        }
    }
    
    return recommendations.get(use_case, {}).get(performance_priority, 'all-MiniLM-L6-v2')

def list_available_models() -> dict:
    """
    List all available models with their specifications.
    
    Returns:
        dict: Dictionary with model information
    """
    return {
        'all-MiniLM-L6-v2': {
            'dimensions': 384,
            'speed': 'fast',
            'quality': 'good',
            'multilingual': False,
            'recommended_for': ['general', 'classification']
        },
        'all-mpnet-base-v2': {
            'dimensions': 768,
            'speed': 'medium',
            'quality': 'very_good',
            'multilingual': False,
            'recommended_for': ['general', 'semantic_search']
        },
        'BAAI/bge-small-en-v1.5': {
            'dimensions': 384,
            'speed': 'fast',
            'quality': 'very_good',
            'multilingual': True,
            'recommended_for': ['multilingual', 'general']
        },
        'BAAI/bge-base-en-v1.5': {
            'dimensions': 768,
            'speed': 'medium',
            'quality': 'excellent',
            'multilingual': True,
            'recommended_for': ['multilingual', 'semantic_search']
        },
        'BAAI/bge-large-en-v1.5': {
            'dimensions': 1024,
            'speed': 'slow',
            'quality': 'best',
            'multilingual': True,
            'recommended_for': ['multilingual', 'high_quality']
        },
        'intfloat/e5-base-v2': {
            'dimensions': 768,
            'speed': 'medium',
            'quality': 'excellent',
            'multilingual': False,
            'recommended_for': ['semantic_search', 'retrieval']
        },
        'intfloat/e5-large-v2': {
            'dimensions': 1024,
            'speed': 'slow',
            'quality': 'best',
            'multilingual': False,
            'recommended_for': ['semantic_search', 'high_quality']
        }
    }
