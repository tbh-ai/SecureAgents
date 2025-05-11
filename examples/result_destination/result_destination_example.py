#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Example script demonstrating the result_destination parameter in the TBH Secure Agents framework.
This script shows how to save results to files in various formats.
"""

import os
import sys
import logging
from pathlib import Path

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# Import the framework
from tbh_secure_agents import Expert, Operation, Squad

# Create output directory
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def main():
    """
    Main function demonstrating the result_destination parameter.
    """
    print("TBH Secure Agents - Result Destination Example")
    print("=============================================")
    
    # Create an expert
    content_expert = Expert(
        specialty="Content Creator",
        objective="Create high-quality content",
        api_key="your_api_key_here"  # Replace with your actual API key
    )
    
    # Create operations with different result_destination formats
    operations = [
        Operation(
            instructions="Write a short paragraph about artificial intelligence.",
            expert=content_expert,
            result_destination=os.path.join(OUTPUT_DIR, "ai_paragraph.txt")
        ),
        Operation(
            instructions="Write a short paragraph about machine learning in markdown format.",
            expert=content_expert,
            result_destination=os.path.join(OUTPUT_DIR, "ml_paragraph.md")
        ),
        Operation(
            instructions="Write a short paragraph about data science in HTML format.",
            expert=content_expert,
            result_destination=os.path.join(OUTPUT_DIR, "data_science.html")
        ),
        Operation(
            instructions="Write a short paragraph about neural networks in JSON format.",
            expert=content_expert,
            result_destination=os.path.join(OUTPUT_DIR, "neural_networks.json")
        )
    ]
    
    # Create a squad with result_destination
    squad = Squad(
        experts=[content_expert],
        operations=operations,
        process="sequential",
        security_level="minimal",  # Use minimal security for this example
        result_destination={
            "format": "md",
            "file_path": os.path.join(OUTPUT_DIR, "squad_result.md")
        }
    )
    
    # Deploy the squad
    print("\nDeploying squad...")
    result = squad.deploy()
    print("Squad deployed successfully")
    
    # Print the result
    print("\nSquad Result:")
    print(result)
    
    # List the created files
    print("\nCreated Files:")
    for file_path in os.listdir(OUTPUT_DIR):
        full_path = os.path.join(OUTPUT_DIR, file_path)
        if os.path.isfile(full_path):
            file_size = os.path.getsize(full_path)
            print(f"- {file_path} ({file_size} bytes)")

if __name__ == "__main__":
    main()
