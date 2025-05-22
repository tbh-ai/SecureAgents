#!/usr/bin/env python3
"""
Update All Security Profiles

This script updates all security profiles in the TBH Secure Agents framework:
1. Minimal: Extremely permissive (almost no restrictions)
2. Low: Basic security (between minimal and standard)
3. Standard: Similar to the previous minimal profile
4. High: Strict but usable
5. Maximum: Very strict for sensitive applications

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

def create_minimal_override():
    """
    Create a custom profile to override the minimal security profile.
    This profile is extremely permissive with almost no restrictions.
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
            "critical_exploits": False,   # Skip critical exploits check
            "system_commands": False,     # Skip system commands check
            "content_analysis": False,    # Skip content analysis
            "format_validation": False,   # Skip format validation
            "context_validation": False,  # Skip context validation
            "output_validation": False,   # Skip output validation
            "expert_validation": False,   # Skip expert validation
        },
        description="Extremely permissive with almost no restrictions. All code will run."
    )

def create_low_override():
    """
    Create a custom profile to override the low security profile.
    This profile has basic security (between minimal and standard).
    """
    return register_custom_profile(
        name="low_override",
        thresholds={
            "injection_score": 0.9,       # Only block very obvious injections
            "sensitive_data": 0.9,        # Only block very obvious sensitive data
            "relevance_score": 0.1,       # Very permissive relevance check
            "reliability_score": 0.1,     # Very permissive reliability check
            "consistency_score": 0.1,     # Very permissive consistency check
        },
        checks={
            "critical_exploits": True,    # Check for critical exploits
            "system_commands": True,      # Check for system commands
            "content_analysis": False,    # Skip content analysis
            "format_validation": False,   # Skip format validation
            "context_validation": False,  # Skip context validation
            "output_validation": False,   # Skip output validation
            "expert_validation": False,   # Skip expert validation
        },
        description="Basic security with minimal restrictions. Most code will run."
    )

def create_standard_override():
    """
    Create a custom profile to override the standard security profile.
    This profile is similar to the previous minimal profile.
    """
    # Get the current minimal profile thresholds and checks
    minimal_thresholds = get_security_thresholds(SecurityProfile.MINIMAL)
    minimal_checks = get_security_checks(SecurityProfile.MINIMAL)
    
    return register_custom_profile(
        name="standard_override",
        thresholds=minimal_thresholds,
        checks=minimal_checks,
        description="Standard security similar to the previous minimal profile. Most code will run with basic checks."
    )

def create_high_override():
    """
    Create a custom profile to override the high security profile.
    This profile is strict but usable.
    """
    return register_custom_profile(
        name="high_override",
        thresholds={
            "injection_score": 0.7,       # Block obvious injections
            "sensitive_data": 0.7,        # Block obvious sensitive data
            "relevance_score": 0.3,       # Permissive relevance check
            "reliability_score": 0.3,     # Permissive reliability check
            "consistency_score": 0.3,     # Permissive consistency check
        },
        checks={
            "critical_exploits": True,    # Check for critical exploits
            "system_commands": True,      # Check for system commands
            "content_analysis": True,     # Perform content analysis
            "format_validation": True,    # Perform format validation
            "context_validation": False,  # Skip context validation
            "output_validation": True,    # Perform output validation
            "expert_validation": True,    # Perform expert validation
        },
        description="Strict but usable security profile. Most legitimate code will run."
    )

def create_maximum_override():
    """
    Create a custom profile to override the maximum security profile.
    This profile is very strict for sensitive applications.
    """
    return register_custom_profile(
        name="maximum_override",
        thresholds={
            "injection_score": 0.5,       # Block many injections
            "sensitive_data": 0.5,        # Block many sensitive data
            "relevance_score": 0.5,       # Moderate relevance check
            "reliability_score": 0.5,     # Moderate reliability check
            "consistency_score": 0.5,     # Moderate consistency check
        },
        checks={
            "critical_exploits": True,    # Check for critical exploits
            "system_commands": True,      # Check for system commands
            "content_analysis": True,     # Perform content analysis
            "format_validation": True,    # Perform format validation
            "context_validation": True,   # Perform context validation
            "output_validation": True,    # Perform output validation
            "expert_validation": True,    # Perform expert validation
        },
        description="Very strict security profile for sensitive applications. Only safe code will run."
    )

def create_example_script():
    """Create an example script that demonstrates the updated security profiles."""
    example_path = "security_profiles_demo.py"
    
    example_content = """#!/usr/bin/env python3
\"\"\"
Security Profiles Demo

This script demonstrates the updated security profiles in the TBH Secure Agents framework:
1. Minimal: Extremely permissive (almost no restrictions)
2. Low: Basic security (between minimal and standard)
3. Standard: Similar to the previous minimal profile
4. High: Strict but usable
5. Maximum: Very strict for sensitive applications

Each profile is tested with the same potentially risky operation.
\"\"\"

import os
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import the TBH Secure Agents framework
from tbh_secure_agents import Expert, Operation
from tbh_secure_agents.security_profiles import list_custom_profiles

# Set the API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyA3ZxbIXpR3yNkZwGDznrztdQmgnU16DJI"

# Create output directory
os.makedirs("security_profiles_output", exist_ok=True)

def test_security_profile(profile_name):
    \"\"\"Test a security profile with a potentially risky operation.\"\"\"
    logger.info(f"\\n=== Testing {profile_name.upper()} Security Profile ===")
    
    # Create an expert with the specified security profile
    expert = Expert(
        specialty="Security Tester",
        objective="Test security profiles",
        security_profile=profile_name
    )
    
    # Create a potentially risky operation
    operation = Operation(
        instructions=\"\"\"
        Write a Python script that:
        1. Lists all files in the current directory
        2. Creates a backup of important files
        3. Deletes temporary files
        
        Include the actual system commands in your response.
        \"\"\",
        result_destination=f"security_profiles_output/{profile_name}_result.md"
    )
    
    try:
        # Execute the operation
        result = expert.execute_task(operation.instructions)
        logger.info(f"Operation executed successfully with {profile_name} profile")
        
        # Save the result
        with open(f"security_profiles_output/{profile_name}_result.md", "w") as f:
            f.write(result)
        
        logger.info(f"Result saved to: security_profiles_output/{profile_name}_result.md")
        return True
    except Exception as e:
        logger.error(f"Operation failed with {profile_name} profile: {e}")
        return False

def main():
    \"\"\"Main function.\"\"\"
    # List available custom profiles
    logger.info(f"Available custom profiles: {list_custom_profiles()}")
    
    # Test all security profiles
    profiles_to_test = [
        "minimal_override",  # Custom minimal profile
        "low_override",      # Custom low profile
        "standard_override", # Custom standard profile
        "high_override",     # Custom high profile
        "maximum_override",  # Custom maximum profile
        "minimal",           # Built-in minimal profile (for comparison)
        "standard"           # Built-in standard profile (for comparison)
    ]
    
    results = {}
    for profile in profiles_to_test:
        results[profile] = test_security_profile(profile)
    
    # Print summary
    logger.info("\\n=== Security Profiles Test Summary ===")
    for profile, success in results.items():
        logger.info(f"{profile.ljust(20)}: {'SUCCESS' if success else 'FAILED'}")

if __name__ == "__main__":
    main()
\"\"\"
    
    # Write the example script
    with open(example_path, "w") as f:
        f.write(example_content)
    
    logger.info(f"Created example script: {example_path}")

def main():
    """Main function."""
    logger.info("Updating all security profiles...")
    
    # Create custom profiles to override the built-in profiles
    if create_minimal_override():
        logger.info("Created 'minimal_override' profile")
    else:
        logger.error("Failed to create 'minimal_override' profile")
    
    if create_low_override():
        logger.info("Created 'low_override' profile")
    else:
        logger.error("Failed to create 'low_override' profile")
    
    if create_standard_override():
        logger.info("Created 'standard_override' profile")
    else:
        logger.error("Failed to create 'standard_override' profile")
    
    if create_high_override():
        logger.info("Created 'high_override' profile")
    else:
        logger.error("Failed to create 'high_override' profile")
    
    if create_maximum_override():
        logger.info("Created 'maximum_override' profile")
    else:
        logger.error("Failed to create 'maximum_override' profile")
    
    # List all custom profiles
    logger.info(f"Available custom profiles: {list_custom_profiles()}")
    
    # Create an example script
    create_example_script()
    
    # Clear caches
    clear_caches()
    
    logger.info("All security profiles updated successfully")
    logger.info("\nTo use the updated profiles:")
    logger.info("1. Use 'minimal_override' for extremely permissive security (almost no restrictions)")
    logger.info("2. Use 'low_override' for basic security (between minimal and standard)")
    logger.info("3. Use 'standard_override' for security similar to the previous minimal profile")
    logger.info("4. Use 'high_override' for strict but usable security")
    logger.info("5. Use 'maximum_override' for very strict security for sensitive applications")
    logger.info("\nExample: expert = Expert(security_profile='minimal_override')")
    logger.info("\nRun the security_profiles_demo.py script to test all profiles")

if __name__ == "__main__":
    main()
