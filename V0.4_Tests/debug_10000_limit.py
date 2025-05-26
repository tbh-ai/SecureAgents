#!/usr/bin/env python3
"""
Debug script to isolate the 10000 character limit issue.
"""

import os
import sys

# Set API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyA3ZxbIXpR3yNkZwGDznrztdQmgnU16DJI"

def test_10000_limit():
    """Test to isolate where the 10000 character limit is coming from."""
    
    print("🔍 DEBUGGING 10000 CHARACTER LIMIT ISSUE")
    print("=" * 50)
    
    try:
        from tbh_secure_agents import Expert
        
        # Create a prompt that's longer than 10000 characters
        test_prompt = "Write a detailed analysis about Python programming. " * 200  # About 11,000 characters
        
        print(f"Test prompt length: {len(test_prompt)} characters")
        print(f"Expected: Should work with minimal security profile")
        
        # Test 1: Create expert with minimal security profile
        print("\n🧪 Test 1: Expert with minimal security profile")
        expert = Expert(
            specialty="Test Expert",
            objective="Test long prompts",
            security_profile="minimal"
        )
        
        print(f"Expert created successfully")
        print(f"Security profile: {expert.security_profile}")
        
        # Test 2: Call _is_prompt_secure directly
        print("\n🧪 Test 2: Direct call to _is_prompt_secure")
        try:
            is_secure = expert._is_prompt_secure(test_prompt)
            print(f"_is_prompt_secure returned: {is_secure}")
        except Exception as e:
            print(f"ERROR in _is_prompt_secure: {e}")
        
        # Test 3: Try execute_task
        print("\n🧪 Test 3: Execute task with long prompt")
        try:
            result = expert.execute_task(test_prompt)
            if "Error:" in result:
                print(f"❌ FAILED: {result}")
            else:
                print(f"✅ SUCCESS: Task executed successfully")
                print(f"Result length: {len(result)} characters")
        except Exception as e:
            print(f"ERROR in execute_task: {e}")
        
        # Test 4: Check if integration is enabled
        print("\n🧪 Test 4: Check integration status")
        print(f"Has use_hybrid_validation: {hasattr(expert, 'use_hybrid_validation')}")
        if hasattr(expert, 'use_hybrid_validation'):
            print(f"use_hybrid_validation value: {expert.use_hybrid_validation}")
        
        # Test 5: Check method source
        print("\n🧪 Test 5: Check _is_prompt_secure method source")
        import inspect
        source_file = inspect.getfile(expert._is_prompt_secure)
        print(f"Method source file: {source_file}")
        
        # Test 6: Try with different security profiles
        print("\n🧪 Test 6: Test other security profiles")
        for profile in ["standard", "high"]:
            try:
                test_expert = Expert(
                    specialty="Test Expert",
                    objective="Test security profiles",
                    security_profile=profile
                )
                is_secure = test_expert._is_prompt_secure(test_prompt)
                print(f"{profile} profile: {is_secure}")
            except Exception as e:
                print(f"{profile} profile ERROR: {e}")
        
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_10000_limit()
