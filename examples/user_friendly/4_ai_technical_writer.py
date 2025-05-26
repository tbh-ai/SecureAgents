#!/usr/bin/env python3
"""
Example 4: AI Marketing Strategist
==================================

This example shows how to create an AI marketing strategist that creates
marketing campaigns and strategies for different products.

Features demonstrated:
- Creating a Marketing Strategist expert
- Using guardrails for campaign parameters
- Saving to HTML format for presentations
"""

import os

# Set your Google API key (replace with your actual key)
os.environ["GOOGLE_API_KEY"] = "AIzaSyA3ZxbIXpR3yNkZwGDznrztdQmgnU16DJI"

from tbh_secure_agents import Expert, Operation

def main():
    # Create outputs directory
    os.makedirs("outputs/user_examples", exist_ok=True)

    # Create an AI technical writer expert
    tech_writer = Expert(
        specialty="Technical Writer",
        objective="Create clear, comprehensive technical documentation",
        security_profile="minimal"
    )

    # Define guardrails for technical writing
    writing_guardrails = {
        "no_harmful_content": True,
        "professional_tone": True,
        "factual_content": True,
        "secure_coding": True,
        "documentation_type": "user guide",
        "technical_level": "beginner to intermediate",
        "include_examples": True,
        "include_troubleshooting": True,
        "format_style": "professional documentation",
        "section_structure": "hierarchical with clear headings"
    }

    # Create a technical writing operation
    documentation_operation = Operation(
        instructions="Create a comprehensive user guide for getting started with machine learning using Python. Include installation steps, basic concepts, and practical examples.",
        output_format="Professional technical documentation with clear sections, examples, and troubleshooting tips",
        expert=tech_writer,
        result_destination="outputs/user_examples/ml_getting_started_guide.pdf"
    )

    # Execute the technical writing
    print("📝 Starting AI technical writing...")
    print("Document: Machine Learning Getting Started Guide")
    print("Format: Professional PDF")
    print("Output: outputs/user_examples/ml_getting_started_guide.pdf")
    print()

    try:
        result = documentation_operation.execute(guardrails=writing_guardrails)
        print("✅ Technical documentation completed successfully!")
        print(f"📄 Results saved to: {documentation_operation.result_destination}")
        print()
        print("Preview of documentation:")
        print("-" * 50)
        print(result[:300] + "..." if len(result) > 300 else result)

    except Exception as e:
        print(f"❌ Error during technical writing: {e}")

if __name__ == "__main__":
    main()
