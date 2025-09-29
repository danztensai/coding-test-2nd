# HuggingFace Embeddings Improvements

## Overview

The HuggingFace embeddings implementation has been significantly improved with better performance, error handling, and optimization features.

## Key Improvements

### 1. **Automatic Device Detection**
- Automatically detects and uses the best available device (CUDA GPU, Apple M1/M2 MPS, or CPU)
- Optimizes performance based on available hardware

### 2. **Model-Specific Optimizations**
- Pre-configured settings for popular embedding models:
  - **Sentence Transformers**: `all-MiniLM-L6-v2`, `all-mpnet-base-v2`
  - **BGE Models**: `bge-small-en-v1.5`, `bge-base-en-v1.5`, `bge-large-en-v1.5`
  - **E5 Models**: `e5-small-v2`, `e5-base-v2`, `e5-large-v2`

### 3. **Performance Optimizations**
- **Batch Processing**: Optimized batch sizes for each model type
- **Normalized Embeddings**: Automatic normalization for better cosine similarity
- **Tensor Conversion**: Efficient tensor operations
- **Progress Bar Control**: Reduced logging noise

### 4. **Error Handling & Fallback**
- Graceful error handling with fallback to basic configuration
- Comprehensive logging for debugging
- Automatic recovery from initialization failures

### 5. **Enhanced Configuration**
- Model-specific batch sizes and parameters
- Device mapping optimization
- Cache folder management

## Supported Models

### High-Performance Models (Recommended)
```bash
# Fast and efficient
EMBEDDING_MODEL=all-MiniLM-L6-v2

# Better quality, slightly slower
EMBEDDING_MODEL=all-mpnet-base-v2

# Multilingual support
EMBEDDING_MODEL=BAAI/bge-small-en-v1.5
```

### Advanced Models
```bash
# High quality embeddings
EMBEDDING_MODEL=BAAI/bge-base-en-v1.5
EMBEDDING_MODEL=intfloat/e5-base-v2

# Best quality (requires more resources)
EMBEDDING_MODEL=BAAI/bge-large-en-v1.5
EMBEDDING_MODEL=intfloat/e5-large-v2
```

## Configuration

### Environment Variables
```bash
# Set embedding provider to huggingface
EMBEDDING_PROVIDER=huggingface

# Choose your preferred model
EMBEDDING_MODEL=all-MiniLM-L6-v2

# Optional: Set cache directory
HF_HOME=/path/to/cache
```

### Model Performance Comparison

| Model | Dimensions | Speed | Quality | Memory |
|-------|------------|-------|---------|--------|
| all-MiniLM-L6-v2 | 384 | ⚡⚡⚡ | ⭐⭐ | 💾 |
| all-mpnet-base-v2 | 768 | ⚡⚡ | ⭐⭐⭐ | 💾💾 |
| bge-small-en-v1.5 | 384 | ⚡⚡⚡ | ⭐⭐⭐ | 💾 |
| bge-base-en-v1.5 | 768 | ⚡⚡ | ⭐⭐⭐⭐ | 💾💾 |
| bge-large-en-v1.5 | 1024 | ⚡ | ⭐⭐⭐⭐⭐ | 💾💾💾 |

## Usage Examples

### Basic Usage
```python
from utils.get_embedding_function import get_embedding_function

# Get optimized embedding function
embedding_function = get_embedding_function()

# Generate embeddings
texts = ["Hello world", "How are you?"]
embeddings = embedding_function.embed_documents(texts)
```

### Single Query
```python
# For single text queries
query_embedding = embedding_function.embed_query("What is machine learning?")
```

### Get Model Information
```python
from utils.get_embedding_function import get_embedding_dimensions

# Get embedding dimensions for a model
dimensions = get_embedding_dimensions("all-MiniLM-L6-v2")
print(f"Embedding dimensions: {dimensions}")  # Output: 384
```

## Testing

Run the test script to verify the improvements:

```bash
cd backend
python test_embeddings.py
```

This will test:
- Initialization performance
- Batch embedding speed
- Single query performance
- Similarity calculations
- Error handling

## Performance Tips

1. **Use GPU**: Ensure CUDA is available for best performance
2. **Batch Processing**: Process multiple texts together when possible
3. **Model Selection**: Choose models based on your quality vs speed requirements
4. **Memory Management**: Larger models require more RAM/VRAM

## Troubleshooting

### Common Issues

1. **CUDA Out of Memory**
   - Reduce batch size in model configuration
   - Use smaller models
   - Process texts in smaller batches

2. **Slow Performance**
   - Check if GPU is being used: `print(torch.cuda.is_available())`
   - Verify model is cached locally
   - Consider using a faster model

3. **Model Download Issues**
   - Check internet connection
   - Verify model name is correct
   - Clear cache and retry

### Debug Mode
Enable detailed logging by setting:
```bash
LOG_LEVEL=DEBUG
```

## Migration from Old Implementation

The new implementation is backward compatible. No changes needed to existing code that uses `get_embedding_function()`.

## Future Enhancements

- [ ] Support for more embedding models
- [ ] Automatic model performance benchmarking
- [ ] Dynamic batch size optimization
- [ ] Multi-GPU support
- [ ] Model quantization for faster inference
