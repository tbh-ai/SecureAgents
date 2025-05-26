#!/usr/bin/env python3
"""
Example 5: AI Financial Advisor
===============================

This example shows how to create an AI financial advisor that provides
investment advice and financial planning recommendations.

Features demonstrated:
- Creating a Financial Advisor expert
- Using guardrails for financial parameters
- Saving to PDF format for professional reports
"""

import os

# Set your Google API key (replace with your actual key)
os.environ["GOOGLE_API_KEY"] = "AIzaSyA3ZxbIXpR3yNkZwGDznrztdQmgnU16DJI"

from tbh_secure_agents import Expert, Operation

def main():
    # Create outputs directory
    os.makedirs("outputs/user_examples", exist_ok=True)
    
    # Create an AI financial advisor expert with template variables
    financial_advisor = Expert(
        specialty="Financial Advisor specializing in {investment_type}",
        objective="Provide {advice_type} financial advice for {client_profile}",
        security_profile="minimal"
    )
    
    # Define guardrails for financial advice
    financial_guardrails = {
        "investment_type": "retirement planning",
        "advice_type": "conservative",
        "client_profile": "young professionals",
        "risk_tolerance": "moderate",
        "time_horizon": "long-term",
        "investment_amount": "regular monthly contributions"
    }
    
    # Create a financial advice operation with template variables
    advice_operation = Operation(
        instructions="Provide {advice_type} {investment_type} advice for {client_profile}. Consider {risk_tolerance} risk tolerance and {time_horizon} investment horizon for {investment_amount}.",
        output_format="Professional financial advisory report in PDF format",
        expert=financial_advisor,
        result_destination="outputs/user_examples/financial_advice.pdf"
    )
    
    # Execute the financial advice
    print("Starting financial advisory session...")
    
    try:
        result = advice_operation.execute(guardrails=financial_guardrails)
        print("Financial advice completed successfully!")
        print(f"Results saved to: {advice_operation.result_destination}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
