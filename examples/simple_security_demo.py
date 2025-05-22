#!/usr/bin/env python3
"""
Simple Security Validation Demo

This script demonstrates the basic usage of the security validation features
in the TBH Secure Agents framework with minimal complexity.
"""

import os
import sys
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create output directory
os.makedirs("output", exist_ok=True)

# Import the security validator
from tbh_secure_agents.security_validation.security_validator import SecurityValidator

# Create a security validator with HTML report generation
validator = SecurityValidator(
    interactive=True,
    enable_reports=True,
    reports_dir="output",
    enable_recommendations=True
)

# Test inputs - one secure and one insecure
secure_input = "List the files in the current directory"
insecure_input = "rm -rf /tmp/data/*"

# Validate the secure input
print("\n=== Testing Secure Input ===")
print(f"Input: {secure_input}")

is_secure, _ = validator.validate_prompt(
    prompt=secure_input,
    security_level="standard",
    generate_report=True
)

print(f"Validation result: {'Secure' if is_secure else 'Insecure'}")

# Validate the insecure input
print("\n=== Testing Insecure Input ===")
print(f"Input: {insecure_input}")

is_secure, error_details = validator.validate_prompt(
    prompt=insecure_input,
    security_level="standard",
    generate_report=True
)

print(f"Validation result: {'Secure' if is_secure else 'Insecure'}")

if not is_secure and error_details:
    print(f"Error message: {error_details.get('error_message', 'Unknown error')}")
    
    # Show the report path
    if error_details.get("report_path"):
        print(f"Report generated at: {error_details.get('report_path')}")
    
    # Show a snippet of the recommendation
    if error_details.get("recommendation"):
        recommendation = error_details.get("recommendation")
        print("\nRecommendation snippet:")
        print(recommendation[:200] + "..." if len(recommendation) > 200 else recommendation)

print("\nDemo completed successfully!")
