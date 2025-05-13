#!/usr/bin/env python3
"""
Comprehensive Demo of TBH Secure Agents Framework

This example demonstrates a realistic use case that showcases multiple features:
- Terminal UI
- Result destination (saving results to files)
- Security profiles (standard and custom)
- Performance optimization with caching
- Guardrails for dynamic inputs
- Multi-expert collaboration

The scenario is a data analysis pipeline that:
1. Extracts information from a dataset
2. Analyzes the data for insights
3. Generates a report with recommendations
"""

import os
import sys
import time
import logging
import json
from typing import Dict, Any, List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

# Import the TBH Secure Agents framework
from tbh_secure_agents import Expert, Operation, Squad
from tbh_secure_agents.security_profiles import (
    register_custom_profile, list_custom_profiles, get_custom_profile, clear_caches
)

# Get API key from environment variable or use a default one for testing
API_KEY = os.environ.get("GOOGLE_API_KEY", "")

# Sample data for demonstration
SAMPLE_DATA = """
Product Sales Data (Q1 2023):
Product A: 1250 units, $62,500 revenue, $45 cost per unit
Product B: 850 units, $76,500 revenue, $65 cost per unit
Product C: 1500 units, $45,000 revenue, $20 cost per unit
Product D: 300 units, $90,000 revenue, $200 cost per unit

Customer Demographics:
Age 18-24: 15% of customers
Age 25-34: 32% of customers
Age 35-44: 28% of customers
Age 45-54: 18% of customers
Age 55+: 7% of customers

Geographic Distribution:
North America: 45%
Europe: 30%
Asia: 15%
Rest of World: 10%
"""

def register_data_analysis_profile():
    """Register a custom security profile for data analysis."""
    return register_custom_profile(
        name="data_analysis",
        thresholds={
            "injection_score": 0.5,       # Moderate injection detection
            "sensitive_data": 0.4,        # Moderate sensitive data detection
            "relevance_score": 0.6,       # Moderate relevance check
            "reliability_score": 0.7,     # Strict reliability check
            "consistency_score": 0.7,     # Strict consistency check
        },
        checks={
            "critical_exploits": True,    # Check for critical exploits
            "system_commands": True,      # Check for system commands
            "content_analysis": True,     # Perform content analysis
            "format_validation": True,    # Perform format validation
            "context_validation": True,   # Perform context validation
            "output_validation": True,    # Perform output validation
            "expert_validation": False,   # Skip expert validation for this demo
        },
        description="Custom security profile for data analysis applications with balanced security"
    )

def create_data_extraction_expert():
    """Create an expert for data extraction."""
    return Expert(
        specialty="Data Extraction Specialist",
        objective="Extract structured data from raw inputs",
        background="Expert in data parsing and extraction",
        security_profile="data_analysis",  # Use our custom profile
        api_key=API_KEY
    )

def create_data_analysis_expert():
    """Create an expert for data analysis."""
    return Expert(
        specialty="Data Analyst",
        objective="Analyze data for insights and patterns",
        background="Expert in statistical analysis and data interpretation",
        security_profile="high",  # Use a standard high security profile
        api_key=API_KEY
    )

def create_report_generation_expert():
    """Create an expert for report generation."""
    return Expert(
        specialty="Report Writer",
        objective="Generate clear, concise reports with actionable recommendations",
        background="Expert in business communication and data visualization",
        security_profile="standard",  # Use the standard security profile
        api_key=API_KEY
    )

def create_data_extraction_operation(data):
    """Create an operation for data extraction."""
    return Operation(
        instructions=f"""
        Extract the following information from the provided data and format it as JSON:
        1. Sales data for each product (units sold, revenue, cost per unit)
        2. Customer demographics (age groups and percentages)
        3. Geographic distribution (regions and percentages)

        Raw data:
        {data}

        Format the output as valid JSON with appropriate keys and values.
        """,
        context="This is the first step in our data analysis pipeline."
    )

def create_data_analysis_operation():
    """Create an operation for data analysis."""
    return Operation(
        instructions="""
        Analyze the extracted data to identify:
        1. The most profitable product (highest profit margin)
        2. The least profitable product (lowest profit margin)
        3. Calculate the profit margin for each product
        4. Identify the largest customer demographic
        5. Identify the largest geographic market

        Provide your analysis in a structured format with clear sections.
        """,
        context="This operation uses the output from the data extraction step."
    )

def create_report_generation_operation():
    """Create an operation for report generation."""
    return Operation(
        instructions="""
        Generate a comprehensive business report based on the data analysis.
        Include:
        1. Executive summary
        2. Key findings
        3. Product performance analysis
        4. Customer insights
        5. Geographic market analysis
        6. Recommendations for improving profitability

        Format the report in a professional manner with clear sections and headings.
        """,
        context="This is the final step that produces the report for stakeholders."
    )

def run_data_analysis_pipeline(data, output_format="markdown"):
    """
    Run the complete data analysis pipeline.

    Args:
        data: The raw data to analyze
        output_format: The format for the final report (markdown, json, html, or txt)

    Returns:
        The final report
    """
    print("Starting Data Analysis Pipeline")
    print("=" * 50)

    # Register our custom security profile
    register_data_analysis_profile()
    print("Registered custom 'data_analysis' security profile")

    # Create experts
    extraction_expert = create_data_extraction_expert()
    analysis_expert = create_data_analysis_expert()
    report_expert = create_report_generation_expert()
    print("Created specialized experts for each stage of the pipeline")

    # Create operations
    extraction_operation = create_data_extraction_operation(data)
    analysis_operation = create_data_analysis_operation()
    report_operation = create_report_generation_operation()

    # Assign experts to operations
    extraction_operation.expert = extraction_expert
    analysis_operation.expert = analysis_expert
    report_operation.expert = report_expert

    # Create guardrails for dynamic inputs
    guardrails = {
        "company_name": "TechCorp Inc.",
        "quarter": "Q1 2023",
        "analysis_focus": "profitability",
        "include_charts": False
    }

    # Measure execution time to demonstrate performance
    start_time = time.time()

    # Create and deploy the squad
    squad = Squad(
        experts=[extraction_expert, analysis_expert, report_expert],
        operations=[extraction_operation, analysis_operation, report_operation],
        process="sequential",  # Process operations in sequence
        security_level="data_analysis",  # Use our custom security profile
        result_destination={
            "format": output_format,
            "file_path": f"output/data_analysis_report.{output_format}"
        }
    )

    # Deploy the squad with guardrails
    result = squad.deploy(guardrails=guardrails)

    # Calculate execution time
    execution_time = time.time() - start_time

    print(f"\nData analysis pipeline completed in {execution_time:.2f} seconds")
    print(f"Results saved to output/data_analysis_report.{output_format}")

    # Clear caches to free memory
    clear_caches()
    print("Performance optimization: Caches cleared")

    return result

def main():
    """Run the comprehensive demo."""
    # Create output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)

    # Run the data analysis pipeline with different output formats
    formats = ["markdown", "json", "html", "txt"]

    for output_format in formats:
        print(f"\n\nRunning pipeline with {output_format.upper()} output format")
        print("-" * 50)

        try:
            result = run_data_analysis_pipeline(SAMPLE_DATA, output_format)
            print(f"\nSuccessfully generated {output_format.upper()} report")
        except Exception as e:
            print(f"Error generating {output_format.upper()} report: {e}")

    print("\n\nComprehensive Demo Completed")
    print("=" * 50)
    print("Features demonstrated:")
    print("1. Terminal UI - You saw the interactive terminal output")
    print("2. Result Destination - Reports saved in multiple formats")
    print("3. Security Profiles - Used standard and custom security profiles")
    print("4. Performance Optimization - Used caching for improved performance")
    print("5. Guardrails - Used dynamic inputs for report generation")
    print("6. Multi-Expert Collaboration - Used specialized experts for each task")

if __name__ == "__main__":
    main()
