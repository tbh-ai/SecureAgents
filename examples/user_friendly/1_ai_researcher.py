#!/usr/bin/env python3
"""
Example 1: AI Researcher
========================

This example shows how to create an AI researcher that can research any topic
and save the results to a markdown file.

Features demonstrated:
- Creating an Expert with minimal security
- Creating an Operation with result_destination
- Simple research workflow
"""

import os

# Set your Google API key (replace with your actual key)
# os.environ["GOOGLE_API_KEY"] = "your-api-key-here"

from tbh_secure_agents import Expert, Operation, Squad

def main():
    # Create outputs directory
    os.makedirs("outputs/user_examples", exist_ok=True)

    # Create an AI researcher expert with template variables
    researcher = Expert(
        specialty="AI Researcher specializing in {research_topic}",
        objective="Research {research_topic} and provide {research_depth} information",
        security_profile="minimal"  # Easy-to-use security setting
    )

    # Define guardrails for research
    research_guardrails = {
        "research_topic": "renewable energy technology",
        "research_depth": "comprehensive",
        "focus_areas": "innovations, market trends, future outlook",
        "tone": "professional",
        "include_sources": True
    }

    # Create a research operation with template variables
    research_operation = Operation(
        instructions="Research the latest developments in {research_topic}. Focus on {focus_areas}. Use a {tone} tone and provide {research_depth} analysis.",
        output_format="A {research_depth} research report with clear sections and bullet points",
        expert=researcher,
        result_destination="outputs/user_examples/renewable_energy_research.md"
    )

    # Execute the research
    print("Starting AI research...")

    try:
        result = research_operation.execute(guardrails=research_guardrails)
        print("Research completed successfully!")
        print(f"Results saved to: {research_operation.result_destination}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
