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

    # Create an AI data analyst expert
    data_analyst = Expert(
        specialty="Data Analyst",
        objective="Analyze data trends and provide actionable insights",
        security_profile="minimal"
    )

    # Define guardrails for data analysis
    analysis_guardrails = {
        "no_personal_info": True,
        "data_privacy": True,
        "factual_content": True,
        "professional_tone": True,
        "analysis_period": "last 12 months",
        "focus_metrics": "growth trends and patterns",
        "include_recommendations": True,
        "data_format": "structured analysis",
        "confidence_level": "high"
    }

    # Create a data analysis operation for CSV
    csv_analysis = Operation(
        instructions="Analyze e-commerce sales trends and create a summary with key metrics, growth patterns, and recommendations.",
        output_format="Structured data analysis suitable for CSV format with clear categories",
        expert=data_analyst,
        result_destination="outputs/user_examples/sales_analysis.csv"
    )

    # Create a data analysis operation for JSON
    json_analysis = Operation(
        instructions="Create a market analysis report for the renewable energy sector with key statistics and growth projections.",
        output_format="Structured analysis data in JSON format with metrics and insights",
        expert=data_analyst,
        result_destination="outputs/user_examples/market_analysis.json"
    )

    # Execute the CSV analysis
    print("📊 Starting AI data analysis...")
    print("Analysis 1: E-commerce Sales Trends")
    print("Output: outputs/user_examples/sales_analysis.csv")
    print()

    try:
        result1 = csv_analysis.execute(guardrails=analysis_guardrails)
        print("✅ Sales analysis completed!")
        print(f"📄 Results saved to: {csv_analysis.result_destination}")
        print()

        # Execute the JSON analysis
        print("Analysis 2: Renewable Energy Market")
        print("Output: outputs/user_examples/market_analysis.json")
        print()

        result2 = json_analysis.execute(guardrails=analysis_guardrails)
        print("✅ Market analysis completed!")
        print(f"📄 Results saved to: {json_analysis.result_destination}")
        print()

        print("Preview of sales analysis:")
        print("-" * 50)
        print(result1[:300] + "..." if len(result1) > 300 else result1)

    except Exception as e:
        print(f"❌ Error during analysis: {e}")

if __name__ == "__main__":
    main()
