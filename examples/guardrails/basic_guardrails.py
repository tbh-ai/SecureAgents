#!/usr/bin/env python3
# examples/guardrails/basic_guardrails.py
# Author: Saish (TBH.AI)

"""
Basic example demonstrating guardrails with TBH Secure Agents.
This example shows how to use guardrails to dynamically control expert behavior.
"""

import os
import sys
import logging

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import the TBH Secure Agents framework
from tbh_secure_agents import Expert, Operation, Squad

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def main():
    """
    Main function demonstrating basic guardrails with TBH Secure Agents.
    """
    print("\n" + "="*80)
    print("TBH SECURE AGENTS - BASIC GUARDRAILS EXAMPLE".center(80))
    print("="*80 + "\n")

    # Set your API key
    # You can also set this as an environment variable: GOOGLE_API_KEY
    api_key = os.environ.get('GOOGLE_API_KEY')
    if not api_key:
        print("Please set your GOOGLE_API_KEY environment variable.")
        return

    print("Creating experts with template variables...\n")

    # Create a content writer expert with template variables
    content_writer = Expert(
        specialty="Healthcare Content Writer",
        objective="Create high-quality, engaging content about healthcare topics tailored to {target_audience}",
        background="You have years of experience writing content for healthcare professionals and understand how to adapt {tone} tone, style, and complexity based on audience needs.",
        api_key=api_key
    )
    
    # Create a data analyst expert with template variables
    data_analyst = Expert(
        specialty="Healthcare Data Analyst",
        objective="Analyze healthcare data and provide insights about {analysis_focus} in a clear, concise manner",
        background="You have expertise in interpreting healthcare data and explaining complex findings in simple terms for {target_audience}.",
        api_key=api_key
    )

    print("Creating operations with template variables...\n")

    # Create operations for the experts with template variables
    writing_operation = Operation(
        instructions="Write a short blog post introduction about {topic}. Use a {tone} tone and target it to {target_audience}. Keep it between {word_count}.",
        output_format="A well-formatted blog post introduction (2-3 paragraphs)",
        expert=content_writer
    )
    
    analysis_operation = Operation(
        instructions="Analyze the provided healthcare data and create a summary of key insights about {analysis_focus}. {include_recommendations, select, true:Include practical recommendations based on the data.|false:Focus only on the insights without recommendations.}",
        output_format="A concise analysis with 3-5 key insights",
        expert=data_analyst
    )

    print("Creating a squad with the experts and operations...\n")

    # Create a squad with the experts and operations
    healthcare_squad = Squad(
        experts=[content_writer, data_analyst],
        operations=[writing_operation, analysis_operation]
    )

    print("Defining guardrail inputs...\n")

    # Define guardrail inputs
    guardrail_inputs = {
        # Shared parameters
        "target_audience": "primary care physicians",
        
        # Content writer parameters
        "topic": "The impact of AI on primary care practice",
        "tone": "professional",
        "word_count": "200-300 words",
        
        # Data analyst parameters
        "analysis_focus": "patient outcomes",
        "include_recommendations": True,
        
        # Sample data for the analysis
        "healthcare_data": {
            "patient_satisfaction": {
                "2020": 72,
                "2021": 78,
                "2022": 85
            },
            "readmission_rates": {
                "2020": 12.4,
                "2021": 10.8,
                "2022": 9.2
            },
            "average_wait_time": {
                "2020": 42,
                "2021": 38,
                "2022": 31
            }
        }
    }

    print("Guardrail inputs defined. Here are some key values:")
    print(f"  - Target audience: {guardrail_inputs['target_audience']}")
    print(f"  - Topic: {guardrail_inputs['topic']}")
    print(f"  - Tone: {guardrail_inputs['tone']}")
    print(f"  - Analysis focus: {guardrail_inputs['analysis_focus']}")
    print(f"  - Include recommendations: {guardrail_inputs['include_recommendations']}")

    print("\nDeploying the squad with guardrail inputs...\n")

    # Deploy the squad with the guardrail inputs
    try:
        result = healthcare_squad.deploy(guardrails=guardrail_inputs)

        print("\n" + "="*80)
        print("FINAL RESULT".center(80))
        print("="*80 + "\n")
        print(result)
        print("\n" + "="*80)

        # Save the output to a file
        output_file = os.path.join(os.path.dirname(__file__), "basic_guardrails_output.txt")
        with open(output_file, "w") as f:
            f.write("TBH SECURE AGENTS - BASIC GUARDRAILS EXAMPLE\n\n")
            f.write("Guardrail inputs:\n")
            for key, value in guardrail_inputs.items():
                if key != "healthcare_data":  # Skip the large data structure
                    f.write(f"  - {key}: {value}\n")
            f.write("\nResult:\n\n")
            f.write(result)
        
        print(f"\nOutput saved to {output_file}")

    except Exception as e:
        print(f"Error during squad deployment: {e}")

if __name__ == "__main__":
    main()
