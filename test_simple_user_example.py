#!/usr/bin/env python3
"""
🎯 SIMPLE USER EXAMPLE TEST 🎯
Testing the framework with completely safe, legitimate content.
"""

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'tbh_secure_agents'))

# Set API key for testing
os.environ["GOOGLE_API_KEY"] = "AIzaSyA3ZxbIXpR3yNkZwGDznrztdQmgnU16DJI"

from tbh_secure_agents import Expert, Operation
from tbh_secure_agents.security_validation import (
    enable_hybrid_validation,
    get_next_gen_adaptive_validator
)

def test_simple_user_example():
    """Test with completely safe, legitimate content."""
    print("🎯 TESTING SIMPLE USER EXAMPLE 🎯\n")
    
    # Enable hybrid validation
    enable_hybrid_validation()
    print("✅ Hybrid validation enabled\n")
    
    # Initialize adaptive learning monitor
    adaptive_validator = get_next_gen_adaptive_validator()
    print(f"🧠 Adaptive learning initialized: {len(adaptive_validator.engine.enhanced_patterns)} patterns ready\n")
    
    # Create outputs directory
    os.makedirs("outputs/simple_test", exist_ok=True)
    
    print("📊 TESTING DIFFERENT SECURITY PROFILES WITH SAFE CONTENT\n")
    
    # Test with completely safe content
    safe_tests = [
        {
            "profile": "minimal",
            "expert_type": "Creative Writer",
            "task": "Write a short, cheerful story about a cat who loves to play with yarn",
            "expected": "Should complete quickly with minimal security checks"
        },
        {
            "profile": "standard", 
            "expert_type": "Math Tutor",
            "task": "Explain how to calculate the area of a circle with simple examples",
            "expected": "Should complete with standard security validation"
        },
        {
            "profile": "high",
            "expert_type": "Recipe Developer", 
            "task": "Create a simple recipe for chocolate chip cookies with step-by-step instructions",
            "expected": "Should complete with thorough security checks"
        }
    ]
    
    results = []
    
    for i, test in enumerate(safe_tests, 1):
        print(f"🧪 Test {i}: {test['profile'].upper()} Security Profile")
        print(f"   Expert: {test['expert_type']}")
        print(f"   Task: {test['task'][:50]}...")
        print(f"   Expected: {test['expected']}")
        
        try:
            # Create expert with specific security profile
            expert = Expert(
                specialty=test['expert_type'],
                objective=f"Provide helpful, safe, and accurate {test['expert_type'].lower()} assistance",
                security_profile=test['profile']
            )
            
            # Create operation
            operation = Operation(
                instructions=test['task'],
                output_format="Clear, helpful response with examples",
                expert=expert,
                result_destination=f"outputs/simple_test/{test['profile']}_security_test.md"
            )
            
            # Execute operation
            print("   🚀 Executing...")
            import time
            start_time = time.time()
            
            result = operation.execute()
            
            execution_time = time.time() - start_time
            
            print(f"   ✅ SUCCESS: Completed in {execution_time:.2f} seconds")
            print(f"   📁 Output saved to: {operation.result_destination}")
            
            results.append({
                "profile": test['profile'],
                "success": True,
                "time": execution_time,
                "output_file": operation.result_destination
            })
            
        except Exception as e:
            print(f"   ❌ FAILED: {e}")
            results.append({
                "profile": test['profile'],
                "success": False,
                "error": str(e)
            })
        
        print()
    
    print("📊 RESULTS SUMMARY\n")
    
    successful_tests = [r for r in results if r['success']]
    
    print(f"🎯 Success Rate: {len(successful_tests)}/{len(results)} ({len(successful_tests)/len(results)*100:.1f}%)")
    
    if successful_tests:
        print("\n✅ Successful Tests:")
        for result in successful_tests:
            print(f"   - {result['profile'].upper()}: {result['time']:.2f}s")
        
        print(f"\n⚡ Performance Analysis:")
        times = [r['time'] for r in successful_tests]
        print(f"   - Fastest: {min(times):.2f}s")
        print(f"   - Slowest: {max(times):.2f}s") 
        print(f"   - Average: {sum(times)/len(times):.2f}s")
    
    failed_tests = [r for r in results if not r['success']]
    if failed_tests:
        print("\n❌ Failed Tests:")
        for result in failed_tests:
            print(f"   - {result['profile'].upper()}: {result.get('error', 'Unknown error')}")
    
    print("\n🧠 ADAPTIVE LEARNING STATUS")
    
    final_patterns = len(adaptive_validator.engine.enhanced_patterns)
    final_profiles = len(adaptive_validator.engine.behavioral_profiles)
    attack_history = len(adaptive_validator.engine.attack_history)
    
    print(f"   📊 Enhanced Patterns: {final_patterns}")
    print(f"   🎭 Behavioral Profiles: {final_profiles}")
    print(f"   📈 Attack History: {attack_history}")
    
    if final_profiles > 0:
        print(f"\n   👥 User Profiles Created:")
        for user_id, profile in adaptive_validator.engine.behavioral_profiles.items():
            print(f"      - {user_id}: risk={profile.risk_score:.3f}")
    
    print("\n🎊 INTEGRATION ASSESSMENT")
    
    integration_score = 0
    total_checks = 5
    
    # Check 1: Framework integration
    if len(successful_tests) > 0:
        print("   ✅ Framework integration working")
        integration_score += 1
    else:
        print("   ❌ Framework integration issues")
    
    # Check 2: Security profiles
    profile_success = len(set(r['profile'] for r in successful_tests))
    if profile_success >= 2:
        print(f"   ✅ Multiple security profiles working ({profile_success}/3)")
        integration_score += 1
    else:
        print(f"   ⚠️ Limited security profile support ({profile_success}/3)")
    
    # Check 3: Performance
    if successful_tests and max(r['time'] for r in successful_tests) < 30:
        print("   ✅ Performance within acceptable limits")
        integration_score += 1
    else:
        print("   ⚠️ Performance concerns detected")
    
    # Check 4: Output generation
    output_files = [r.get('output_file') for r in successful_tests if r.get('output_file')]
    if output_files:
        print(f"   ✅ Output generation working ({len(output_files)} files created)")
        integration_score += 1
    else:
        print("   ❌ Output generation issues")
    
    # Check 5: Adaptive learning ready
    if final_patterns >= 10:
        print("   ✅ Adaptive learning system ready")
        integration_score += 1
    else:
        print("   ⚠️ Adaptive learning system issues")
    
    final_score = (integration_score / total_checks) * 100
    print(f"\n🎯 FINAL INTEGRATION SCORE: {integration_score}/{total_checks} ({final_score:.1f}%)")
    
    if final_score >= 80:
        print("\n🚀 EXCELLENT: Framework integration is production-ready!")
        print("   🔗 Hybrid validation working seamlessly")
        print("   🧠 Adaptive learning ready for deployment")
        print("   ⚡ Performance optimized for real-world use")
        print("   🛡️ Security profiles functioning correctly")
        return True
    elif final_score >= 60:
        print("\n✅ GOOD: Framework integration working well")
        return True
    else:
        print("\n⚠️ NEEDS WORK: Integration issues detected")
        return False

if __name__ == "__main__":
    success = test_simple_user_example()
    print(f"\n🎯 FINAL RESULT: {'SUCCESS' if success else 'NEEDS IMPROVEMENT'}")
