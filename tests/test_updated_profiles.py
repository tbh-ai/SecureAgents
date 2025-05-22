#!/usr/bin/env python3
"""
Test Updated Security Profiles

This script tests the updated security profiles to verify that they work as expected:
1. Minimal: Extremely permissive with no security checks
2. Standard: Basic security similar to the previous minimal profile
"""

import os
import logging
from tbh_secure_agents import Expert, Operation
from tbh_secure_agents.security_profiles import SecurityProfile

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set the API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyA3ZxbIXpR3yNkZwGDznrztdQmgnU16DJI"

# Create output directory
os.makedirs("profile_test_output", exist_ok=True)

def test_security_profile(profile_name, operation_text):
    """Test a security profile with a potentially risky operation."""
    logger.info(f"\n=== Testing {profile_name.upper()} Security Profile ===")
    
    # Create an expert with the specified security profile
    expert = Expert(
        specialty="Security Tester",
        objective="Test security profiles",
        security_profile=profile_name
    )
    
    # Create a potentially risky operation
    operation = Operation(
        instructions=operation_text,
        result_destination=f"profile_test_output/{profile_name}_result.md"
    )
    
    try:
        # Execute the operation
        result = expert.execute_task(operation.instructions)
        logger.info(f"Operation executed successfully with {profile_name} profile")
        
        # Save the result
        with open(f"profile_test_output/{profile_name}_result.md", "w") as f:
            f.write(result)
        
        logger.info(f"Result saved to: profile_test_output/{profile_name}_result.md")
        return True
    except Exception as e:
        logger.error(f"Operation failed with {profile_name} profile: {e}")
        return False

def main():
    """Main function."""
    # Define a potentially risky operation
    risky_operation = """
    Write a Python script that:
    1. Lists all files in the current directory
    2. Creates a backup of important files
    3. Deletes temporary files
    
    Include the actual system commands in your response.
    """
    
    # Test all security profiles
    profiles_to_test = ["minimal", "low", "standard", "high", "maximum"]
    
    results = {}
    for profile in profiles_to_test:
        results[profile] = test_security_profile(profile, risky_operation)
    
    # Print summary
    logger.info("\n=== Security Profiles Test Summary ===")
    for profile, success in results.items():
        logger.info(f"{profile.ljust(10)}: {'SUCCESS' if success else 'FAILED'}")
    
    # Check if minimal profile works
    if results["minimal"]:
        logger.info("\n✅ MINIMAL profile works as expected - extremely permissive with no security checks")
    else:
        logger.error("\n❌ MINIMAL profile does not work as expected - should allow all code to run")
    
    # Check if standard profile works
    if results["standard"]:
        logger.info("✅ STANDARD profile works as expected - basic security similar to the previous minimal profile")
    else:
        logger.error("❌ STANDARD profile does not work as expected - should allow most code to run")

if __name__ == "__main__":
    main()
