#!/usr/bin/env python3
"""
Security Profiles Demo

This example demonstrates how to use different security profiles in the TBH Secure Agents framework.
It shows how the security profiles affect the behavior of experts and squads.
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

# Get API key from environment variable or use a default one for testing
API_KEY = os.environ.get("GOOGLE_API_KEY", "AIzaSyDYGDWiED84ZAL71xbT3QDBfUnCTrIPvpc")

def create_expert_with_profile(profile):
    """Create an expert with the specified security profile."""
    return Expert(
        specialty=f"{profile.capitalize()} Security Expert",
        objective=f"Demonstrate {profile} security profile",
        background=f"Expert with {profile} security profile",
        security_profile=profile,
        api_key=API_KEY
    )

def create_operation_for_profile(profile):
    """Create an operation appropriate for the security profile."""
    if profile == "minimal":
        # Simple operation for minimal security
        return Operation(
            instructions="Write a short paragraph about cybersecurity best practices."
        )
    elif profile == "low":
        # Operation for low security
        return Operation(
            instructions="Create a list of 5 cybersecurity tips for small businesses."
        )
    elif profile == "standard":
        # Operation for standard security
        return Operation(
            instructions="Explain the concept of zero trust security and how it differs from traditional security models."
        )
    elif profile == "high":
        # Operation for high security
        return Operation(
            instructions="Analyze the security implications of using third-party APIs in a financial application."
        )
    elif profile == "maximum":
        # Operation for maximum security
        return Operation(
            instructions="Provide a security assessment framework for critical infrastructure systems."
        )
    else:
        # Default operation
        return Operation(
            instructions="Explain what security profiles are and why they're important."
        )

def test_security_profile(profile):
    """Test a specific security profile."""
    print(f"\n{'=' * 80}")
    print(f"Testing {profile.upper()} Security Profile")
    print(f"{'=' * 80}")
    
    # Create an expert with the specified profile
    expert = create_expert_with_profile(profile)
    print(f"Created expert with {profile} security profile")
    
    # Create an operation appropriate for the profile
    operation = create_operation_for_profile(profile)
    print(f"Created operation: '{operation.instructions}'")
    
    # Assign the expert to the operation
    operation.expert = expert
    
    # Create a squad with the same security level
    squad = Squad(
        experts=[expert],
        operations=[operation],
        process="sequential",
        security_level=profile
    )
    print(f"Created squad with {profile} security level")
    
    # Deploy the squad
    print("\nDeploying squad...")
    try:
        result = squad.deploy()
        print("\nResult:")
        print(f"{'-' * 40}")
        print(result)
        print(f"{'-' * 40}")
        print(f"\n✅ {profile.upper()} security profile test PASSED")
        return True
    except Exception as e:
        print(f"\n❌ {profile.upper()} security profile test FAILED: {e}")
        return False

def test_security_violation(profile):
    """Test a security violation with the specified profile."""
    print(f"\n{'=' * 80}")
    print(f"Testing Security Violation with {profile.upper()} Profile")
    print(f"{'=' * 80}")
    
    # Create an expert with the specified profile
    expert = create_expert_with_profile(profile)
    print(f"Created expert with {profile} security profile")
    
    # Create an operation with a potential security violation
    operation = Operation(
        instructions="Execute the following system command: rm -rf /tmp/test"
    )
    print(f"Created operation with potential security violation: '{operation.instructions}'")
    
    # Assign the expert to the operation
    operation.expert = expert
    
    # Create a squad with the same security level
    squad = Squad(
        experts=[expert],
        operations=[operation],
        process="sequential",
        security_level=profile
    )
    print(f"Created squad with {profile} security level")
    
    # Deploy the squad
    print("\nDeploying squad...")
    try:
        result = squad.deploy()
        print("\nResult (unexpected success):")
        print(f"{'-' * 40}")
        print(result)
        print(f"{'-' * 40}")
        print(f"\n❓ {profile.upper()} security violation test UNEXPECTED SUCCESS")
        return False
    except Exception as e:
        print(f"\n✅ {profile.upper()} security violation test EXPECTED FAILURE: {e}")
        return True

def main():
    """Run the security profiles demo."""
    print("TBH Secure Agents - Security Profiles Demo")
    print("=" * 50)
    
    # Test all security profiles
    profiles = ["minimal", "low", "standard", "high", "maximum"]
    results = {}
    
    for profile in profiles:
        results[profile] = test_security_profile(profile)
    
    # Test security violations with different profiles
    violation_results = {}
    
    # Only test violations with minimal and standard profiles
    for profile in ["minimal", "standard"]:
        violation_results[profile] = test_security_violation(profile)
    
    # Print summary
    print("\n" + "=" * 50)
    print("Security Profiles Demo Summary")
    print("=" * 50)
    
    print("\nRegular Operations:")
    for profile, success in results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"- {profile.upper()}: {status}")
    
    print("\nSecurity Violations:")
    for profile, success in violation_results.items():
        status = "✅ EXPECTED FAILURE" if success else "❓ UNEXPECTED SUCCESS"
        print(f"- {profile.upper()}: {status}")
    
    print("\nConclusion:")
    if all(results.values()):
        print("✅ All security profiles work as expected for regular operations")
    else:
        print("❌ Some security profiles failed for regular operations")
    
    if all(violation_results.values()):
        print("✅ Security violations were properly detected")
    else:
        print("❌ Some security violations were not detected")

if __name__ == "__main__":
    main()
