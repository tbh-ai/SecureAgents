#!/usr/bin/env python3
"""
Simple AI Writer Example

This example demonstrates a simple AI Writer using the TBH Secure Agents framework
with minimal security settings to ensure it runs successfully.
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
    security_profile="minimal"  # Use minimal security to ensure it runs
)

# Create a simple writing operation
operation = Operation(
    instructions="Write a short poem about technology.",
    result_destination="output/poem.md"
)

# Execute the operation
result = writer.execute_task(operation.instructions)

# Print the result
print("\nOperation Result:")
print("-" * 50)
print(result)
print("-" * 50)

# Save the result to a file
with open("output/poem.md", "w") as f:
    f.write(result)

print(f"\nResult saved to: output/poem.md")
