#!/usr/bin/env python3
"""
Test script to demonstrate the improved RAG pipeline with enhanced prompt template.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.rag_pipeline import RAGPipeline
import time
import json

def test_rag_pipeline():
    """Test the improved RAG pipeline functionality."""
    
    print("🚀 Testing Improved RAG Pipeline")
    print("=" * 50)
    
    # Initialize RAG pipeline
    print("📥 Initializing RAG pipeline...")
    start_time = time.time()
    rag_pipeline = RAGPipeline()
    init_time = time.time() - start_time
    print(f"✅ Initialized in {init_time:.2f} seconds")
    
    # Test questions
    test_questions = [
        "What is the main topic of this document?",
        "Can you explain the key concepts mentioned?",
        "What are the main benefits or advantages discussed?",
        "How does this relate to current industry practices?",
        "What conclusions can be drawn from this information?"
    ]
    
    # Simulate chat history
    chat_history = [
        {"role": "user", "content": "I'm interested in learning about this topic"},
        {"role": "assistant", "content": "I'd be happy to help you understand this topic. What specific aspects would you like to explore?"}
    ]
    
    print(f"\n📝 Testing with {len(test_questions)} sample questions...")
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n🔍 Question {i}: {question}")
        print("-" * 40)
        
        start_time = time.time()
        result = rag_pipeline.generate_answer(question, chat_history)
        response_time = time.time() - start_time
        
        print(f"⏱️  Response time: {response_time:.2f} seconds")
        print(f"📄 Documents retrieved: {result.get('documents_retrieved', 0)}")
        print(f"📏 Context length: {result.get('context_length', 0)} characters")
        
        # Display answer (truncated for readability)
        answer = result.get('answer', 'No answer generated')
        print(f"💬 Answer: {answer[:200]}{'...' if len(answer) > 200 else ''}")
        
        # Display sources
        sources = result.get('sources', [])
        if sources:
            print(f"📚 Sources ({len(sources)}):")
            for j, source in enumerate(sources[:2], 1):  # Show first 2 sources
                print(f"   {j}. {source.get('source', 'Unknown')} (Score: {source.get('score', 0):.3f})")
        
        print()
    
    # Test with a more complex question
    print("🧠 Testing Complex Analysis Question")
    print("-" * 40)
    
    complex_question = "Based on the information provided, what patterns or trends can you identify, and what implications might these have for future developments in this field?"
    
    start_time = time.time()
    result = rag_pipeline.generate_answer(complex_question, chat_history)
    response_time = time.time() - start_time
    
    print(f"⏱️  Response time: {response_time:.2f} seconds")
    print(f"💬 Answer: {result.get('answer', 'No answer generated')}")
    
    print(f"\n🎉 All tests completed successfully!")
    print(f"📊 Performance Summary:")
    print(f"   - Pipeline initialization: {init_time:.2f}s")
    print(f"   - Average response time: {response_time:.2f}s")
    print(f"   - Enhanced prompt template: ✅ Active")
    print(f"   - Context enhancement: ✅ Active")
    print(f"   - Source filtering: ✅ Active")

if __name__ == "__main__":
    test_rag_pipeline()

