#!/usr/bin/env python3
"""
Example 4: AI Marketing Strategist
==================================

This example shows how to create an AI marketing strategist that creates
marketing campaigns and strategies for different products.

Features demonstrated:
- Creating a Marketing Strategist expert
- Using guardrails for campaign parameters
- Saving to HTML format for presentations
"""

import os

# Set your Google API key (replace with your actual key)
os.environ["GOOGLE_API_KEY"] = "AIzaSyA3ZxbIXpR3yNkZwGDznrztdQmgnU16DJI"

from tbh_secure_agents import Expert, Operation

def main():
    # Create outputs directory
    os.makedirs("outputs/user_examples", exist_ok=True)
    
    # Create an AI marketing strategist expert with template variables
    marketing_strategist = Expert(
        specialty="Marketing Strategist specializing in {product_category}",
        objective="Create effective {campaign_type} campaigns for {target_market}",
        security_profile="minimal"
    )
    
    # Define guardrails for marketing strategy
    marketing_guardrails = {
        "product_category": "sustainable technology",
        "campaign_type": "digital marketing",
        "target_market": "environmentally conscious consumers",
        "budget_range": "mid-tier",
        "campaign_duration": "3 months",
        "primary_channels": "social media and content marketing"
    }
    
    # Create a marketing strategy operation with template variables
    strategy_operation = Operation(
        instructions="Create a comprehensive {campaign_type} strategy for {product_category} targeting {target_market}. Plan for {campaign_duration} with {budget_range} budget using {primary_channels}.",
        output_format="Professional marketing strategy presentation in HTML format",
        expert=marketing_strategist,
        result_destination="outputs/user_examples/marketing_strategy.html"
    )
    
    # Execute the marketing strategy
    print("Starting marketing strategy development...")
    
    try:
        result = strategy_operation.execute(guardrails=marketing_guardrails)
        print("Marketing strategy completed successfully!")
        print(f"Results saved to: {strategy_operation.result_destination}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
