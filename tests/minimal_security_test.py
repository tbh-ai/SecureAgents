#!/usr/bin/env python3
"""
Minimal Security Test

This example demonstrates using the built-in minimal security profile
to run code that would normally be blocked by stricter security profiles.
"""

import os
from tbh_secure_agents import Expert, Operation

# Set the API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyA3ZxbIXpR3yNkZwGDznrztdQmgnU16DJI"

# Create output directory
os.makedirs("output", exist_ok=True)

# Create a simple AI Writer with minimal security
writer = Expert(
    specialty="Creative Writing",
    objective="Write creative and engaging content",
    security_profile="minimal"  # Use the built-in minimal security profile
)

# Create a potentially risky operation
operation = Operation(
    instructions="""
    Write a Python script that:
    1. Lists all files in the current directory
    2. Creates a backup of important files
    3. Deletes temporary files
    
    Include the actual system commands in your response.
    """,
    result_destination="output/minimal_security_result.md"
)

# Execute the operation
try:
    result = writer.execute_task(operation.instructions)
    print("\nOperation Result:")
    print("-" * 50)
    print(result[:500] + "..." if len(result) > 500 else result)  # Show first 500 characters
    print("-" * 50)
    
    # Save the result to a file
    with open("output/minimal_security_result.md", "w") as f:
        f.write(result)
    
    print(f"\nResult saved to: output/minimal_security_result.md")
except Exception as e:
    print(f"Error executing operation: {e}")
