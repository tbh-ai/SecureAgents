#!/usr/bin/env python3
"""
Test script for the hybrid security validation system.

This script demonstrates how to use the hybrid security validation system
with the TBH Secure Agents framework.
"""

import os
import sys
import logging
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Create output directory
OUTPUT_DIR = os.path.join(os.getcwd(), "validation_output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def test_direct_validation():
    """Test direct security validation."""
    try:
        # Import the security validator
        from tbh_secure_agents.security_validation.security_validator import SecurityValidator
        
        # Create a security validator
        validator = SecurityValidator(
            interactive=True,
            enable_reports=True,
            reports_dir=OUTPUT_DIR,
            enable_recommendations=True
        )
        
        # Sample input with security issues
        input_text = "rm -rf /tmp/data/*"
        
        logger.info(f"Testing security validation with input: {input_text}")
        
        # Validate the input
        is_secure, error_details = validator.validate_prompt(
            prompt=input_text,
            security_level="standard",
            generate_report=True,
            open_report=False
        )
        
        # Print validation result
        if is_secure:
            logger.info("Input is secure")
        else:
            logger.info(f"Input failed security validation: {error_details['error_message']}")
            
            # Print report path if available
            if error_details.get("report_path"):
                logger.info(f"Security report generated at: {error_details['report_path']}")
            
            # Print recommendation if available
            if error_details.get("recommendation"):
                logger.info("\nSecurity recommendation:")
                logger.info(error_details["recommendation"])
                
        return True
    except ImportError as e:
        logger.error(f"Import error: {e}")
        return False
    except Exception as e:
        logger.error(f"Error testing direct validation: {e}")
        return False

def test_hybrid_validation_integration():
    """Test hybrid validation integration with the framework."""
    try:
        # Import the framework
        from tbh_secure_agents.agent import Expert
        from tbh_secure_agents.task import Operation
        from tbh_secure_agents.crew import Squad
        from tbh_secure_agents.security_validation.integration import enable_hybrid_validation
        
        # Enable hybrid validation
        enable_hybrid_validation(enable_reports=True, auto_open_reports=False)
        logger.info("Enabled hybrid security validation")
        
        # Create an expert
        security_expert = Expert(
            specialty="Security Analyst",
            objective="Analyze security implications and vulnerabilities",
            security_profile="high"
        )
        logger.info("Created security expert")
        
        # Create an operation with potentially insecure content
        operation = Operation(
            instructions="Analyze the security implications of this command: rm -rf /tmp/data/*",
            result_destination=os.path.join(OUTPUT_DIR, "security_analysis.md")
        )
        operation.expert = security_expert
        logger.info("Created operation with result destination")
        
        # Create a squad
        squad = Squad(
            name="Security Analysis Team",
            experts=[security_expert],
            operations=[operation],
            security_profile="standard",
            process="sequential",
            result_destination={
                "format": "md",
                "file_path": os.path.join(OUTPUT_DIR, "squad_result.md")
            }
        )
        logger.info("Created squad with result destination")
        
        # Deploy the squad
        logger.info("Deploying squad...")
        try:
            squad.deploy()
            logger.info("Squad deployed successfully")
            
            # List the created files
            logger.info("\nCreated Files:")
            for file_path in os.listdir(OUTPUT_DIR):
                if file_path.endswith(".md") or file_path.endswith(".html"):
                    full_path = os.path.join(OUTPUT_DIR, file_path)
                    if os.path.isfile(full_path):
                        file_size = os.path.getsize(full_path)
                        logger.info(f"- {file_path} ({file_size} bytes)")
        except Exception as e:
            logger.error(f"Error deploying squad: {e}")
        
        return True
    except ImportError as e:
        logger.error(f"Import error: {e}")
        return False
    except Exception as e:
        logger.error(f"Error testing hybrid validation integration: {e}")
        return False

def main():
    """Main function."""
    # Get API key from environment variable
    api_key = os.environ.get("GOOGLE_API_KEY")
    
    if not api_key:
        logger.warning("GOOGLE_API_KEY environment variable not set. Some features may not work.")
    
    # Test direct validation
    logger.info("=== Testing Direct Security Validation ===")
    direct_validation_success = test_direct_validation()
    
    # Test hybrid validation integration
    logger.info("\n=== Testing Hybrid Validation Integration ===")
    hybrid_validation_success = test_hybrid_validation_integration()
    
    # Print summary
    logger.info("\n=== Test Summary ===")
    logger.info(f"Direct Validation: {'Success' if direct_validation_success else 'Failed'}")
    logger.info(f"Hybrid Validation Integration: {'Success' if hybrid_validation_success else 'Failed'}")
    
    if direct_validation_success and hybrid_validation_success:
        logger.info("\nAll tests passed! The hybrid security validation system is working correctly.")
    else:
        logger.warning("\nSome tests failed. Check the logs for details.")

if __name__ == "__main__":
    main()
