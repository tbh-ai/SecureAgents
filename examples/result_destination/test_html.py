#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test script for HTML file creation in the TBH Secure Agents framework.
"""

import os
import sys
import logging

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# Import the framework
from tbh_secure_agents import Expert, Operation

# Create output directory
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def test_html_file():
    """Test creating an HTML file."""
    print("Testing HTML file creation...")

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Created output directory: {OUTPUT_DIR}")

    # Create a file path for the result
    file_path = os.path.abspath(os.path.join(OUTPUT_DIR, "test.html"))
    print(f"File path: {file_path}")

    # Create an expert
    expert = Expert(
        specialty="Content Creator",
        objective="Create high-quality content",
        api_key="test_key"
    )

    # Create an operation with result_destination
    operation = Operation(
        instructions="Write a short paragraph about artificial intelligence.",
        expert=expert,
        result_destination=file_path
    )

    # Execute the operation
    print("Executing operation...")
    result = operation.execute()
    print("Operation executed successfully")

    # Verify the file was created
    if os.path.exists(file_path):
        file_size = os.path.getsize(file_path)
        print(f"✅ File created successfully: {file_path}")
        print(f"   File size: {file_size} bytes")

        # Print the file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            print(f"File content:\n{content}")
    else:
        print(f"❌ Failed to create file: {file_path}")

if __name__ == "__main__":
    test_html_file()
