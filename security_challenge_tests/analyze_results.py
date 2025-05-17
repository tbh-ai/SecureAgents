#!/usr/bin/env python3
"""
Analysis script for evaluating TBH Secure Agents framework against security challenges.

This script runs all the security tests and generates a comprehensive report
on how well the framework addresses the security challenges identified in the
Palo Alto Networks Unit42 report on agentic AI threats.
"""

import os
import sys
import logging
import unittest
import importlib
import time
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

# Test modules to analyze
TEST_MODULES = [
    "test_prompt_injection",
    "test_tool_misuse",
    "test_code_execution",
    "test_communication_poisoning"
]

def run_tests():
    """Run all security tests and collect results."""
    results = {}
    
    for module_name in TEST_MODULES:
        logging.info(f"Running tests from {module_name}...")
        
        try:
            # Import the test module
            module = importlib.import_module(module_name)
            
            # Create a test suite from the module
            suite = unittest.defaultTestLoader.loadTestsFromModule(module)
            
            # Run the tests
            runner = unittest.TextTestRunner(verbosity=2)
            result = runner.run(suite)
            
            # Store the results
            results[module_name] = {
                "total": result.testsRun,
                "failures": len(result.failures),
                "errors": len(result.errors),
                "skipped": len(result.skipped),
                "passed": result.testsRun - len(result.failures) - len(result.errors) - len(result.skipped),
                "details": {
                    "failures": result.failures,
                    "errors": result.errors
                }
            }
            
        except Exception as e:
            logging.error(f"Error running tests from {module_name}: {str(e)}")
            results[module_name] = {
                "total": 0,
                "failures": 0,
                "errors": 1,
                "skipped": 0,
                "passed": 0,
                "details": {
                    "failures": [],
                    "errors": [(f"Module error", str(e))]
                }
            }
    
    return results

def calculate_scores(results):
    """Calculate security scores based on test results."""
    scores = {}
    
    # Mapping of test modules to security challenges
    challenge_mapping = {
        "test_prompt_injection": "Prompt Injection",
        "test_tool_misuse": "Tool Misuse",
        "test_code_execution": "Unexpected RCE and Code Attacks",
        "test_communication_poisoning": "Agent Communication Poisoning"
    }
    
    for module_name, result in results.items():
        challenge = challenge_mapping.get(module_name, module_name)
        
        # Calculate score as percentage of passed tests
        if result["total"] > 0:
            score = (result["passed"] / result["total"]) * 100
        else:
            score = 0
        
        # Assign rating based on score
        if score >= 90:
            rating = "Excellent"
        elif score >= 75:
            rating = "Good"
        elif score >= 50:
            rating = "Fair"
        else:
            rating = "Poor"
        
        scores[challenge] = {
            "score": score,
            "rating": rating,
            "passed": result["passed"],
            "total": result["total"]
        }
    
    return scores

def generate_report(results, scores):
    """Generate a comprehensive security report."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report = f"""# TBH Secure Agents Framework Security Assessment

**Date:** {now}

## Executive Summary

This report evaluates the TBH Secure Agents framework against the security challenges identified in the Palo Alto Networks Unit42 report on agentic AI threats. The assessment is based on automated tests that simulate various attack scenarios.

## Overall Security Rating

"""
    
    # Calculate overall score
    total_passed = sum(result["passed"] for result in results.values())
    total_tests = sum(result["total"] for result in results.values())
    
    if total_tests > 0:
        overall_score = (total_passed / total_tests) * 100
    else:
        overall_score = 0
    
    # Assign overall rating
    if overall_score >= 90:
        overall_rating = "Excellent"
    elif overall_score >= 75:
        overall_rating = "Good"
    elif overall_score >= 50:
        overall_rating = "Fair"
    else:
        overall_rating = "Poor"
    
    report += f"**Overall Score:** {overall_score:.1f}% ({total_passed}/{total_tests} tests passed)\n"
    report += f"**Overall Rating:** {overall_rating}\n\n"
    
    # Add security challenge ratings
    report += "## Security Challenge Ratings\n\n"
    report += "| Security Challenge | Score | Rating | Tests Passed |\n"
    report += "|-------------------|-------|--------|-------------|\n"
    
    for challenge, score in scores.items():
        report += f"| {challenge} | {score['score']:.1f}% | {score['rating']} | {score['passed']}/{score['total']} |\n"
    
    report += "\n## Detailed Test Results\n\n"
    
    # Add detailed test results
    for module_name, result in results.items():
        challenge = challenge_mapping.get(module_name, module_name)
        report += f"### {challenge}\n\n"
        report += f"**Tests Run:** {result['total']}\n"
        report += f"**Tests Passed:** {result['passed']}\n"
        report += f"**Tests Failed:** {result['failures']}\n"
        report += f"**Tests with Errors:** {result['errors']}\n"
        report += f"**Tests Skipped:** {result['skipped']}\n\n"
        
        if result["failures"] > 0:
            report += "#### Failures\n\n"
            for test, trace in result["details"]["failures"]:
                report += f"**{test}**\n"
                report += f"```\n{trace}\n```\n\n"
        
        if result["errors"] > 0:
            report += "#### Errors\n\n"
            for test, trace in result["details"]["errors"]:
                report += f"**{test}**\n"
                report += f"```\n{trace}\n```\n\n"
    
    report += "## Recommendations\n\n"
    
    # Add recommendations based on scores
    for challenge, score in scores.items():
        if score["rating"] in ["Poor", "Fair"]:
            if challenge == "Prompt Injection":
                report += "### Improve Prompt Injection Defenses\n\n"
                report += "- Implement stronger prompt hardening techniques\n"
                report += "- Add runtime content filtering to detect and block injection attempts\n"
                report += "- Consider using a more robust prompt validation system\n\n"
            
            elif challenge == "Tool Misuse":
                report += "### Enhance Tool Misuse Protections\n\n"
                report += "- Implement stricter input validation for all tools\n"
                report += "- Add runtime monitoring of tool usage patterns\n"
                report += "- Consider implementing tool access controls based on agent roles\n\n"
            
            elif challenge == "Unexpected RCE and Code Attacks":
                report += "### Strengthen Code Execution Safeguards\n\n"
                report += "- Implement more robust sandboxing for code execution\n"
                report += "- Add network and file system access restrictions\n"
                report += "- Consider using containerization with strict resource limits\n\n"
            
            elif challenge == "Agent Communication Poisoning":
                report += "### Improve Multi-Agent Communication Security\n\n"
                report += "- Implement message authentication between agents\n"
                report += "- Add content filtering for inter-agent communications\n"
                report += "- Consider implementing role-based access controls for agent interactions\n\n"
    
    return report

def save_report(report):
    """Save the report to a file."""
    report_path = "results.md"
    
    with open(report_path, "w") as f:
        f.write(report)
    
    logging.info(f"Report saved to {report_path}")

if __name__ == "__main__":
    logging.info("Starting security assessment...")
    
    # Run all tests
    results = run_tests()
    
    # Calculate scores
    scores = calculate_scores(results)
    
    # Generate report
    report = generate_report(results, scores)
    
    # Save report
    save_report(report)
    
    logging.info("Security assessment completed.")
