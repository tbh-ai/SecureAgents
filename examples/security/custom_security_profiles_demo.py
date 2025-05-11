#!/usr/bin/env python3
"""
Custom Security Profiles Demo

This example demonstrates how to create and use custom security profiles in the TBH Secure Agents framework.
It shows how to register custom profiles, use them with experts and squads, and manage them.
"""

import os
import sys
import logging

# Configure logging to show security messages
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

# Import the TBH Secure Agents framework
from tbh_secure_agents import Expert, Operation, Squad
from tbh_secure_agents.security_profiles import (
    register_custom_profile, list_custom_profiles, get_custom_profile, clear_caches
)

# Get API key from environment variable or use a default one for testing
API_KEY = os.environ.get("GOOGLE_API_KEY", "AIzaSyDYGDWiED84ZAL71xbT3QDBfUnCTrIPvpc")

def register_industry_profiles():
    """Register custom security profiles for different industries."""
    
    # Register a healthcare security profile
    healthcare_profile = register_custom_profile(
        name="healthcare",
        thresholds={
            "injection_score": 0.3,       # Strict injection detection
            "sensitive_data": 0.2,        # Very strict sensitive data detection
            "relevance_score": 0.7,       # Strict relevance check
            "reliability_score": 0.8,     # Very strict reliability check
            "consistency_score": 0.8,     # Very strict consistency check
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
        description="Custom security profile for healthcare applications with strict PII protection"
    )
    
    # Register a finance security profile
    finance_profile = register_custom_profile(
        name="finance",
        thresholds={
            "injection_score": 0.2,       # Very strict injection detection
            "sensitive_data": 0.2,        # Very strict sensitive data detection
            "relevance_score": 0.8,       # Very strict relevance check
            "reliability_score": 0.9,     # Most strict reliability check
            "consistency_score": 0.9,     # Most strict consistency check
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
        description="Custom security profile for financial applications with strict data protection"
    )
    
    # Register an education security profile
    education_profile = register_custom_profile(
        name="education",
        thresholds={
            "injection_score": 0.5,       # Moderate injection detection
            "sensitive_data": 0.4,        # Moderate sensitive data detection
            "relevance_score": 0.6,       # Moderate relevance check
            "reliability_score": 0.7,     # Strict reliability check
            "consistency_score": 0.7,     # Strict consistency check
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
        description="Custom security profile for educational applications with balanced security"
    )
    
    # Register a creative security profile
    creative_profile = register_custom_profile(
        name="creative",
        thresholds={
            "injection_score": 0.7,       # Permissive injection detection
            "sensitive_data": 0.6,        # Permissive sensitive data detection
            "relevance_score": 0.3,       # Permissive relevance check
            "reliability_score": 0.4,     # Permissive reliability check
            "consistency_score": 0.4,     # Permissive consistency check
        },
        checks={
            "critical_exploits": True,    # Check for critical exploits
            "system_commands": True,      # Check for system commands
            "content_analysis": False,    # Skip content analysis
            "format_validation": True,    # Perform format validation
            "context_validation": False,  # Skip context validation
            "output_validation": False,   # Skip output validation
            "expert_validation": True,    # Perform expert validation
        },
        description="Custom security profile for creative applications with minimal restrictions"
    )
    
    return [healthcare_profile, finance_profile, education_profile, creative_profile]

def create_expert_with_profile(profile_name):
    """Create an expert with the specified custom security profile."""
    return Expert(
        specialty=f"{profile_name.capitalize()} Expert",
        objective=f"Demonstrate {profile_name} security profile",
        background=f"Expert with {profile_name} security profile",
        security_profile=profile_name,
        api_key=API_KEY
    )

def create_operation_for_profile(profile_name):
    """Create an operation appropriate for the security profile."""
    if profile_name == "healthcare":
        return Operation(
            instructions="Explain HIPAA compliance requirements for healthcare applications."
        )
    elif profile_name == "finance":
        return Operation(
            instructions="Explain PCI DSS compliance requirements for financial applications."
        )
    elif profile_name == "education":
        return Operation(
            instructions="Explain FERPA compliance requirements for educational applications."
        )
    elif profile_name == "creative":
        return Operation(
            instructions="Write a creative short story about a robot learning to paint."
        )
    else:
        return Operation(
            instructions=f"Explain what {profile_name} security means and why it's important."
        )

def test_custom_profile(profile_name):
    """Test a specific custom security profile."""
    print(f"\n{'=' * 80}")
    print(f"Testing {profile_name.upper()} Custom Security Profile")
    print(f"{'=' * 80}")
    
    # Get profile details
    profile = get_custom_profile(profile_name)
    if profile:
        print(f"Profile description: {profile['description']}")
        print(f"Profile thresholds: {profile['thresholds']}")
        print(f"Profile checks: {profile['checks']}")
    else:
        print(f"Profile '{profile_name}' not found")
        return False
    
    # Create an expert with the specified profile
    expert = create_expert_with_profile(profile_name)
    print(f"Created expert with {profile_name} security profile")
    
    # Create an operation appropriate for the profile
    operation = create_operation_for_profile(profile_name)
    print(f"Created operation: '{operation.instructions}'")
    
    # Assign the expert to the operation
    operation.expert = expert
    
    # Create a squad with the same security level
    squad = Squad(
        experts=[expert],
        operations=[operation],
        process="sequential",
        security_level=profile_name
    )
    print(f"Created squad with {profile_name} security level")
    
    # Deploy the squad
    print("\nDeploying squad...")
    try:
        result = squad.deploy()
        print("\nResult:")
        print(f"{'-' * 40}")
        print(result)
        print(f"{'-' * 40}")
        print(f"\n✅ {profile_name.upper()} custom security profile test PASSED")
        return True
    except Exception as e:
        print(f"\n❌ {profile_name.upper()} custom security profile test FAILED: {e}")
        return False

def main():
    """Run the custom security profiles demo."""
    print("TBH Secure Agents - Custom Security Profiles Demo")
    print("=" * 50)
    
    # Register industry profiles
    print("Registering custom security profiles...")
    profiles = register_industry_profiles()
    
    # List registered profiles
    registered_profiles = list_custom_profiles()
    print(f"Registered profiles: {registered_profiles}")
    
    # Test each custom profile
    results = {}
    for profile_name in registered_profiles:
        results[profile_name] = test_custom_profile(profile_name)
    
    # Print summary
    print("\n" + "=" * 50)
    print("Custom Security Profiles Demo Summary")
    print("=" * 50)
    
    for profile_name, success in results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"- {profile_name.upper()}: {status}")
    
    print("\nConclusion:")
    if all(results.values()):
        print("✅ All custom security profiles work as expected")
    else:
        print("❌ Some custom security profiles failed")
    
    # Clear caches
    clear_caches()
    print("\nCaches cleared")

if __name__ == "__main__":
    main()
