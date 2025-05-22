"""
Test script for security profiles and error messages in the tbh_secure_agents framework.
This script tests various security validation scenarios to verify the new error messages and suggestions.
"""

import sys
import os
from tbh_secure_agents.agent import Expert
from tbh_secure_agents.task import Operation
from tbh_secure_agents.crew import Squad

def test_empty_squad():
    """Test squad with no experts or operations."""
    print("\n=== Testing Empty Squad ===")
    try:
        # This should fail with a helpful error message
        squad = Squad(experts=[], operations=[], security_profile="standard")
        squad.deploy()
    except Exception as e:
        print(f"Expected error: {e}")
        return
    
    print("Test failed: Expected error for empty experts list")

def test_invalid_process():
    """Test squad with invalid process type."""
    print("\n=== Testing Invalid Process ===")
    
    # Create a simple expert and operation
    expert = Expert(
        specialty="Testing",
        objective="To test the security profiles",
        api_key="dummy_key"
    )
    
    operation = Operation(
        instructions="Test operation",
        expert=expert
    )
    
    # Create a squad with invalid process type
    squad = Squad(
        experts=[expert],
        operations=[operation],
        process="invalid_process",  # Invalid process type
        security_profile="standard"
    )
    
    # This should fail with a helpful error message about invalid process
    result = squad.deploy()
    print(f"Result: {result}")

def test_excessive_instructions():
    """Test squad with excessively long operation instructions."""
    print("\n=== Testing Excessive Instructions ===")
    
    # Create a simple expert
    expert = Expert(
        specialty="Testing",
        objective="To test the security profiles",
        api_key="dummy_key"
    )
    
    # Create an operation with very long instructions
    long_instructions = "Test operation " * 1000  # Very long instructions
    operation = Operation(
        instructions=long_instructions,
        expert=expert
    )
    
    # Create a squad with high security profile (stricter limits)
    squad = Squad(
        experts=[expert],
        operations=[operation],
        security_profile="high"  # High security profile has stricter limits
    )
    
    # This should fail with a helpful error message about excessive instructions
    result = squad.deploy()
    print(f"Result: {result}")

def test_dangerous_operation():
    """Test squad with potentially dangerous operation instructions."""
    print("\n=== Testing Dangerous Operation ===")
    
    # Create a simple expert
    expert = Expert(
        specialty="Testing",
        objective="To test the security profiles",
        api_key="dummy_key"
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
        security_profile="standard"
    )
    
    # This should fail with a helpful error message about dangerous operation
    result = squad.deploy()
    print(f"Result: {result}")

def test_minimal_security_profile():
    """Test squad with minimal security profile."""
    print("\n=== Testing Minimal Security Profile ===")
    
    # Create a simple expert
    expert = Expert(
        specialty="Testing",
        objective="To test the security profiles",
        api_key="dummy_key"
    )
    
    # Create an operation with potentially dangerous instructions
    # This should pass with minimal security profile
    dangerous_instructions = "Delete all files in the system directory using rm -rf /"
    operation = Operation(
        instructions=dangerous_instructions,
        expert=expert
    )
    
    # Create a squad with minimal security profile
    squad = Squad(
        experts=[expert],
        operations=[operation],
        security_profile="minimal"  # Minimal security profile has fewer checks
    )
    
    # This should pass with minimal security profile
    result = squad.deploy()
    print(f"Result: {result or 'No output'}")

if __name__ == "__main__":
    # Run the tests
    test_empty_squad()
    test_invalid_process()
    test_excessive_instructions()
    test_dangerous_operation()
    test_minimal_security_profile()
