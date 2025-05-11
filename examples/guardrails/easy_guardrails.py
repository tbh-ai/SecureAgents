#!/usr/bin/env python3
# examples/guardrails/easy_guardrails.py
# Author: Saish (TBH.AI)

"""
Easy example demonstrating basic guardrails with TBH Secure Agents.
This example shows simple template variables and basic guardrail usage.
"""

import os
import sys
import logging

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import the TBH Secure Agents framework
from tbh_secure_agents import Expert, Operation, Squad

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def main():
    """
    Main function demonstrating basic guardrails with TBH Secure Agents.
    """
    print("\n" + "="*80)
    print("TBH SECURE AGENTS - EASY GUARDRAILS EXAMPLE".center(80))
    print("="*80 + "\n")

    # Set your API key
    # You can also set this as an environment variable: GOOGLE_API_KEY
    api_key = os.environ.get('GOOGLE_API_KEY')
    if not api_key:
        print("Please set your GOOGLE_API_KEY environment variable.")
        return

    print("Creating a weather expert with template variables...\n")

    # Create a weather expert with template variables
    weather_expert = Expert(
        specialty="Weather Forecaster",
        objective="Provide accurate and helpful weather information for {location}",
        background="You are an experienced meteorologist who specializes in providing clear and concise weather forecasts.",
        api_key=api_key
    )

    print("Creating a weather forecast operation with template variables...\n")

    # Create a weather forecast operation with template variables
    weather_operation = Operation(
        instructions="""
        Create a weather forecast for {location} for {time_period}.
        
        Include information about:
        - Temperature (high and low)
        - Precipitation chance
        - Wind conditions
        - General weather outlook
        
        {include_activities, select,
          true:Suggest appropriate outdoor activities based on the weather conditions.|
          false:Do not include activity suggestions.
        }
        """,
        output_format="A clear and concise weather forecast",
        expert=weather_expert
    )

    print("Creating a squad with the weather expert and operation...\n")

    # Create a squad with the weather expert and operation
    weather_squad = Squad(
        experts=[weather_expert],
        operations=[weather_operation],
        process="sequential"
    )

    print("Defining guardrail inputs...\n")

    # Define guardrail inputs
    guardrail_inputs = {
        "location": "Seattle, Washington",
        "time_period": "the next 3 days",
        "include_activities": True
    }

    print("Guardrail inputs defined:")
    for key, value in guardrail_inputs.items():
        print(f"  - {key}: {value}")

    print("\nDeploying the squad with guardrail inputs...\n")

    # Deploy the squad with the guardrail inputs
    try:
        result = weather_squad.deploy(guardrails=guardrail_inputs)

        print("\n" + "="*80)
        print("FINAL RESULT".center(80))
        print("="*80 + "\n")
        print(result)
        print("\n" + "="*80)

        # Save the output to a file
        output_file = os.path.join(os.path.dirname(__file__), "easy_guardrails_output.txt")
        with open(output_file, "w") as f:
            f.write("TBH SECURE AGENTS - EASY GUARDRAILS EXAMPLE\n\n")
            f.write("Guardrail inputs:\n")
            for key, value in guardrail_inputs.items():
                f.write(f"  - {key}: {value}\n")
            f.write("\nResult:\n\n")
            f.write(result)
        
        print(f"\nOutput saved to {output_file}")

    except Exception as e:
        print(f"Error during squad deployment: {e}")

if __name__ == "__main__":
    main()
