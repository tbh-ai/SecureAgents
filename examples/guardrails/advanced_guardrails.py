#!/usr/bin/env python3
# examples/guardrails/advanced_guardrails.py
# Author: Saish (TBH.AI)

"""
Advanced example demonstrating the use of guardrail inputs with TBH Secure Agents.
This example shows more complex template variables, conditional formatting,
and dynamic content generation based on guardrail inputs.
"""

import os
import sys
import logging
import json

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import the TBH Secure Agents framework
from tbh_secure_agents import Expert, Operation, Squad

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def main():
    """
    Main function demonstrating advanced guardrail features with TBH Secure Agents.
    """
    print("\n" + "="*80)
    print("TBH SECURE AGENTS - ADVANCED GUARDRAILS EXAMPLE".center(80))
    print("="*80 + "\n")

    # Set your API key
    # You can also set this as an environment variable: GOOGLE_API_KEY
    api_key = os.environ.get('GOOGLE_API_KEY')
    if not api_key:
        print("Please set your GOOGLE_API_KEY environment variable.")
        return

    print("Creating experts with template variables in their profiles...\n")

    # Create a content writer expert with template variables
    content_writer = Expert(
        specialty="Content Writer specializing in {content_domain}",
        objective="Create {content_type} content that {objective_detail}",
        background="You have {experience_years} years of experience writing for {target_audience} and excel at creating content that is {tone} and {style}.",
        api_key=api_key
    )

    # Create a data analyst expert with template variables
    data_analyst = Expert(
        specialty="Data Analyst with expertise in {analysis_domain}",
        objective="Analyze {data_type} data and provide {insight_type} insights",
        background="You have experience working with {data_source} data and can present findings in a way that's accessible to {audience_expertise} audiences.",
        api_key=api_key
    )

    # Create a product expert with template variables
    product_expert = Expert(
        specialty="Product Expert for {product_category}",
        objective="Provide detailed information about {product_type} products with a focus on {product_aspect}",
        background="You have deep knowledge of {product_category} products, their features, benefits, and how they compare to alternatives.",
        api_key=api_key
    )

    print("Creating operations with template variables and conditional logic...\n")

    # Create operations with template variables and conditional formatting
    writing_operation = Operation(
        instructions="""
        Write a {content_length} {content_type} about {topic}.
        
        {tone, select, 
          professional:Use a formal, authoritative tone suitable for business contexts.|
          conversational:Use a friendly, approachable tone as if speaking directly to the reader.|
          technical:Use precise technical language appropriate for experts in the field.|
          inspirational:Use motivational language that inspires action and positive feelings.
        }
        
        Target audience: {target_audience}
        
        {include_cta, select,
          true:Include a clear call-to-action at the end.|
          false:No call-to-action is needed.
        }
        
        {include_statistics, select,
          true:Include relevant statistics and data points to support your points.|
          false:Focus on qualitative information rather than statistics.
        }
        """,
        output_format="A well-formatted {content_type} with appropriate sections and formatting",
        expert=content_writer
    )

    analysis_operation = Operation(
        instructions="""
        Analyze the following {data_type} data and create a summary of key insights:
        
        {data}
        
        Focus your analysis on {analysis_focus}.
        
        {chart_type, select,
          none:No visualization description needed.|
          bar:Describe what a bar chart of this data would show.|
          line:Describe what a line chart of this data would show.|
          pie:Describe what a pie chart of this data would show.
        }
        
        {audience_expertise, select,
          technical:Use technical language appropriate for data specialists.|
          executive:Focus on high-level insights suitable for executive decision-makers.|
          general:Explain concepts in simple terms accessible to a general audience.
        }
        
        {include_recommendations, select,
          true:Include 2-3 actionable recommendations based on the data.|
          false:Focus only on insights without recommendations.
        }
        """,
        output_format="A structured analysis with clear sections for insights and recommendations",
        expert=data_analyst
    )

    product_operation = Operation(
        instructions="""
        Create a {detail_level} description of {product_name}, a {product_type} in the {product_category} category.
        
        {focus_area, select,
          features:Focus primarily on the technical features and specifications.|
          benefits:Focus primarily on the benefits and value proposition.|
          comparison:Compare this product with similar alternatives in the market.|
          use_cases:Describe the main use cases and ideal users for this product.
        }
        
        {pricing_info, select,
          include:Include pricing information in your description.|
          exclude:Do not mention pricing information.
        }
        
        {target_audience, select,
          technical:Write for a technical audience familiar with {product_category}.|
          business:Write for business decision-makers evaluating solutions.|
          consumer:Write for everyday consumers considering a purchase.
        }
        """,
        output_format="A comprehensive product description formatted appropriately for the target audience",
        expert=product_expert
    )

    print("Creating a squad with the experts and operations...\n")

    # Create a squad with the experts and operations
    advanced_squad = Squad(
        experts=[content_writer, data_analyst, product_expert],
        operations=[writing_operation, analysis_operation, product_operation],
        process="sequential"  # Operations run in sequence
    )

    print("Defining advanced guardrail inputs...\n")

    # Define complex guardrail inputs
    guardrail_inputs = {
        # Content writer guardrails
        "content_domain": "healthcare technology",
        "content_type": "blog post",
        "content_length": "short (300-400 words)",
        "objective_detail": "educates readers while maintaining their interest",
        "experience_years": "8+",
        "target_audience": "healthcare professionals with limited technical background",
        "tone": "professional",
        "style": "clear and engaging",
        "topic": "The role of AI in improving patient outcomes",
        "include_cta": True,
        "include_statistics": True,
        
        # Data analyst guardrails
        "analysis_domain": "healthcare metrics",
        "data_type": "patient outcome",
        "insight_type": "actionable",
        "data_source": "hospital",
        "audience_expertise": "executive",
        "analysis_focus": "trends in recovery times and readmission rates",
        "chart_type": "line",
        "include_recommendations": True,
        "data": {
            "recovery_times_days": {
                "Traditional treatment": [14, 13, 12, 11, 10],
                "AI-assisted treatment": [12, 10, 8, 7, 6]
            },
            "readmission_rates_percent": {
                "Traditional treatment": [15, 14, 13, 12, 11],
                "AI-assisted treatment": [13, 11, 9, 7, 5]
            },
            "years": [2019, 2020, 2021, 2022, 2023]
        },
        
        # Product expert guardrails
        "product_category": "healthcare AI solutions",
        "product_type": "clinical decision support system",
        "product_aspect": "clinical workflow integration",
        "product_name": "MediAssist AI",
        "detail_level": "comprehensive",
        "focus_area": "benefits",
        "pricing_info": "exclude",
        "target_audience": "business"
    }

    print("Advanced guardrail inputs defined. Here are some key values:")
    print(f"  - Content domain: {guardrail_inputs['content_domain']}")
    print(f"  - Content type: {guardrail_inputs['content_type']}")
    print(f"  - Topic: {guardrail_inputs['topic']}")
    print(f"  - Product: {guardrail_inputs['product_name']}")
    print(f"  - Analysis focus: {guardrail_inputs['analysis_focus']}")

    print("\nDeploying the squad with advanced guardrail inputs...\n")

    # Deploy the squad with the guardrail inputs
    try:
        result = advanced_squad.deploy(guardrails=guardrail_inputs)

        print("\n" + "="*80)
        print("FINAL RESULT".center(80))
        print("="*80 + "\n")
        print(result)
        print("\n" + "="*80)

        # Save the output to a file
        output_file = os.path.join(os.path.dirname(__file__), "advanced_guardrails_output.txt")
        with open(output_file, "w") as f:
            f.write("TBH SECURE AGENTS - ADVANCED GUARDRAILS EXAMPLE\n\n")
            f.write("Guardrail inputs (selected):\n")
            for key in ["content_domain", "content_type", "topic", "product_name", "analysis_focus"]:
                f.write(f"  - {key}: {guardrail_inputs[key]}\n")
            f.write("\nResult:\n\n")
            f.write(result)
        
        print(f"\nOutput saved to {output_file}")

    except Exception as e:
        print(f"Error during squad deployment: {e}")

if __name__ == "__main__":
    main()
