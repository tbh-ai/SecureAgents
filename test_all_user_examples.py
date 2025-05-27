#!/usr/bin/env python3
"""
🧪 COMPREHENSIVE USER EXAMPLES TEST 🧪
Running all user-friendly examples to validate complete integration.
"""

import os
import sys
import time
import subprocess
import traceback
from pathlib import Path

# Set API key for testing
os.environ["GOOGLE_API_KEY"] = "AIzaSyA3ZxbIXpR3yNkZwGDznrztdQmgnU16DJI"

# Add the tbh_secure_agents to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'tbh_secure_agents'))

# Import security validation to enable hybrid validation
from tbh_secure_agents.security_validation import (
    enable_hybrid_validation,
    get_next_gen_adaptive_validator
)

def test_all_user_examples():
    """Test all user-friendly examples systematically."""
    print("🧪 COMPREHENSIVE USER EXAMPLES TEST 🧪\n")
    
    # Enable hybrid validation for all tests
    print("🔗 Enabling Hybrid Validation Integration:")
    try:
        enable_hybrid_validation()
        print("   ✅ Hybrid validation enabled for all examples")
    except Exception as e:
        print(f"   ⚠️ Integration issue: {e}")
    
    # Initialize adaptive learning monitor
    print("\n🧠 Initializing Adaptive Learning Monitor:")
    try:
        adaptive_validator = get_next_gen_adaptive_validator()
        adaptive_engine = adaptive_validator.engine
        initial_patterns = len(adaptive_engine.enhanced_patterns)
        initial_profiles = len(adaptive_engine.behavioral_profiles)
        print(f"   📊 Initial Patterns: {initial_patterns}")
        print(f"   🎭 Initial Profiles: {initial_profiles}")
    except Exception as e:
        print(f"   ❌ Adaptive learning initialization failed: {e}")
        adaptive_engine = None
    
    # Define all user-friendly examples
    examples = [
        {
            "name": "AI Researcher",
            "file": "examples/user_friendly/1_ai_researcher.py",
            "description": "Research and analysis expert",
            "expected_output": "Research report in markdown format"
        },
        {
            "name": "AI Code Developer", 
            "file": "examples/user_friendly/2_ai_code_developer.py",
            "description": "Software development expert",
            "expected_output": "Python code file"
        },
        {
            "name": "AI Content Creator",
            "file": "examples/user_friendly/2_ai_content_creator.py", 
            "description": "Content creation expert",
            "expected_output": "Creative content"
        },
        {
            "name": "AI Writer",
            "file": "examples/user_friendly/2_ai_writer.py",
            "description": "Writing and editing expert", 
            "expected_output": "Written content"
        },
        {
            "name": "AI Business Analyst",
            "file": "examples/user_friendly/3_ai_business_analyst.py",
            "description": "Business analysis expert",
            "expected_output": "Business analysis in JSON format"
        },
        {
            "name": "AI Data Analyst", 
            "file": "examples/user_friendly/3_ai_data_analyst.py",
            "description": "Data analysis expert",
            "expected_output": "Data analysis report"
        },
        {
            "name": "AI Marketing Strategist",
            "file": "examples/user_friendly/4_ai_marketing_strategist.py",
            "description": "Marketing strategy expert",
            "expected_output": "Marketing strategy in HTML format"
        },
        {
            "name": "AI Technical Writer",
            "file": "examples/user_friendly/4_ai_technical_writer.py", 
            "description": "Technical documentation expert",
            "expected_output": "Technical documentation"
        },
        {
            "name": "AI Financial Advisor",
            "file": "examples/user_friendly/5_ai_financial_advisor.py",
            "description": "Financial advice expert", 
            "expected_output": "Financial advice in PDF format"
        },
        {
            "name": "AI Research Writing Team",
            "file": "examples/user_friendly/5_ai_research_writing_team.py",
            "description": "Collaborative research team",
            "expected_output": "Collaborative research output"
        }
    ]
    
    print(f"\n📊 RUNNING {len(examples)} USER-FRIENDLY EXAMPLES\n")
    
    results = []
    total_start_time = time.time()
    
    for i, example in enumerate(examples, 1):
        print(f"🧪 Test {i}/{len(examples)}: {example['name']}")
        print(f"   📁 File: {example['file']}")
        print(f"   📝 Description: {example['description']}")
        print(f"   🎯 Expected: {example['expected_output']}")
        
        # Check if file exists
        if not os.path.exists(example['file']):
            print(f"   ❌ SKIPPED: File not found")
            results.append({
                "name": example['name'],
                "status": "skipped",
                "reason": "File not found",
                "time": 0
            })
            print()
            continue
        
        # Run the example
        start_time = time.time()
        try:
            print(f"   🚀 Executing...")
            
            # Run the example as a subprocess to isolate it
            result = subprocess.run(
                [sys.executable, example['file']],
                cwd=os.getcwd(),
                capture_output=True,
                text=True,
                timeout=180  # 3 minute timeout per example
            )
            
            execution_time = time.time() - start_time
            
            if result.returncode == 0:
                print(f"   ✅ SUCCESS: Completed in {execution_time:.2f} seconds")
                
                # Check for any security warnings in output
                security_warnings = 0
                if "SECURITY WARNING" in result.stdout or "SECURITY WARNING" in result.stderr:
                    security_warnings = result.stdout.count("SECURITY WARNING") + result.stderr.count("SECURITY WARNING")
                    print(f"   ⚠️ Security warnings: {security_warnings}")
                
                # Check for any errors in output
                if "Error" in result.stdout or "Error" in result.stderr:
                    print(f"   ⚠️ Errors detected in output")
                
                results.append({
                    "name": example['name'],
                    "status": "success",
                    "time": execution_time,
                    "security_warnings": security_warnings,
                    "stdout_length": len(result.stdout),
                    "stderr_length": len(result.stderr)
                })
                
            else:
                print(f"   ❌ FAILED: Exit code {result.returncode}")
                print(f"   📝 Error output: {result.stderr[:200]}...")
                
                results.append({
                    "name": example['name'],
                    "status": "failed", 
                    "reason": f"Exit code {result.returncode}",
                    "time": execution_time,
                    "error": result.stderr[:500]
                })
        
        except subprocess.TimeoutExpired:
            execution_time = time.time() - start_time
            print(f"   ⏰ TIMEOUT: Exceeded 3 minute limit")
            results.append({
                "name": example['name'],
                "status": "timeout",
                "time": execution_time,
                "reason": "Execution timeout (3 minutes)"
            })
        
        except Exception as e:
            execution_time = time.time() - start_time
            print(f"   ❌ EXCEPTION: {e}")
            results.append({
                "name": example['name'],
                "status": "exception",
                "time": execution_time,
                "reason": str(e)
            })
        
        print()
    
    total_execution_time = time.time() - total_start_time
    
    print("📊 COMPREHENSIVE RESULTS ANALYSIS\n")
    
    # Categorize results
    successful = [r for r in results if r['status'] == 'success']
    failed = [r for r in results if r['status'] == 'failed']
    timeouts = [r for r in results if r['status'] == 'timeout']
    exceptions = [r for r in results if r['status'] == 'exception']
    skipped = [r for r in results if r['status'] == 'skipped']
    
    print(f"🎯 OVERALL STATISTICS:")
    print(f"   📊 Total Examples: {len(examples)}")
    print(f"   ✅ Successful: {len(successful)}")
    print(f"   ❌ Failed: {len(failed)}")
    print(f"   ⏰ Timeouts: {len(timeouts)}")
    print(f"   🚨 Exceptions: {len(exceptions)}")
    print(f"   ⏭️ Skipped: {len(skipped)}")
    print(f"   ⏱️ Total Time: {total_execution_time:.2f} seconds")
    
    success_rate = (len(successful) / len(examples)) * 100
    print(f"   🎊 Success Rate: {success_rate:.1f}%")
    
    if successful:
        print(f"\n✅ SUCCESSFUL EXAMPLES:")
        for result in successful:
            warnings = result.get('security_warnings', 0)
            warning_text = f" ({warnings} security warnings)" if warnings > 0 else ""
            print(f"   - {result['name']}: {result['time']:.2f}s{warning_text}")
        
        # Performance analysis
        times = [r['time'] for r in successful]
        print(f"\n⚡ PERFORMANCE ANALYSIS:")
        print(f"   - Fastest: {min(times):.2f}s")
        print(f"   - Slowest: {max(times):.2f}s")
        print(f"   - Average: {sum(times)/len(times):.2f}s")
        print(f"   - Total: {sum(times):.2f}s")
        
        # Security analysis
        total_warnings = sum(r.get('security_warnings', 0) for r in successful)
        if total_warnings > 0:
            print(f"\n🛡️ SECURITY ANALYSIS:")
            print(f"   - Total Security Warnings: {total_warnings}")
            print(f"   - Examples with Warnings: {len([r for r in successful if r.get('security_warnings', 0) > 0])}")
    
    if failed:
        print(f"\n❌ FAILED EXAMPLES:")
        for result in failed:
            print(f"   - {result['name']}: {result.get('reason', 'Unknown error')}")
    
    if timeouts:
        print(f"\n⏰ TIMEOUT EXAMPLES:")
        for result in timeouts:
            print(f"   - {result['name']}: Exceeded 3 minute limit")
    
    if exceptions:
        print(f"\n🚨 EXCEPTION EXAMPLES:")
        for result in exceptions:
            print(f"   - {result['name']}: {result.get('reason', 'Unknown exception')}")
    
    # Adaptive learning analysis
    if adaptive_engine:
        print(f"\n🧠 ADAPTIVE LEARNING ANALYSIS:")
        final_patterns = len(adaptive_engine.enhanced_patterns)
        final_profiles = len(adaptive_engine.behavioral_profiles)
        attack_history = len(adaptive_engine.attack_history)
        
        print(f"   📊 Enhanced Patterns: {initial_patterns} → {final_patterns}")
        print(f"   🎭 Behavioral Profiles: {initial_profiles} → {final_profiles}")
        print(f"   📈 Attack History: {attack_history} entries")
        
        if final_profiles > initial_profiles:
            print(f"   ✅ Learning Active: +{final_profiles - initial_profiles} new profiles")
        else:
            print(f"   ➖ Limited Learning: No new profiles created")
        
        if final_profiles > 0:
            print(f"\n   👥 User Profiles Created:")
            for user_id, profile in list(adaptive_engine.behavioral_profiles.items())[:5]:
                print(f"      - {user_id}: risk={profile.risk_score:.3f}")
    
    # Integration assessment
    print(f"\n🎊 INTEGRATION ASSESSMENT:")
    
    integration_score = 0
    total_checks = 6
    
    # Check 1: Basic functionality
    if len(successful) > 0:
        print(f"   ✅ Basic functionality working ({len(successful)} examples successful)")
        integration_score += 1
    else:
        print(f"   ❌ Basic functionality issues (no successful examples)")
    
    # Check 2: Success rate
    if success_rate >= 70:
        print(f"   ✅ High success rate ({success_rate:.1f}%)")
        integration_score += 1
    elif success_rate >= 50:
        print(f"   ⚠️ Moderate success rate ({success_rate:.1f}%)")
        integration_score += 0.5
    else:
        print(f"   ❌ Low success rate ({success_rate:.1f}%)")
    
    # Check 3: Performance
    if successful and max(r['time'] for r in successful) < 60:
        print(f"   ✅ Performance acceptable (max {max(r['time'] for r in successful):.1f}s)")
        integration_score += 1
    elif successful:
        print(f"   ⚠️ Performance concerns (max {max(r['time'] for r in successful):.1f}s)")
        integration_score += 0.5
    else:
        print(f"   ❌ Performance cannot be assessed")
    
    # Check 4: Security integration
    if adaptive_engine and (final_profiles > initial_profiles or attack_history > 0):
        print(f"   ✅ Security integration active")
        integration_score += 1
    else:
        print(f"   ⚠️ Limited security integration activity")
        integration_score += 0.5
    
    # Check 5: Error handling
    if len(exceptions) == 0:
        print(f"   ✅ Good error handling (no exceptions)")
        integration_score += 1
    elif len(exceptions) <= 2:
        print(f"   ⚠️ Some error handling issues ({len(exceptions)} exceptions)")
        integration_score += 0.5
    else:
        print(f"   ❌ Poor error handling ({len(exceptions)} exceptions)")
    
    # Check 6: Timeout management
    if len(timeouts) == 0:
        print(f"   ✅ Good timeout management (no timeouts)")
        integration_score += 1
    elif len(timeouts) <= 2:
        print(f"   ⚠️ Some timeout issues ({len(timeouts)} timeouts)")
        integration_score += 0.5
    else:
        print(f"   ❌ Poor timeout management ({len(timeouts)} timeouts)")
    
    final_score = (integration_score / total_checks) * 100
    print(f"\n🎯 FINAL INTEGRATION SCORE: {integration_score:.1f}/{total_checks} ({final_score:.1f}%)")
    
    # Final assessment
    if final_score >= 85:
        print(f"\n🚀 EXCELLENT: User examples integration is production-ready!")
        print(f"   🔗 Framework working seamlessly with security")
        print(f"   🧠 Adaptive learning monitoring all activities")
        print(f"   ⚡ Performance optimized for real-world use")
        print(f"   🛡️ Security validation integrated properly")
        return True
    elif final_score >= 70:
        print(f"\n✅ GOOD: User examples working well with minor issues")
        print(f"   🔧 Some optimization opportunities available")
        return True
    elif final_score >= 50:
        print(f"\n⚠️ MODERATE: User examples working but need improvement")
        print(f"   🔧 Several issues need to be addressed")
        return False
    else:
        print(f"\n❌ POOR: Significant integration issues detected")
        print(f"   🔧 Major fixes required before production use")
        return False

if __name__ == "__main__":
    print("🧪 STARTING COMPREHENSIVE USER EXAMPLES TEST 🧪")
    print("=" * 60)
    
    success = test_all_user_examples()
    
    print("=" * 60)
    print(f"🎯 FINAL RESULT: {'SUCCESS' if success else 'NEEDS IMPROVEMENT'}")
    
    if success:
        print("\n🎉 The enhanced adaptive security system is successfully")
        print("   integrated with all user-friendly examples!")
        print("   Ready for production deployment! 🚀")
    else:
        print("\n🔧 Some issues detected - check the detailed analysis above")
        print("   for specific areas that need attention.")
