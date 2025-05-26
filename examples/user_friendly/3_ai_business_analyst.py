#!/usr/bin/env python3
"""
Example 3: AI Business Analyst
==============================

This example shows how to create an AI business analyst that analyzes
business problems and creates strategic recommendations.

Features demonstrated:
- Creating a Business Analyst expert
- Using guardrails for business analysis
- Saving to JSON format
"""

import os

# Set your Google API key (replace with your actual key)
os.environ["GOOGLE_API_KEY"] = "AIzaSyA3ZxbIXpR3yNkZwGDznrztdQmgnU16DJI"

from tbh_secure_agents import Expert, Operation

def main():
    # Create outputs directory
    os.makedirs("outputs/user_examples", exist_ok=True)
    
    # Create an AI business analyst expert with template variables
    business_analyst = Expert(
        specialty="Business Analyst specializing in {industry} sector",
        objective="Analyze {business_problem} and provide {analysis_type} recommendations",
        security_profile="minimal"
    )
    
    # Define guardrails for business analysis
    business_guardrails = {
        "industry": "e-commerce",
        "business_problem": "declining customer retention",
        "analysis_type": "strategic",
        "timeframe": "next 6 months",
        "budget_consideration": "cost-effective solutions",
        "stakeholders": "management team"
    }
    
    # Create a business analysis operation with template variables
    analysis_operation = Operation(
        instructions="Analyze the {business_problem} in the {industry} industry. Provide {analysis_type} recommendations for the {timeframe}. Focus on {budget_consideration} for {stakeholders}.",
        output_format="Strategic business analysis with actionable recommendations in JSON format",
        expert=business_analyst,
        result_destination="outputs/user_examples/business_analysis.json"
    )
    
    # Execute the business analysis
    print("Starting business analysis...")
    
    try:
        result = analysis_operation.execute(guardrails=business_guardrails)
        print("Business analysis completed successfully!")
        print(f"Results saved to: {analysis_operation.result_destination}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
