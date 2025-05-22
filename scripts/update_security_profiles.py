#!/usr/bin/env python3
"""
Update Security Profiles

This script updates the security profiles in the TBH Secure Agents framework:
1. Creates a new "unrestricted" profile that's even more permissive than "minimal"
2. Updates the "minimal" profile to allow any code to run with minimal warnings
3. Updates the "standard" profile to be similar to the current "minimal" profile

Run this script once to update the security profiles for the framework.
"""

import os
import sys
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import the security profiles module
from tbh_secure_agents.security_profiles import (
    register_custom_profile,
    SecurityProfile,
    get_security_thresholds,
    get_security_checks,
    list_custom_profiles,
    get_custom_profile,
    clear_caches
)

def create_unrestricted_profile():
    """Create a new 'unrestricted' profile that's even more permissive than 'minimal'."""
    return register_custom_profile(
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

def update_minimal_profile():
    """
    Update the 'minimal' profile to allow any code to run with minimal warnings.
    
    Since we can't directly modify the built-in profiles, we'll create a custom
    profile called 'minimal_override' that will be used instead of the built-in
    'minimal' profile.
    """
    return register_custom_profile(
        name="minimal_override",
        thresholds={
            "injection_score": 1.0,       # Never block injections
            "sensitive_data": 1.0,        # Never block sensitive data
            "relevance_score": 0.0,       # No relevance check
            "reliability_score": 0.0,     # No reliability check
            "consistency_score": 0.0,     # No consistency check
        },
        checks={
            "critical_exploits": True,    # Only check for critical exploits
            "system_commands": False,     # Skip system commands check
            "content_analysis": False,    # Skip content analysis
            "format_validation": False,   # Skip format validation
            "context_validation": False,  # Skip context validation
            "output_validation": False,   # Skip output validation
            "expert_validation": False,   # Skip expert validation
        },
        description="Minimal security with only critical exploit checks. Almost all code will run."
    )

def update_standard_profile():
    """
    Update the 'standard' profile to be similar to the current 'minimal' profile.
    
    Since we can't directly modify the built-in profiles, we'll create a custom
    profile called 'standard_override' that will be used instead of the built-in
    'standard' profile.
    """
    # Get the current minimal profile thresholds and checks
    minimal_thresholds = get_security_thresholds(SecurityProfile.MINIMAL)
    minimal_checks = get_security_checks(SecurityProfile.MINIMAL)
    
    return register_custom_profile(
        name="standard_override",
        thresholds=minimal_thresholds,
        checks=minimal_checks,
        description="Standard security with minimal restrictions. Most code will run."
    )

def create_example_with_updated_profiles():
    """Create an example script that uses the updated security profiles."""
    example_path = "examples/updated_security_profiles_example.py"
    
    example_content = """#!/usr/bin/env python3
\"\"\"
Example Using Updated Security Profiles

This example demonstrates how to use the updated security profiles:
- unrestricted: No security checks at all
- minimal: Only critical exploit checks
- standard: Similar to the old minimal profile
\"\"\"

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
    \"\"\"Run an operation with the specified security profile.\"\"\"
    logger.info(f"\\n=== Running with {profile_name.upper()} security profile ===")
    
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
    \"\"\"Main function.\"\"\"
    # List available custom profiles
    logger.info(f"Available custom profiles: {list_custom_profiles()}")
    
    # Define a potentially risky operation
    operation_text = \"\"\"
    Write a Python script that:
    1. Lists all files in the current directory
    2. Creates a backup of important files
    3. Deletes temporary files
    
    Include the actual system commands in your response.
    \"\"\"
    
    # Run with different security profiles
    run_with_profile("unrestricted", operation_text)
    run_with_profile("minimal_override", operation_text)
    run_with_profile("standard_override", operation_text)
    run_with_profile("standard", operation_text)  # For comparison
    
    logger.info("\\nExample completed. Check the output directory for results.")

if __name__ == "__main__":
    main()
\"\"\"
    """
    
    # Create the examples directory if it doesn't exist
    os.makedirs(os.path.dirname(example_path), exist_ok=True)
    
    # Write the example script
    with open(example_path, "w") as f:
        f.write(example_content)
    
    logger.info(f"Created example script: {example_path}")

def main():
    """Main function."""
    logger.info("Updating security profiles...")
    
    # Create the unrestricted profile
    if create_unrestricted_profile():
        logger.info("Created 'unrestricted' profile")
    else:
        logger.error("Failed to create 'unrestricted' profile")
    
    # Update the minimal profile
    if update_minimal_profile():
        logger.info("Created 'minimal_override' profile to replace 'minimal'")
    else:
        logger.error("Failed to create 'minimal_override' profile")
    
    # Update the standard profile
    if update_standard_profile():
        logger.info("Created 'standard_override' profile to replace 'standard'")
    else:
        logger.error("Failed to create 'standard_override' profile")
    
    # List all custom profiles
    logger.info(f"Available custom profiles: {list_custom_profiles()}")
    
    # Create an example script
    create_example_with_updated_profiles()
    
    # Clear caches
    clear_caches()
    
    logger.info("Security profiles updated successfully")
    logger.info("\nTo use the updated profiles:")
    logger.info("1. Use 'unrestricted' for no security checks at all")
    logger.info("2. Use 'minimal_override' instead of 'minimal' for minimal security")
    logger.info("3. Use 'standard_override' instead of 'standard' for the old minimal level")
    logger.info("\nExample: expert = Expert(security_profile='unrestricted')")

if __name__ == "__main__":
    main()
