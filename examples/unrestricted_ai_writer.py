#!/usr/bin/env python3
"""
Unrestricted AI Writer Example

This example demonstrates how to use the unrestricted security profile
to allow any code to run without security checks.
"""

import os
from tbh_secure_agents import Expert, Operation
from tbh_secure_agents.security_validation import enable_hybrid_validation

# Set the API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyA3ZxbIXpR3yNkZwGDznrztdQmgnU16DJI"

# Create output directory
os.makedirs("output", exist_ok=True)

# Register a custom unrestricted security profile
from tbh_secure_agents.security_profiles import register_custom_profile

# Create an unrestricted security profile
unrestricted_profile = register_custom_profile(
    name="unrestricted",
    thresholds={
        "injection_score": 1.0,       # Never block injections
        "sensitive_data": 1.0,        # Never block sensitive data
        "relevance_score": 0.0,       # No relevance check
        "reliability_score": 0.0,     # No reliability check
        "consistency_score": 0.0,     # No consistency check
    },
    checks={
        "critical_exploits": False,   # Skip critical exploits check
        "system_commands": False,     # Skip system commands check
        "content_analysis": False,    # Skip content analysis
        "format_validation": False,   # Skip format validation
        "context_validation": False,  # Skip context validation
        "output_validation": False,   # Skip output validation
        "expert_validation": False,   # Skip expert validation
    },
    description="Unrestricted mode with no security checks. Use at your own risk."
)

# Enable hybrid validation with report generation
enable_hybrid_validation(enable_reports=True, auto_open_reports=False)

# Create a simple AI Writer with unrestricted security
writer = Expert(
    specialty="Creative Writing",
    objective="Write creative and engaging content",
    security_profile="unrestricted"  # Use unrestricted security
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
    result_destination="output/unrestricted_result.md"
)

# Execute the operation
try:
    result = writer.execute_task(operation.instructions)
    print("\nOperation Result:")
    print("-" * 50)
    print(result)
    print("-" * 50)
    
    # Save the result to a file
    with open("output/unrestricted_result.md", "w") as f:
        f.write(result)
    
    print(f"\nResult saved to: output/unrestricted_result.md")
except Exception as e:
    print(f"Error executing operation: {e}")
