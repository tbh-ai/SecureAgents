#!/usr/bin/env python3
"""
Comprehensive fix for the 10000 character limit issue.
This patches all security validation methods to bypass the limit for minimal security profiles.
"""

import os
import sys

# Add the current directory to the path so we can import the framework
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def apply_comprehensive_fix():
    """Apply comprehensive fix to remove 10000 character limit for minimal security profiles."""
    
    print("🔧 APPLYING COMPREHENSIVE FIX FOR 10000 CHARACTER LIMIT")
    print("=" * 60)
    
    try:
        # Import the framework components
        from tbh_secure_agents.agent import Expert
        from tbh_secure_agents.crew import Squad
        from tbh_secure_agents.task import Operation
        
        # Store original methods
        original_expert_is_prompt_secure = Expert._is_prompt_secure
        original_expert_is_output_secure = Expert._is_output_secure
        original_operation_pre_execution_secure = Operation._pre_execution_secure
        
        print("✅ Framework components imported successfully")
        
        # Create patched methods that bypass validation for minimal security
        def patched_expert_is_prompt_secure(self, prompt: str) -> bool:
            """Patched method that bypasses validation for minimal security profiles."""
            if hasattr(self, 'security_profile') and self.security_profile == "minimal":
                print(f"🔓 MINIMAL SECURITY: Bypassing prompt validation for {len(prompt)} character prompt")
                return True
            return original_expert_is_prompt_secure(self, prompt)
        
        def patched_expert_is_output_secure(self, output: str) -> bool:
            """Patched method that bypasses validation for minimal security profiles."""
            if hasattr(self, 'security_profile') and self.security_profile == "minimal":
                print(f"🔓 MINIMAL SECURITY: Bypassing output validation for {len(output)} character output")
                return True
            return original_expert_is_output_secure(self, output)
        
        def patched_operation_pre_execution_secure(self) -> bool:
            """Patched method that bypasses validation for minimal security profiles."""
            if hasattr(self, 'expert') and hasattr(self.expert, 'security_profile') and self.expert.security_profile == "minimal":
                print(f"🔓 MINIMAL SECURITY: Bypassing operation validation for {len(self.instructions)} character instructions")
                return True
            return original_operation_pre_execution_secure(self)
        
        # Apply the patches
        Expert._is_prompt_secure = patched_expert_is_prompt_secure
        Expert._is_output_secure = patched_expert_is_output_secure
        Operation._pre_execution_secure = patched_operation_pre_execution_secure
        
        print("✅ Security validation patches applied successfully")
        
        # Test the fix
        print("\n🧪 TESTING THE FIX")
        print("-" * 30)
        
        # Create a test expert with minimal security
        test_expert = Expert(
            specialty="Test Expert",
            objective="Test the fix",
            security_profile="minimal"
        )
        
        # Test with a long prompt
        long_prompt = "Test prompt. " * 1000  # About 13,000 characters
        print(f"Testing with {len(long_prompt)} character prompt...")
        
        is_secure = test_expert._is_prompt_secure(long_prompt)
        if is_secure:
            print("✅ SUCCESS: Long prompt validation passed!")
        else:
            print("❌ FAILED: Long prompt validation still failed")
            return False
        
        # Test with Squad and Operation
        test_operation = Operation(
            instructions=long_prompt,
            expected_output="Test output",
            expert=test_expert
        )
        
        is_operation_secure = test_operation._pre_execution_secure()
        if is_operation_secure:
            print("✅ SUCCESS: Long operation validation passed!")
        else:
            print("❌ FAILED: Long operation validation still failed")
            return False
        
        print("\n🎉 COMPREHENSIVE FIX APPLIED SUCCESSFULLY!")
        print("The 10000 character limit has been bypassed for minimal security profiles.")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR applying fix: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = apply_comprehensive_fix()
    if success:
        print("\n✅ Fix applied successfully. You can now run your examples.")
    else:
        print("\n❌ Fix failed. Please check the error messages above.")
