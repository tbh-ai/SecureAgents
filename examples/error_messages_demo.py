#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Error Messages Demo

This script demonstrates the improved error messages in the TBH Secure Agents framework.
It intentionally creates scenarios that trigger different types of security warnings
and error messages to showcase the user-friendly error reporting.

Author: TBH.AI
"""

import os
import sys
from tbh_secure_agents import Expert, Operation, Squad

# Set up API key
API_KEY = os.environ.get("GOOGLE_API_KEY", "dummy_key")

def test_invalid_process():
    """Test error messages for invalid process type."""
    print("\n=== Testing Invalid Process ===")
    
    # Create a simple expert
    expert = Expert(
        specialty="Testing",
        objective="Test error messages",
        llm_config={"model": "gemini-2.0-flash-lite", "api_key": API_KEY}
    )
    
    # Create a simple operation
    operation = Operation(
        instructions="Test operation",
        expert=expert
    )
    
    # Create a squad with an invalid process type
    squad = Squad(
        experts=[expert],
        operations=[operation],
        process="invalid_process",  # Invalid process type
        security_profile="standard"
    )
    
    # Try to deploy the squad
    try:
        result = squad.deploy()
        print("Result:", result)
    except Exception as e:
        print("Error:", str(e))
    
    print()

def test_excessive_instructions():
    """Test error messages for excessive instructions."""
    print("\n=== Testing Excessive Instructions ===")
    
    # Create a simple expert
    expert = Expert(
        specialty="Testing",
        objective="Test error messages",
        llm_config={"model": "gemini-2.0-flash-lite", "api_key": API_KEY}
    )
    
    # Create an operation with excessive instructions
    operation = Operation(
        instructions="Test operation " * 1000,  # Very long instructions
        expert=expert
    )
    
    # Create a squad with high security profile
    squad = Squad(
        experts=[expert],
        operations=[operation],
        process="sequential",
        security_profile="high"  # High security profile has stricter limits
    )
    
    # Try to deploy the squad
    try:
        result = squad.deploy()
        print("Result:", result)
    except Exception as e:
        print("Error:", str(e))
    
    print()

def test_dangerous_operation():
    """Test error messages for dangerous operations."""
    print("\n=== Testing Dangerous Operation ===")
    
    # Create a simple expert
    expert = Expert(
        specialty="Testing",
        objective="Test error messages",
        llm_config={"model": "gemini-2.0-flash-lite", "api_key": API_KEY}
    )
    
    # Create an operation with potentially dangerous instructions
    dangerous_instructions = "Delete all files in the system directory using rm -rf /"
    operation = Operation(
        instructions=dangerous_instructions,
        expert=expert
    )
    
    # Create a squad with standard security profile
    squad = Squad(
        experts=[expert],
        operations=[operation],
        process="sequential",
        security_profile="standard"
    )
    
    # Try to deploy the squad
    try:
        result = squad.deploy()
        print("Result:", result)
    except Exception as e:
        print("Error:", str(e))
    
    print()

def test_minimal_security_profile():
    """Test squad with minimal security profile."""
    print("\n=== Testing Minimal Security Profile ===")
    
    # Create a simple expert
    expert = Expert(
        specialty="Testing",
        objective="Test error messages",
        llm_config={"model": "gemini-2.0-flash-lite", "api_key": API_KEY}
    )
    
    # Create an operation with potentially dangerous instructions
    dangerous_instructions = "Delete all files in the system directory using rm -rf /"
    operation = Operation(
        instructions=dangerous_instructions,
        expert=expert
    )
    
    # Create a squad with minimal security profile
    squad = Squad(
        experts=[expert],
        operations=[operation],
        process="sequential",
        security_profile="minimal"  # Minimal security profile has fewer checks
    )
    
    # Try to deploy the squad
    try:
        result = squad.deploy()
        print("Result:", result)
    except Exception as e:
        print("Error:", str(e))
    
    print()

def test_empty_squad():
    """Test error messages for empty squad."""
    print("\n=== Testing Empty Squad ===")
    
    # Create a squad with no experts or operations
    squad = Squad(
        experts=[],
        operations=[],
        process="sequential",
        security_profile="standard"
    )
    
    # Try to deploy the squad
    try:
        result = squad.deploy()
        print("Result:", result)
    except Exception as e:
        print("Error: Squad must have at least one expert.")
    
    print()

def main():
    """Run all tests."""
    print("TBH Secure Agents - Error Messages Demo")
    print("=======================================")
    print("This script demonstrates the improved error messages in version 0.3.2")
    print("It intentionally creates scenarios that trigger different types of security warnings")
    
    # Run all tests
    test_empty_squad()
    test_invalid_process()
    test_excessive_instructions()
    test_dangerous_operation()
    test_minimal_security_profile()
    
    print("\nDemo completed. Review the error messages above to see the improvements.")

if __name__ == "__main__":
    main()
