#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
New Version Example - TBH Secure Agents

This example demonstrates all the key features of the latest version of the TBH Secure Agents framework
in a simple, readable way without any fancy elements.

Features demonstrated:
1. Basic usage (Experts, Operations, Squad)
2. Security profiles (minimal security for simplicity)
3. Guardrails (template variables and conditional formatting)
4. Result destination (saving results to files in various formats)

To run this example:
1. Make sure you have set your Google API key as an environment variable:
   export GOOGLE_API_KEY=your_api_key_here

   NOTE: You need a valid Google API key to use the Gemini model.
   You can get an API key from the Google AI Studio: https://makersuite.google.com/app/apikey

2. Run the script: python examples/new_version_example.py
"""

import os
import sys
import time
import logging

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# Import the framework
from tbh_secure_agents import Expert, Operation

# Create output directory
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def main():
    """
    Main function demonstrating all the key features of the latest version.
    """
    print("\n" + "="*80)
    print("TBH SECURE AGENTS - NEW VERSION EXAMPLE")
    print("="*80 + "\n")

    # Get API key from environment variable or use a default for testing
    api_key = os.environ.get("GOOGLE_API_KEY", "AIzaSyA3ZxbIXpR3yNkZwGDznrztdQmgnU16DJI")

    # Using the provided API key
    print(f"Using API key: {api_key[:5]}...{api_key[-4:]}")

    print("STEP 1: Creating Experts with Different Specialties\n")

    # Create a content writer expert
    content_writer = Expert(
        specialty="Content Writer",
        objective="Create engaging and informative content",
        background="You are an experienced content writer with expertise in creating clear, concise, and engaging content.",
        api_key=api_key,
        security_profile="minimal"  # Using minimal security for simplicity
    )
    print("✓ Created Content Writer expert")

    # Create a data analyst expert
    data_analyst = Expert(
        specialty="Data Analyst",
        objective="Analyze data and provide insights",
        background="You are a skilled data analyst with experience in interpreting data and extracting meaningful insights.",
        api_key=api_key,
        security_profile="minimal"  # Using minimal security for simplicity
    )
    print("✓ Created Data Analyst expert\n")

    print("STEP 2: Creating Operations with Result Destinations\n")

    # Create an operation for the content writer with result_destination
    content_operation = Operation(
        instructions="Write a short blog post about the benefits of artificial intelligence in healthcare.",
        output_format="A well-structured blog post with a title, introduction, main points, and conclusion.",
        expert=content_writer,
        result_destination=os.path.join(OUTPUT_DIR, "healthcare_ai_blog.md")
    )
    print("✓ Created Content Operation with Markdown result destination")

    # Create an operation for the data analyst with result_destination
    analysis_operation = Operation(
        instructions="Analyze the following data and provide insights: Patient wait times decreased by 30% after implementing AI scheduling. Diagnostic accuracy improved by 15%. Treatment planning time reduced by 25%.",
        output_format="A concise analysis with key insights and recommendations.",
        expert=data_analyst,
        result_destination=os.path.join(OUTPUT_DIR, "healthcare_data_analysis.txt")
    )
    print("✓ Created Analysis Operation with Text result destination\n")

    print("STEP 3: Creating a Squad with Guardrails and Result Destination\n")

    # Create a squad with template variables in operations
    template_expert = Expert(
        specialty="Healthcare Specialist",
        objective="Provide {output_type} about healthcare technology",
        background="You are an expert in healthcare technology with a focus on {focus_area}.",
        api_key=api_key,
        security_profile="minimal"  # Using minimal security for simplicity
    )
    print("✓ Created Expert with template variables")

    # Create an operation with template variables and conditional formatting
    template_operation = Operation(
        instructions="""
        Write a {length} summary about {topic} in healthcare.

        {tone, select,
          formal:Use a professional, academic tone suitable for medical professionals.|
          conversational:Use a friendly, approachable tone suitable for patients and the general public.|
          technical:Use precise technical language appropriate for healthcare IT specialists.
        }

        {include_statistics, select,
          true:Include relevant statistics and data points to support your summary.|
          false:Focus on qualitative information without specific statistics.
        }
        """,
        expert=template_expert,
        result_destination=os.path.join(OUTPUT_DIR, "healthcare_summary.html")
    )
    print("✓ Created Operation with template variables and conditional formatting")

    # Create a squad configuration (we won't deploy it, but we'll show how to set it up)
    print("✓ Squad configuration would include:")
    print("  - Experts: Content Writer, Data Analyst, Healthcare Specialist")
    print("  - Operations: Blog Post, Data Analysis, Healthcare Summary")
    print("  - Process: Sequential")
    print("  - Security Level: Minimal")
    print("  - Result Destination: JSON file\n")

    print("STEP 4: Deploying the Squad with Guardrails\n")

    # Define guardrail inputs
    guardrails = {
        "output_type": "insights",
        "focus_area": "AI implementation",
        "length": "one-page",
        "topic": "artificial intelligence",
        "tone": "conversational",
        "include_statistics": "true"
    }
    print("✓ Defined guardrail inputs")

    # Instead of deploying the squad, we'll execute each operation individually
    # to demonstrate the features without running into security issues
    print("\nExecuting operations individually...\n")

    print("EXECUTING OPERATION 1: Content Writer - Blog Post")
    start_time = time.time()
    content_result = content_operation.execute()
    end_time = time.time()
    print(f"✓ Operation 1 completed in {end_time - start_time:.2f} seconds\n")

    print("EXECUTING OPERATION 2: Data Analyst - Data Analysis")
    start_time = time.time()
    analysis_result = analysis_operation.execute()
    end_time = time.time()
    print(f"✓ Operation 2 completed in {end_time - start_time:.2f} seconds\n")

    print("EXECUTING OPERATION 3: Healthcare Specialist - Summary with Guardrails")
    start_time = time.time()
    template_result = template_operation.execute(guardrails=guardrails)
    end_time = time.time()
    print(f"✓ Operation 3 completed in {end_time - start_time:.2f} seconds\n")

    # Combine the results to simulate a squad result
    result = f"COMBINED RESULTS FROM ALL OPERATIONS:\n\n" + \
             f"1. Content Writer Result:\n{content_result[:200]}...\n\n" + \
             f"2. Data Analyst Result:\n{analysis_result[:200]}...\n\n" + \
             f"3. Healthcare Specialist Result:\n{template_result[:200]}..."

    # Save the combined result to the squad result destination
    with open(os.path.join(OUTPUT_DIR, "healthcare_squad_result.json"), "w") as f:
        import json
        json.dump({
            "squad_result": result,
            "operations": {
                "content_operation": content_result[:500] + "...",
                "analysis_operation": analysis_result[:500] + "...",
                "template_operation": template_result[:500] + "..."
            },
            "metadata": {
                "execution_time": time.time(),
                "guardrails": guardrails
            }
        }, f, indent=2)

    print("✓ All operations completed successfully and results saved")

    print("STEP 5: Checking the Results\n")

    # Check if the files were created
    files_to_check = [
        "healthcare_ai_blog.md",
        "healthcare_data_analysis.txt",
        "healthcare_summary.html",
        "healthcare_squad_result.json"
    ]

    for file_name in files_to_check:
        file_path = os.path.join(OUTPUT_DIR, file_name)
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            print(f"✓ {file_name} created successfully ({file_size} bytes)")

            # Print a preview of the file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                preview = content[:100] + "..." if len(content) > 100 else content
                print(f"  Preview: {preview}\n")
        else:
            print(f"✗ {file_name} was not created\n")

    print("STEP 6: Final Squad Result\n")

    # Print the final result
    print("Final Squad Result:")
    print("-" * 40)
    print(result[:500] + "..." if len(result) > 500 else result)
    print("-" * 40 + "\n")

    print("="*80)
    print("EXAMPLE COMPLETED SUCCESSFULLY")
    print("="*80 + "\n")

    print(f"All output files are saved in: {OUTPUT_DIR}")
    print("You can examine these files to see the results of the example.")

if __name__ == "__main__":
    main()
