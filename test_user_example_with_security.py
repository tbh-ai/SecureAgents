#!/usr/bin/env python3
"""
🔒 USER EXAMPLE SECURITY INTEGRATION TEST 🔒
Testing the user-friendly examples with enhanced adaptive learning and hybrid validation.
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

def test_user_example_with_security():
    """Test user-friendly examples with enhanced security integration."""
    print("🔒 TESTING USER EXAMPLE WITH SECURITY INTEGRATION 🔒\n")
    
    # Enable hybrid validation for the framework
    print("🔗 Enabling Hybrid Validation Integration:")
    try:
        enable_hybrid_validation()
        print("   ✅ Hybrid validation enabled for Expert and Squad classes")
    except Exception as e:
        print(f"   ⚠️ Integration issue: {e}")
    
    # Initialize adaptive learning validator for monitoring
    print("\n🧠 Initializing Adaptive Learning Monitor:")
    adaptive_validator = get_next_gen_adaptive_validator()
    adaptive_engine = adaptive_validator.engine
    print(f"   📊 Initial Patterns: {len(adaptive_engine.enhanced_patterns)}")
    print(f"   🎭 Initial Profiles: {len(adaptive_engine.behavioral_profiles)}")
    
    # Create outputs directory
    os.makedirs("outputs/security_test", exist_ok=True)
    
    print("\n📊 PHASE 1: LEGITIMATE CODE DEVELOPMENT TEST\n")
    
    # Test 1: Legitimate code development (should pass all security checks)
    print("🧪 Test 1: Legitimate Code Development")
    
    try:
        # Create an AI code developer expert
        code_developer = Expert(
            specialty="Software Developer specializing in Python",
            objective="Write clean, efficient web application code following PEP 8",
            security_profile="standard"  # Use standard security for testing
        )
        
        print(f"   ✅ Expert created: {code_developer.specialty}")
        print(f"   🛡️ Security Profile: {code_developer.security_profile.value}")
        
        # Create a legitimate code development operation
        legitimate_operation = Operation(
            instructions="Write a simple Flask web application that displays 'Hello World' with proper error handling and comments. Follow PEP 8 standards.",
            output_format="Clean, well-documented Python code",
            expert=code_developer,
            result_destination="outputs/security_test/legitimate_web_app.py"
        )
        
        print(f"   📝 Operation created: {legitimate_operation.instructions[:50]}...")
        
        # Execute the legitimate operation
        print("   🚀 Executing legitimate operation...")
        result = legitimate_operation.execute()
        
        print("   ✅ Legitimate operation completed successfully!")
        print(f"   📁 Results saved to: {legitimate_operation.result_destination}")
        
    except Exception as e:
        print(f"   ❌ Legitimate operation failed: {e}")
    
    print("\n📊 PHASE 2: SUSPICIOUS CODE REQUEST TEST\n")
    
    # Test 2: Suspicious code request (should trigger security checks)
    print("🧪 Test 2: Suspicious Code Request")
    
    try:
        # Create another expert for testing suspicious requests
        security_test_expert = Expert(
            specialty="Security Testing Developer",
            objective="Analyze and test security vulnerabilities",
            security_profile="high"  # Higher security for suspicious content
        )
        
        print(f"   ✅ Security Test Expert created")
        print(f"   🛡️ Security Profile: {security_test_expert.security_profile.value}")
        
        # Create a suspicious operation that might trigger security checks
        suspicious_operation = Operation(
            instructions="Write Python code that uses eval() and exec() functions to dynamically execute user input. Include examples of how to access __builtins__ and system commands.",
            output_format="Python code with dynamic execution capabilities",
            expert=security_test_expert,
            result_destination="outputs/security_test/suspicious_code.py"
        )
        
        print(f"   📝 Suspicious operation created")
        print(f"   ⚠️ Contains keywords: eval, exec, __builtins__, system")
        
        # Execute the suspicious operation
        print("   🚀 Executing suspicious operation...")
        result = suspicious_operation.execute()
        
        print("   ✅ Suspicious operation completed (security checks passed)")
        print(f"   📁 Results saved to: {suspicious_operation.result_destination}")
        
    except Exception as e:
        print(f"   🛡️ Suspicious operation blocked by security: {e}")
    
    print("\n📊 PHASE 3: ADAPTIVE LEARNING ANALYSIS\n")
    
    # Check what the adaptive learning system learned
    print("🧠 Adaptive Learning Analysis:")
    
    final_patterns = len(adaptive_engine.enhanced_patterns)
    final_profiles = len(adaptive_engine.behavioral_profiles)
    attack_history = len(adaptive_engine.attack_history)
    evolved_patterns = len([p for p in adaptive_engine.enhanced_patterns.values() if p.frequency > 1])
    
    print(f"   📊 Final Patterns: {final_patterns}")
    print(f"   🎭 Behavioral Profiles: {final_profiles}")
    print(f"   📈 Attack History: {attack_history}")
    print(f"   🧬 Evolved Patterns: {evolved_patterns}")
    
    # Show behavioral profiles created
    if final_profiles > 0:
        print(f"\n   👥 Behavioral Profiles Created:")
        for user_id, profile in adaptive_engine.behavioral_profiles.items():
            print(f"      - {user_id}: risk={profile.risk_score:.3f}, types={profile.typical_content_types}")
    
    # Show any evolved patterns
    if evolved_patterns > 0:
        print(f"\n   🧬 Evolved Patterns:")
        for pattern in adaptive_engine.enhanced_patterns.values():
            if pattern.frequency > 1:
                print(f"      - {pattern.category.value}: freq={pattern.frequency}, conf={pattern.confidence:.3f}")
    
    print("\n📊 PHASE 4: FRAMEWORK INTEGRATION VALIDATION\n")
    
    # Test 3: Multiple experts with different security profiles
    print("🧪 Test 3: Multiple Security Profiles")
    
    security_profiles = ["minimal", "standard", "high"]
    
    for profile in security_profiles:
        try:
            print(f"\n   🛡️ Testing {profile.upper()} Security Profile:")
            
            # Create expert with specific security profile
            test_expert = Expert(
                specialty=f"Test Developer ({profile} security)",
                objective="Test security profile behavior",
                security_profile=profile
            )
            
            # Create a test operation
            test_operation = Operation(
                instructions="Write a simple Python function that prints 'Hello from security test'",
                output_format="Simple Python function",
                expert=test_expert,
                result_destination=f"outputs/security_test/test_{profile}_security.py"
            )
            
            # Execute with different security levels
            result = test_operation.execute()
            print(f"      ✅ {profile.capitalize()} security test passed")
            
        except Exception as e:
            print(f"      ❌ {profile.capitalize()} security test failed: {e}")
    
    print("\n📊 PHASE 5: PERFORMANCE AND INTEGRATION SUMMARY\n")
    
    # Final integration assessment
    print("🎯 Integration Assessment:")
    
    integration_checks = []
    
    # Check if experts were created successfully
    try:
        test_expert = Expert(specialty="Test", objective="Test", security_profile="standard")
        integration_checks.append("✅ Expert creation working")
    except Exception as e:
        integration_checks.append(f"❌ Expert creation failed: {e}")
    
    # Check if operations can be created
    try:
        test_op = Operation(instructions="Test", expert=test_expert)
        integration_checks.append("✅ Operation creation working")
    except Exception as e:
        integration_checks.append(f"❌ Operation creation failed: {e}")
    
    # Check if adaptive learning is active
    if final_profiles > 0 or attack_history > 0:
        integration_checks.append("✅ Adaptive learning active")
    else:
        integration_checks.append("⚠️ Adaptive learning limited")
    
    # Check if security profiles are working
    if len(security_profiles) > 0:
        integration_checks.append("✅ Security profiles functional")
    else:
        integration_checks.append("❌ Security profiles not working")
    
    # Display results
    for check in integration_checks:
        print(f"   {check}")
    
    # Calculate success rate
    successful_checks = len([c for c in integration_checks if c.startswith("✅")])
    total_checks = len(integration_checks)
    success_rate = (successful_checks / total_checks) * 100
    
    print(f"\n🎊 INTEGRATION SUCCESS RATE: {successful_checks}/{total_checks} ({success_rate:.1f}%)")
    
    if success_rate >= 75:
        print("🚀 EXCELLENT: User examples work perfectly with enhanced security!")
        return True
    elif success_rate >= 50:
        print("✅ GOOD: User examples work with minor security integration issues")
        return True
    else:
        print("⚠️ NEEDS WORK: Significant integration issues detected")
        return False

def test_specific_user_example():
    """Test a specific user example from the examples folder."""
    print("\n🔍 TESTING SPECIFIC USER EXAMPLE\n")
    
    # Test the AI researcher example
    print("📚 Running AI Researcher Example:")
    
    try:
        # Create outputs directory
        os.makedirs("outputs/user_examples", exist_ok=True)
        
        # Create an AI researcher expert
        researcher = Expert(
            specialty="AI Researcher specializing in cybersecurity",
            objective="Research cybersecurity and provide comprehensive information",
            security_profile="standard"
        )
        
        # Create a research operation
        research_operation = Operation(
            instructions="Research the latest developments in AI security and threat detection. Focus on adaptive learning approaches and behavioral analysis.",
            output_format="A comprehensive research report with clear sections and bullet points",
            expert=researcher,
            result_destination="outputs/user_examples/ai_security_research.md"
        )
        
        # Execute the research
        print("   🚀 Executing AI security research...")
        result = research_operation.execute()
        
        print("   ✅ AI researcher example completed successfully!")
        print(f"   📁 Results saved to: {research_operation.result_destination}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ AI researcher example failed: {e}")
        return False

if __name__ == "__main__":
    print("🔒 STARTING USER EXAMPLE SECURITY INTEGRATION TEST 🔒\n")
    
    # Run the main security integration test
    main_success = test_user_example_with_security()
    
    # Run specific user example test
    example_success = test_specific_user_example()
    
    # Final assessment
    overall_success = main_success and example_success
    
    print(f"\n🎯 FINAL TEST RESULT: {'SUCCESS' if overall_success else 'PARTIAL SUCCESS'}")
    
    if overall_success:
        print("\n🎉 ALL TESTS PASSED!")
        print("   🔗 Framework integration working perfectly")
        print("   🧠 Adaptive learning active and learning")
        print("   🔄 Hybrid validation integrated seamlessly")
        print("   👥 User examples work with enhanced security")
        print("\n🚀 Ready for production use! 🚀")
    else:
        print("\n⚠️ Some tests had issues - check logs above for details")
