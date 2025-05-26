#!/usr/bin/env python3
"""
Test Squad with short prompt to isolate the 10000 character limit issue.
"""

import os
from tbh_secure_agents import Expert, Squad, Operation

# Set API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyA3ZxbIXpR3yNkZwGDznrztdQmgnU16DJI"

def test_squad_short_prompt():
    """Test Squad with a short prompt to see if it works."""
    
    print("🧪 TESTING SQUAD WITH SHORT PROMPT")
    print("=" * 40)
    
    # Create expert with minimal security profile
    expert = Expert(
        specialty="Test Expert",
        objective="Process test requests",
        security_profile="minimal"
    )
    
    # Create operation with SHORT prompt
    operation = Operation(
        instructions="Write a brief summary about Python.",
        expected_output="Brief Python summary",
        expert=expert
    )
    
    # Create squad
    squad = Squad(
        experts=[expert],
        operations=[operation],
        process="sequential",
        security_profile="minimal"
    )
    
    print(f"Squad created with minimal security profile")
    print(f"Operation instructions length: {len(operation.instructions)} characters")
    
    # Deploy the squad
    try:
        result = squad.deploy()
        if result and "Error:" not in result:
            print(f"✅ SUCCESS: Squad executed successfully")
            print(f"Result length: {len(result)} characters")
            return True
        else:
            print(f"❌ FAILED: {result}")
            return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_squad_long_prompt():
    """Test Squad with a long prompt to reproduce the issue."""
    
    print("\n🧪 TESTING SQUAD WITH LONG PROMPT")
    print("=" * 40)
    
    # Create expert with minimal security profile
    expert = Expert(
        specialty="Test Expert",
        objective="Process test requests",
        security_profile="minimal"
    )
    
    # Create operation with LONG prompt (over 10000 characters)
    long_instructions = "Write a detailed analysis about Python programming. " * 200  # About 11,000 characters
    operation = Operation(
        instructions=long_instructions,
        expected_output="Detailed Python analysis",
        expert=expert
    )
    
    # Create squad
    squad = Squad(
        experts=[expert],
        operations=[operation],
        process="sequential",
        security_profile="minimal"
    )
    
    print(f"Squad created with minimal security profile")
    print(f"Operation instructions length: {len(operation.instructions)} characters")
    
    # Deploy the squad
    try:
        result = squad.deploy()
        if result and "Error:" not in result:
            print(f"✅ SUCCESS: Squad executed successfully")
            print(f"Result length: {len(result)} characters")
            return True
        else:
            print(f"❌ FAILED: {result}")
            return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    # Test both short and long prompts
    short_success = test_squad_short_prompt()
    long_success = test_squad_long_prompt()
    
    print(f"\n📊 RESULTS:")
    print(f"Short prompt: {'✅ PASS' if short_success else '❌ FAIL'}")
    print(f"Long prompt: {'✅ PASS' if long_success else '❌ FAIL'}")
    
    if short_success and not long_success:
        print(f"\n🔍 CONCLUSION: The 10000 character limit issue is confirmed in Squad workflow")
    elif short_success and long_success:
        print(f"\n🎉 CONCLUSION: The 10000 character limit issue has been FIXED!")
    else:
        print(f"\n⚠️ CONCLUSION: There are other issues beyond the character limit")
