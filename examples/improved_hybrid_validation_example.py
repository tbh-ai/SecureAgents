#!/usr/bin/env python3
"""
Improved Hybrid Validation Example

This example demonstrates how to use the improved hybrid validation system
with the TBH Secure Agents framework.
"""

import os
import logging
from tbh_secure_agents import Expert, Operation, Squad
from tbh_secure_agents.security_validation import enable_improved_hybrid_validation

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set the API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyA3ZxbIXpR3yNkZwGDznrztdQmgnU16DJI"

# Create output directory
os.makedirs("improved_validation_output", exist_ok=True)

def main():
    """Main function."""
    # Enable the improved hybrid validation system
    enable_improved_hybrid_validation(
        api_key=os.environ.get("GOOGLE_API_KEY"),
        use_parallel=True,
        enable_reports=True,
        auto_open_reports=True,
        reports_dir="improved_validation_output/reports",
        recommendation_style="detailed",
        include_code_examples=True
    )
    
    logger.info("Enabled improved hybrid validation system")
    
    # Test with different security profiles
    test_security_profiles()
    
def test_security_profiles():
    """Test the improved hybrid validation with different security profiles."""
    # Define a potentially risky operation
    risky_operation = """
    Write a Python script that:
    1. Lists all files in the current directory
    2. Creates a backup of important files
    3. Deletes temporary files
    
    Include the actual system commands in your response.
    """
    
    # Test with different security profiles
    security_profiles = ["minimal", "low", "standard", "high", "maximum"]
    
    for profile in security_profiles:
        logger.info(f"\n=== Testing {profile.upper()} security profile ===")
        
        # Create an expert with the specified security profile
        expert = Expert(
            specialty="Security Tester",
            objective="Test security profiles",
            security_profile=profile
        )
        
        # Create an operation
        operation = Operation(
            instructions=risky_operation,
            result_destination=f"improved_validation_output/{profile}_result.md"
        )
        
        try:
            # Execute the operation
            result = expert.execute_task(operation.instructions)
            logger.info(f"Operation executed successfully with {profile} profile")
            
            # Save the result
            with open(f"improved_validation_output/{profile}_result.md", "w") as f:
                f.write(result)
            
            logger.info(f"Result saved to: improved_validation_output/{profile}_result.md")
        except Exception as e:
            logger.error(f"Operation failed with {profile} profile: {e}")
            
            # Save the error message
            with open(f"improved_validation_output/{profile}_result.md", "w") as f:
                f.write(f"Error: {str(e)}")
            
            logger.info(f"Error saved to: improved_validation_output/{profile}_result.md")

if __name__ == "__main__":
    main()
