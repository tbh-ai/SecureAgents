#!/usr/bin/env python3
"""
Test script for the result_destination feature.

This script tests the result_destination parameter in both Operation and Squad classes
by creating simple operations and checking if the results are saved to the specified files.
"""

import os
import sys
import logging
from typing import Dict, Any, Optional

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

# Import the TBH Secure Agents framework
from tbh_secure_agents import Expert, Operation, Squad

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Get API key from environment variable or use a default one for testing
API_KEY = os.environ.get("GOOGLE_API_KEY", "AIzaSyDYGDWiED84ZAL71xbT3QDBfUnCTrIPvpc")

def test_operation_result_destination():
    """Test the result_destination parameter in the Operation class."""
    print("\n=== Testing Operation result_destination ===")
    
    # Create output directory if it doesn't exist
    output_dir = os.path.join(os.getcwd(), "output")
    os.makedirs(output_dir, exist_ok=True)
    print(f"Created output directory: {output_dir}")
    
    # Create a simple expert
    expert = Expert(
        specialty="Content Creator",
        objective="Create simple content for testing",
        background="Expert in creating test content",
        security_profile="minimal",  # Use minimal security for testing
        api_key=API_KEY
    )
    
    # Create an operation with result_destination
    operation = Operation(
        instructions="Write a short paragraph about artificial intelligence.",
        output_format="A clear and concise paragraph",
        expert=expert,
        result_destination=os.path.join(output_dir, "ai_paragraph.txt")
    )
    
    # Execute the operation
    print("Executing operation...")
    result = operation.execute()
    print(f"Operation executed successfully")
    
    # Check if the file was created
    file_path = os.path.join(output_dir, "ai_paragraph.txt")
    if os.path.exists(file_path):
        print(f"✅ File created successfully: {file_path}")
        # Print file size
        print(f"   File size: {os.path.getsize(file_path)} bytes")
        # Print first few lines of the file
        with open(file_path, 'r') as f:
            content = f.read(200)
            print(f"   Content preview: {content}...")
    else:
        print(f"❌ File was NOT created: {file_path}")
    
    return result

def test_squad_result_destination():
    """Test the result_destination parameter in the Squad class."""
    print("\n=== Testing Squad result_destination ===")
    
    # Create output directory if it doesn't exist
    output_dir = os.path.join(os.getcwd(), "output")
    os.makedirs(output_dir, exist_ok=True)
    print(f"Created output directory: {output_dir}")
    
    # Create a simple expert
    expert = Expert(
        specialty="Content Creator",
        objective="Create simple content for testing",
        background="Expert in creating test content",
        security_profile="minimal",  # Use minimal security for testing
        api_key=API_KEY
    )
    
    # Create an operation without result_destination
    operation = Operation(
        instructions="Write a short paragraph about machine learning.",
        output_format="A clear and concise paragraph",
        expert=expert
    )
    
    # Create a squad with result_destination
    squad = Squad(
        experts=[expert],
        operations=[operation],
        process="sequential",
        security_level="minimal",  # Use minimal security for testing
        result_destination={
            "format": "markdown",
            "file_path": os.path.join(output_dir, "squad_result.md")
        }
    )
    
    # Deploy the squad
    print("Deploying squad...")
    result = squad.deploy()
    print(f"Squad deployed successfully")
    
    # Check if the file was created
    file_path = os.path.join(output_dir, "squad_result.md")
    if os.path.exists(file_path):
        print(f"✅ File created successfully: {file_path}")
        # Print file size
        print(f"   File size: {os.path.getsize(file_path)} bytes")
        # Print first few lines of the file
        with open(file_path, 'r') as f:
            content = f.read(200)
            print(f"   Content preview: {content}...")
    else:
        print(f"❌ File was NOT created: {file_path}")
    
    return result

def test_multiple_formats():
    """Test multiple file formats for result_destination."""
    print("\n=== Testing Multiple Formats ===")
    
    # Create output directory if it doesn't exist
    output_dir = os.path.join(os.getcwd(), "output")
    os.makedirs(output_dir, exist_ok=True)
    print(f"Created output directory: {output_dir}")
    
    # Create a simple expert
    expert = Expert(
        specialty="Content Creator",
        objective="Create simple content for testing",
        background="Expert in creating test content",
        security_profile="minimal",  # Use minimal security for testing
        api_key=API_KEY
    )
    
    # Test different formats
    formats = ["txt", "md", "json", "html"]
    operations = []
    
    for fmt in formats:
        # Create an operation with result_destination
        operation = Operation(
            instructions=f"Create content about renewable energy in {fmt.upper()} format.",
            output_format=f"Content in {fmt.upper()} format",
            expert=expert,
            result_destination=os.path.join(output_dir, f"energy.{fmt}")
        )
        operations.append(operation)
    
    # Create a squad with all operations
    squad = Squad(
        experts=[expert],
        operations=operations,
        process="sequential",
        security_level="minimal"  # Use minimal security for testing
    )
    
    # Deploy the squad
    print("Deploying squad...")
    result = squad.deploy()
    print(f"Squad deployed successfully")
    
    # Check if the files were created
    for fmt in formats:
        file_path = os.path.join(output_dir, f"energy.{fmt}")
        if os.path.exists(file_path):
            print(f"✅ {fmt.upper()} file created successfully: {file_path}")
            # Print file size
            print(f"   File size: {os.path.getsize(file_path)} bytes")
        else:
            print(f"❌ {fmt.upper()} file was NOT created: {file_path}")
    
    return result

def main():
    """Run all tests."""
    print("Starting result_destination tests...")
    
    try:
        # Test Operation result_destination
        test_operation_result_destination()
        
        # Test Squad result_destination
        test_squad_result_destination()
        
        # Test multiple formats
        test_multiple_formats()
        
        print("\nAll tests completed!")
    except Exception as e:
        print(f"Error during testing: {e}")

if __name__ == "__main__":
    main()
