#!/usr/bin/env python3
"""
Simple test script for the integrated security validation features.
"""

import os
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def test_security_validator():
    """Test the SecurityValidator class."""
    from tbh_secure_agents.security_validation import SecurityValidator
    
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
        
        # Print report path if available
        if error_details.get("report_path"):
            logger.info(f"\nReport generated at: {error_details['report_path']}")

def main():
    """Main function."""
    # Create security reports directory
    os.makedirs("security_reports", exist_ok=True)
    
    # Run test
    test_security_validator()

if __name__ == "__main__":
    main()
