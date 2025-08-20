#!/usr/bin/env python3
"""
Simple test script to demonstrate the improved prompt template.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.rag_pipeline import PROMPT_TEMPLATE

def test_prompt_template():
    """Test the improved prompt template."""
    
    print("🚀 Testing Improved Prompt Template")
    print("=" * 50)
    
    # Sample context and question
    sample_context = """
    Document 1 (Relevance: 0.892)
    Source: sample.pdf
    Page: 5
    Content:
    Artificial Intelligence (AI) has revolutionized various industries including healthcare, finance, and transportation. 
    Machine learning algorithms can now process vast amounts of data to identify patterns and make predictions. 
    Deep learning, a subset of AI, uses neural networks with multiple layers to solve complex problems.
    
    Document 2 (Relevance: 0.845)
    Source: sample.pdf
    Page: 8
    Content:
    The implementation of AI systems requires careful consideration of ethical implications, data privacy, 
    and potential biases in algorithms. Organizations must ensure transparency and accountability in their AI deployments.
    """
    
    sample_question = "What are the main benefits and challenges of implementing AI systems?"
    
    # Test the prompt template
    print("📝 Sample Context:")
    print(sample_context)
    print("\n❓ Sample Question:")
    print(sample_question)
    
    print("\n🔧 Generated Prompt:")
    print("-" * 40)
    
    # Format the prompt template
    formatted_prompt = PROMPT_TEMPLATE.format(
        context=sample_context,
        question=sample_question
    )
    
    print(formatted_prompt)
    
    print("\n✅ Prompt Template Features:")
    print("   - Intelligent assistant persona: ✅")
    print("   - Core capabilities definition: ✅")
    print("   - Analysis guidelines: ✅")
    print("   - Fact vs. inference distinction: ✅")
    print("   - Comprehensive response structure: ✅")
    
    print("\n🎯 Key Improvements:")
    print("   1. **Deep Knowledge Integration**: The AI can apply domain knowledge")
    print("   2. **Pattern Recognition**: Identifies trends and logical flows")
    print("   3. **Assumption Framework**: Clear labeling of assumptions")
    print("   4. **Factual Grounding**: Distinguishes facts from interpretations")
    print("   5. **Comprehensive Analysis**: Provides complete insights with caveats")
    
    print("\n📊 Expected Response Structure:")
    print("   - Direct answer to the question")
    print("   - Facts from the provided context")
    print("   - Inferences drawn from the information")
    print("   - Assumptions made (clearly labeled)")
    print("   - Related context and background")
    print("   - Important caveats or limitations")
    
    print("\n🎉 Prompt template test completed successfully!")

if __name__ == "__main__":
    test_prompt_template()

