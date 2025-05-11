#!/usr/bin/env python3
# examples/guardrails/medium_guardrails.py
# Author: Saish (TBH.AI)

"""
Medium example demonstrating more complex guardrails with TBH Secure Agents.
This example shows multiple experts, conditional formatting, and more complex template variables.
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
    Main function demonstrating medium complexity guardrails with TBH Secure Agents.
    """
    print("\n" + "="*80)
    print("TBH SECURE AGENTS - MEDIUM GUARDRAILS EXAMPLE".center(80))
    print("="*80 + "\n")

    # Set your API key
    # You can also set this as an environment variable: GOOGLE_API_KEY
    api_key = os.environ.get('GOOGLE_API_KEY')
    if not api_key:
        print("Please set your GOOGLE_API_KEY environment variable.")
        return

    print("Creating experts with template variables...\n")

    # Create a travel guide expert with template variables
    travel_expert = Expert(
        specialty="Travel Guide specializing in {destination_type} destinations",
        objective="Create engaging travel guides for {traveler_type} travelers",
        background="You have extensive knowledge of global destinations and travel planning with a focus on {travel_focus}.",
        api_key=api_key
    )

    # Create a food expert with template variables
    food_expert = Expert(
        specialty="Food Expert specializing in {cuisine_type} cuisine",
        objective="Provide culinary recommendations and insights for {destination}",
        background="You have deep knowledge of local cuisines, dining customs, and food experiences around the world.",
        api_key=api_key
    )

    print("Creating operations with template variables and conditional formatting...\n")

    # Create a destination guide operation with template variables
    destination_operation = Operation(
        instructions="""
        Create a travel guide for {destination} focused on a {trip_duration} trip.
        
        {traveler_type, select,
          family:Focus on family-friendly activities, accommodations, and considerations for traveling with children.|
          solo:Focus on solo traveler experiences, safety tips, and opportunities to meet other travelers.|
          couple:Focus on romantic experiences, intimate settings, and couple-friendly activities.|
          group:Focus on group-friendly activities, accommodations that can handle larger parties, and group dining options.
        }
        
        {budget_level, select,
          budget:Emphasize affordable options, budget accommodations, and free or low-cost activities.|
          mid-range:Focus on moderate pricing with good value, mid-range hotels, and a mix of free and paid activities.|
          luxury:Highlight premium experiences, luxury accommodations, and exclusive activities regardless of cost.
        }
        
        Include information about:
        - Best time to visit
        - Top {attraction_count} attractions
        - Transportation options
        - Accommodation recommendations
        
        {include_safety_tips, select,
          true:Include a section on safety considerations and tips specific to this destination.|
          false:No safety section is needed.
        }
        """,
        output_format="A comprehensive travel guide for {destination}",
        expert=travel_expert
    )

    # Create a food guide operation with template variables
    food_operation = Operation(
        instructions="""
        Create a food guide for {destination} highlighting the local cuisine and dining experiences.
        
        {cuisine_focus, select,
          traditional:Focus on authentic, traditional dishes and dining experiences that showcase local culture.|
          modern:Highlight contemporary dining, fusion cuisine, and modern interpretations of traditional dishes.|
          street_food:Emphasize street food, markets, and casual local eateries.|
          fine_dining:Focus on high-end restaurants, chef specialties, and gourmet experiences.
        }
        
        Include:
        - {dish_count} must-try local dishes
        - Recommended dining areas or districts
        - Local dining customs or etiquette
        
        {dietary_restrictions, select,
          none:No specific dietary focus needed.|
          vegetarian:Include options for vegetarian travelers.|
          vegan:Highlight vegan-friendly options and adaptations of local cuisine.|
          gluten_free:Include guidance for gluten-free dining in this destination.
        }
        
        {include_price_guide, select,
          true:Include a price guide with approximate costs for budget, mid-range, and high-end dining.|
          false:No price guide is needed.
        }
        """,
        output_format="A culinary guide to {destination}",
        expert=food_expert
    )

    print("Creating a squad with the experts and operations...\n")

    # Create a squad with the experts and operations
    travel_squad = Squad(
        experts=[travel_expert, food_expert],
        operations=[destination_operation, food_operation],
        process="sequential"  # Operations run in sequence
    )

    print("Defining guardrail inputs...\n")

    # Define guardrail inputs
    guardrail_inputs = {
        # Travel expert guardrails
        "destination_type": "cultural",
        "traveler_type": "family",
        "travel_focus": "cultural experiences and historical sites",
        
        # Food expert guardrails
        "cuisine_type": "Mediterranean",
        
        # Destination operation guardrails
        "destination": "Barcelona, Spain",
        "trip_duration": "5-day",
        "budget_level": "mid-range",
        "attraction_count": 10,
        "include_safety_tips": True,
        
        # Food operation guardrails
        "cuisine_focus": "traditional",
        "dish_count": 8,
        "dietary_restrictions": "vegetarian",
        "include_price_guide": True
    }

    print("Guardrail inputs defined. Here are some key values:")
    print(f"  - Destination: {guardrail_inputs['destination']}")
    print(f"  - Traveler type: {guardrail_inputs['traveler_type']}")
    print(f"  - Trip duration: {guardrail_inputs['trip_duration']}")
    print(f"  - Budget level: {guardrail_inputs['budget_level']}")
    print(f"  - Cuisine focus: {guardrail_inputs['cuisine_focus']}")

    print("\nDeploying the squad with guardrail inputs...\n")

    # Deploy the squad with the guardrail inputs
    try:
        result = travel_squad.deploy(guardrails=guardrail_inputs)

        print("\n" + "="*80)
        print("FINAL RESULT".center(80))
        print("="*80 + "\n")
        print(result)
        print("\n" + "="*80)

        # Save the output to a file
        output_file = os.path.join(os.path.dirname(__file__), "medium_guardrails_output.txt")
        with open(output_file, "w") as f:
            f.write("TBH SECURE AGENTS - MEDIUM GUARDRAILS EXAMPLE\n\n")
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
