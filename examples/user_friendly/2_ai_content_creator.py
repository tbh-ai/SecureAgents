#!/usr/bin/env python3
"""
Example 2: AI Code Developer
============================

This example shows how to create an AI code developer that writes
code with specific requirements using guardrails.

Features demonstrated:
- Creating a Code Developer expert
- Using guardrails for code requirements
- Saving to Python file format
"""

import os

# Set your Google API key (replace with your actual key)
os.environ["GOOGLE_API_KEY"] = "AIzaSyA3ZxbIXpR3yNkZwGDznrztdQmgnU16DJI"

from tbh_secure_agents import Expert, Operation, Squad

def main():
    # Create outputs directory
    os.makedirs("outputs/user_examples", exist_ok=True)

    # Create an AI content creator expert with template variables
    content_creator = Expert(
        specialty="Content Creator specializing in {content_type}",
        objective="Create {tone} content for {target_audience}",
        security_profile="minimal"
    )

    # Define guardrails for content creation
    content_guardrails = {
        "topic": "work-life balance in the modern workplace",
        "tone": "friendly and engaging",
        "target_audience": "young professionals",
        "content_type": "social media post",
        "include_call_to_action": True,
        "word_limit": 300
    }

    # Create a content creation operation with template variables
    content_operation = Operation(
        instructions="Create a {content_type} about {topic}. Use a {tone} tone for {target_audience}. Keep it under {word_limit} words.",
        output_format="An engaging {content_type} with hashtags and call-to-action",
        expert=content_creator,
        result_destination="outputs/user_examples/work_life_balance_post.html"
    )

    # Execute the content creation
    print("Starting content creation...")

    try:
        result = content_operation.execute(guardrails=content_guardrails)
        print("Content creation completed successfully!")
        print(f"Results saved to: {content_operation.result_destination}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
