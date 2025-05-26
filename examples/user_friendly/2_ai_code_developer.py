#!/usr/bin/env python3
"""
Example 2: AI Code Developer
============================

This example shows how to create an AI code developer that writes
code with specific requirements using guardrails.

Features demonstrated:
- Creating a Code Developer expert
- Using guardrails for code requirements
- Saving to Python file format
"""

import os

# Set your Google API key (replace with your actual key)
os.environ["GOOGLE_API_KEY"] = "AIzaSyA3ZxbIXpR3yNkZwGDznrztdQmgnU16DJI"

from tbh_secure_agents import Expert, Operation

def main():
    # Create outputs directory
    os.makedirs("outputs/user_examples", exist_ok=True)
    
    # Create an AI code developer expert with template variables
    code_developer = Expert(
        specialty="Software Developer specializing in {programming_language}",
        objective="Write clean, efficient {code_type} code following {coding_standards}",
        security_profile="minimal"
    )
    
    # Define guardrails for code development
    code_guardrails = {
        "programming_language": "Python",
        "code_type": "web application",
        "coding_standards": "PEP 8",
        "include_comments": True,
        "include_error_handling": True,
        "complexity_level": "beginner-friendly"
    }
    
    # Create a code development operation with template variables
    code_operation = Operation(
        instructions="Write a simple {code_type} in {programming_language}. Follow {coding_standards} standards. Make it {complexity_level} with proper comments and error handling.",
        output_format="Clean, well-documented {programming_language} code",
        expert=code_developer,
        result_destination="outputs/user_examples/simple_web_app.py"
    )
    
    # Execute the code development
    print("Starting code development...")
    
    try:
        result = code_operation.execute(guardrails=code_guardrails)
        print("Code development completed successfully!")
        print(f"Results saved to: {code_operation.result_destination}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
