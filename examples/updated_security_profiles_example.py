#!/usr/bin/env python3
"""
Example Using Updated Security Profiles

This example demonstrates how to use the updated security profiles:
- unrestricted: No security checks at all
- minimal: Only critical exploit checks
- standard: Similar to the old minimal profile
"""

import os
import sys
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import the TBH Secure Agents framework
from tbh_secure_agents import Expert, Operation, Squad
from tbh_secure_agents.security_profiles import list_custom_profiles

# Create output directory
os.makedirs("output", exist_ok=True)

def run_with_profile(profile_name, operation_text):
    """Run an operation with the specified security profile."""
    logger.info(f"\n=== Running with {profile_name.upper()} security profile ===")

    # Create an expert with the specified security profile
    expert = Expert(
        specialty="AI Assistant",
        objective="Execute the given task",
        security_profile=profile_name
    )

    # Create an operation
    operation = Operation(
        instructions=operation_text,
        result_destination=f"output/{profile_name}_result.md"
    )

    try:
        # Execute the operation
        result = expert.execute_task(operation.instructions)
        logger.info(f"Operation executed successfully with {profile_name} profile")

        # Save the result
        with open(f"output/{profile_name}_result.md", "w") as f:
            f.write(result)

        logger.info(f"Result saved to: output/{profile_name}_result.md")
        return True
    except Exception as e:
        logger.error(f"Operation failed with {profile_name} profile: {e}")
        return False

def main():
    """Main function."""
    # List available custom profiles
    logger.info(f"Available custom profiles: {list_custom_profiles()}")

    # Define a potentially risky operation
    operation_text = """
    Write a Python script that:
    1. Lists all files in the current directory
    2. Creates a backup of important files
    3. Deletes temporary files

    Include the actual system commands in your response.
    """

    # Run with different security profiles
    run_with_profile("unrestricted", operation_text)
    run_with_profile("minimal_override", operation_text)
    run_with_profile("standard_override", operation_text)
    run_with_profile("standard", operation_text)  # For comparison

    logger.info("\nExample completed. Check the output directory for results.")

if __name__ == "__main__":
    main()