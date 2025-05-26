#!/usr/bin/env python3
"""
Example 2: AI Writer
===================

This example shows how to create an AI writer that can write content
with specific guidelines using guardrails and save to different formats.

Features demonstrated:
- Creating an Expert writer
- Using guardrails to control writing style
- Saving to different file formats
- Using result_destination
"""

import os

# Set your Google API key (replace with your actual key)
os.environ["GOOGLE_API_KEY"] = "your_google_api_key_here"

from tbh_secure_agents import Expert, Operation

def main():
    # Create outputs directory
    os.makedirs("outputs/user_examples", exist_ok=True)
    
    # Create an AI writer expert
    writer = Expert(
        specialty="Content Writer",
        objective="Create engaging and informative content",
        security_profile="minimal"  # Easy-to-use security setting
    )
    
    # Define guardrails to control the writing
    writing_guardrails = {
        "tone": "professional but friendly",
        "audience": "general public",
        "length": "medium-length article",
        "include_examples": True,
        "writing_style": "clear and engaging"
    }
    
    # Create a writing operation for blog post
    blog_operation = Operation(
        instructions="Write a blog post about the benefits of artificial intelligence in healthcare. Make it informative yet accessible to everyone.",
        output_format="A well-structured blog post with introduction, main points, and conclusion",
        expert=writer,
        result_destination="outputs/user_examples/ai_healthcare_blog.md"
    )
    
    # Create a writing operation for HTML format
    html_operation = Operation(
        instructions="Write a brief guide about getting started with Python programming. Include practical tips for beginners.",
        output_format="A beginner-friendly guide with clear steps",
        expert=writer,
        result_destination="outputs/user_examples/python_guide.html"
    )
    
    # Execute the blog writing
    print("✍️ Starting AI writing...")
    print("Task 1: Healthcare AI Blog Post")
    print("Output: outputs/user_examples/ai_healthcare_blog.md")
    print()
    
    try:
        result1 = blog_operation.execute(guardrails=writing_guardrails)
        print("✅ Blog post completed!")
        print(f"📄 Saved to: {blog_operation.result_destination}")
        print()
        
        # Execute the guide writing
        print("Task 2: Python Programming Guide")
        print("Output: outputs/user_examples/python_guide.html")
        print()
        
        result2 = html_operation.execute(guardrails=writing_guardrails)
        print("✅ Programming guide completed!")
        print(f"📄 Saved to: {html_operation.result_destination}")
        print()
        
        print("Preview of blog post:")
        print("-" * 50)
        print(result1[:300] + "..." if len(result1) > 300 else result1)
        
    except Exception as e:
        print(f"❌ Error during writing: {e}")

if __name__ == "__main__":
    main()
