#!/usr/bin/env python3
"""
Example script demonstrating security validation with HTML reports.

This script shows how to use the security validation framework with HTML report
generation and LLM-based recommendations.
"""

import os
import sys
import logging
from typing import Dict, Any, List, Optional

from tbh_secure_agents import (
    Expert,
    Operation,
    Squad,
    SecurityValidator,
    SecurityReportGenerator,
    LLMRecommendationGenerator
)
from tbh_secure_agents.security_validation import enable_hybrid_validation

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def example_direct_validation():
    """Example of direct security validation with HTML reports."""
    # Create a security validator
    validator = SecurityValidator(
        interactive=True,
        enable_reports=True,
        reports_dir="security_reports",
        enable_recommendations=True
    )
    
    # Sample input with security issues
    input_text = "rm -rf /tmp/data/*"
    
    # Validate the input
    is_secure, error_details = validator.validate_prompt(
        prompt=input_text,
        security_level="standard",
        generate_report=True,
        open_report=True
    )
    
    # Print validation result
    if is_secure:
        logger.info("Input is secure")
    else:
        logger.info(f"Input is insecure: {error_details['error_message']}")
        
        # Print recommendation if available
        if error_details.get("recommendation"):
            logger.info("\nRecommendation:")
            logger.info(error_details["recommendation"])
        
        # Print report path if available
        if error_details.get("report_path"):
            logger.info(f"\nReport generated at: {error_details['report_path']}")

def example_expert_with_validation():
    """Example of using an Expert with security validation and reports."""
    # Enable hybrid validation with report generation
    enable_hybrid_validation(enable_reports=True, auto_open_reports=True)
    
    # Create an expert
    expert = Expert(
        specialty="Security Analyst",
        objective="Analyze security issues in code",
        security_profile="standard",
        api_key=os.environ.get("GOOGLE_API_KEY")
    )
    
    # Create an operation with potentially insecure content
    operation = Operation(
        instructions="Analyze the security implications of this command: rm -rf /tmp/data/*"
    )
    
    # Execute the operation
    try:
        result = expert.execute_task(operation.instructions)
        logger.info(f"Operation executed successfully")
        logger.info(f"Result: {result[:100]}...")
    except Exception as e:
        logger.error(f"Operation failed: {e}")

def example_squad_with_validation():
    """Example of using a Squad with security validation and reports."""
    # Enable hybrid validation with report generation
    enable_hybrid_validation(enable_reports=True, auto_open_reports=True)
    
    # Create experts
    security_expert = Expert(
        specialty="Security Analyst",
        objective="Analyze security issues in code",
        security_profile="standard",
        api_key=os.environ.get("GOOGLE_API_KEY")
    )
    
    code_expert = Expert(
        specialty="Code Reviewer",
        objective="Review code for best practices",
        security_profile="standard",
        api_key=os.environ.get("GOOGLE_API_KEY")
    )
    
    # Create a squad
    squad = Squad(
        name="Security Review Team",
        experts=[security_expert, code_expert],
        security_profile="standard"
    )
    
    # Create operations
    operations = [
        Operation(
            instructions="Analyze the security implications of this command: rm -rf /tmp/data/*"
        ),
        Operation(
            instructions="Suggest a more secure alternative to the command: rm -rf /tmp/data/*"
        )
    ]
    
    # Execute the operations
    try:
        results = squad.execute_operations(operations)
        logger.info(f"Operations executed successfully")
        for i, result in enumerate(results):
            logger.info(f"Result {i+1}: {result[:100]}...")
    except Exception as e:
        logger.error(f"Operations failed: {e}")

def main():
    """Main function."""
    # Check if API key is set
    if not os.environ.get("GOOGLE_API_KEY"):
        logger.warning("GOOGLE_API_KEY environment variable not set. Some features may not work.")
    
    # Create security reports directory
    os.makedirs("security_reports", exist_ok=True)
    
    # Run examples
    print("\n=== Example 1: Direct Security Validation ===\n")
    example_direct_validation()
    
    print("\n=== Example 2: Expert with Security Validation ===\n")
    example_expert_with_validation()
    
    print("\n=== Example 3: Squad with Security Validation ===\n")
    example_squad_with_validation()

if __name__ == "__main__":
    main()
