#!/usr/bin/env python3
"""
Test script to demonstrate improved HuggingFace embeddings functionality.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.get_embedding_function import (
    get_embedding_function, 
    get_embedding_dimensions,
    get_recommended_model,
    list_available_models
)
import time
import numpy as np

def test_embeddings():
    """Test the improved embedding functionality."""
    
    print("🚀 Testing Improved HuggingFace Embeddings")
    print("=" * 50)
    
    # Get the embedding function
    print("📥 Initializing embedding function...")
    start_time = time.time()
    embedding_function = get_embedding_function()
    init_time = time.time() - start_time
    print(f"✅ Initialized in {init_time:.2f} seconds")
    
    # Test texts
    test_texts = [
        "This is a sample document about artificial intelligence.",
        "Machine learning is a subset of AI that focuses on algorithms.",
        "Natural language processing helps computers understand human language.",
        "Deep learning uses neural networks with multiple layers.",
        "Computer vision enables machines to interpret visual information."
    ]
    
    print(f"\n📝 Testing with {len(test_texts)} sample texts...")
    
    # Generate embeddings
    start_time = time.time()
    embeddings = embedding_function.embed_documents(test_texts)
    embed_time = time.time() - start_time
    
    print(f"✅ Generated embeddings in {embed_time:.2f} seconds")
    print(f"📊 Average time per text: {embed_time/len(test_texts):.3f} seconds")
    
    # Check embedding dimensions
    model_name = getattr(embedding_function, 'model_name', 'unknown')
    dimensions = get_embedding_dimensions(model_name)
    if dimensions:
        print(f"📏 Embedding dimensions: {dimensions}")
    
    # Test similarity
    print(f"\n🔍 Testing similarity between first two texts...")
    embedding1 = embeddings[0]
    embedding2 = embeddings[1]
    
    # Calculate cosine similarity
    similarity = np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))
    print(f"📈 Cosine similarity: {similarity:.4f}")
    
    # Test single text embedding
    print(f"\n🔤 Testing single text embedding...")
    start_time = time.time()
    single_embedding = embedding_function.embed_query("This is a single query text.")
    single_time = time.time() - start_time
    print(f"✅ Single embedding generated in {single_time:.3f} seconds")
    
    print(f"\n🎉 All tests completed successfully!")
    print(f"📊 Performance Summary:")
    print(f"   - Initialization: {init_time:.2f}s")
    print(f"   - Batch embedding: {embed_time:.2f}s ({embed_time/len(test_texts):.3f}s per text)")
    print(f"   - Single embedding: {single_time:.3f}s")
    
    # Test utility functions
    print(f"\n🔧 Testing Utility Functions:")
    print(f"   - Recommended model for general use: {get_recommended_model('general', 'balanced')}")
    print(f"   - Recommended model for multilingual: {get_recommended_model('multilingual', 'speed')}")
    print(f"   - Recommended model for semantic search: {get_recommended_model('semantic_search', 'quality')}")
    
    # Show available models
    print(f"\n📋 Available Models:")
    models = list_available_models()
    for model_name, info in models.items():
        print(f"   - {model_name}: {info['dimensions']}d, {info['speed']}, {info['quality']}")

if __name__ == "__main__":
    test_embeddings()
