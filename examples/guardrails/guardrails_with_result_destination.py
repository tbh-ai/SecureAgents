"""
Example demonstrating the use of guardrails with manual result saving.

This example shows how to use guardrails to dynamically control expert behavior
and save the results to different file formats manually.
"""

import os
import logging
import json
import csv
from tbh_secure_agents import Expert, Operation, Squad

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Get API key from environment variable
api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("Please set the GOOGLE_API_KEY environment variable")

# Create output directory if it doesn't exist
os.makedirs("examples/guardrails/outputs", exist_ok=True)

# Create a weather forecaster expert
weather_expert = Expert(
    specialty="Weather Forecaster",
    objective="Provide accurate weather forecasts for {location}",
    backstory="You are a professional meteorologist with years of experience in weather prediction.",
    api_key=api_key
)

# Create operations with different output formats

# Text format (.txt)
txt_operation = Operation(
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

# Markdown format (.md)
md_operation = Operation(
    instructions="""
    Create a detailed weather report for {location} for {time_period}.

    Include information about:
    - Temperature (high and low)
    - Precipitation chance
    - Wind conditions
    - General weather outlook
    - Humidity levels
    - UV index

    Format the report with proper markdown headings, lists, and emphasis.

    {include_activities, select,
      true:Suggest appropriate outdoor activities based on the weather conditions.|
      false:Do not include activity suggestions.
    }
    """,
    output_format="A well-formatted markdown report",
    expert=weather_expert
)

# CSV format (.csv)
csv_operation = Operation(
    instructions="""
    Create a weather forecast for {location} for {time_period} in a tabular format.

    For each day, provide:
    - Date
    - High temperature
    - Low temperature
    - Precipitation chance (%)
    - Wind speed
    - Weather condition (e.g., Sunny, Cloudy, Rainy)

    Format your response as a CSV table with headers.
    """,
    output_format="A CSV table with weather data",
    expert=weather_expert
)

# JSON format (.json)
json_operation = Operation(
    instructions="""
    Create a weather forecast for {location} for {time_period} in JSON format.

    For each day, include:
    - date
    - high_temp
    - low_temp
    - precipitation_chance
    - wind_speed
    - weather_condition
    - humidity

    {include_activities, select,
      true:For each day, also include a "recommended_activities" array with at least 2 suggested activities.|
      false:Do not include activity suggestions.
    }

    Format your response as a valid JSON object.
    """,
    output_format="A JSON object with weather data",
    expert=weather_expert
)

# HTML format (.html)
html_operation = Operation(
    instructions="""
    Create a weather forecast webpage for {location} for {time_period}.

    Include:
    - A title with the location and time period
    - A summary of the overall weather pattern
    - A day-by-day breakdown with:
      - Temperature (high and low)
      - Precipitation chance
      - Wind conditions
      - Weather icon description (e.g., "Sunny", "Partly Cloudy")

    {include_activities, select,
      true:Include a section with recommended activities for each day based on the weather.|
      false:Do not include activity suggestions.
    }

    Format your response as HTML with appropriate tags, headings, and styling.
    """,
    output_format="An HTML webpage with weather forecast",
    expert=weather_expert
)

# PDF format (.pdf) - Note: This requires reportlab package
pdf_operation = Operation(
    instructions="""
    Create a professional weather report for {location} for {time_period}.

    Include:
    - An executive summary of the weather outlook
    - Detailed daily forecasts with:
      - Temperature (high and low)
      - Precipitation chance
      - Wind conditions
      - Humidity and pressure
      - UV index
    - Weather alerts or warnings if applicable

    {include_activities, select,
      true:Include a section with recommended activities for each day based on the weather.|
      false:Do not include activity suggestions.
    }

    Format your response as a professional report suitable for PDF conversion.
    """,
    output_format="A professional weather report",
    expert=weather_expert
)

# Define file paths for saving results
file_paths = {
    "txt": "examples/guardrails/outputs/weather_forecast.txt",
    "md": "examples/guardrails/outputs/weather_report.md",
    "csv": "examples/guardrails/outputs/weather_data.csv",
    "json": "examples/guardrails/outputs/weather_data.json",
    "html": "examples/guardrails/outputs/weather_forecast.html",
    "pdf": "examples/guardrails/outputs/weather_report.pdf"
}

# Create a squad with all operations
squad = Squad(
    experts=[weather_expert],
    operations=[txt_operation, md_operation, csv_operation, json_operation, html_operation, pdf_operation],
    process="sequential"
)

# Define guardrail inputs
guardrail_inputs = {
    "location": "Seattle, Washington",
    "time_period": "the next 3 days",
    "include_activities": True
}

# Deploy the squad with guardrails
print("Deploying squad to generate weather forecasts in different formats...")
results = squad.deploy(guardrails=guardrail_inputs)

print("\nGuardrail inputs used:")
for key, value in guardrail_inputs.items():
    print(f"  - {key}: {value}")

# Save results to files
def save_result_to_file(result, file_path, format_type, guardrails=None):
    """Save result to a file in the specified format."""
    try:
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)

        if format_type == "txt" or format_type == "md":
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("# Operation Result\n\n")
                f.write("## Guardrail Inputs\n")
                for key, value in guardrails.items():
                    f.write(f"- {key}: {value}\n")
                f.write("\n## Result\n\n")
                f.write(result)

        elif format_type == "csv":
            # For CSV, we'll just write the raw output as it should already be in CSV format
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(result)

        elif format_type == "json":
            # For JSON, we'll try to parse it and then save it properly formatted
            try:
                # Try to parse as JSON
                json_data = json.loads(result)
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(json_data, f, indent=2)
            except json.JSONDecodeError:
                # If it's not valid JSON, save as text
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(result)

        elif format_type == "html":
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(result)

        elif format_type == "pdf":
            # For PDF, we'll save as text since we don't have reportlab
            with open(file_path.replace('.pdf', '.txt'), 'w', encoding='utf-8') as f:
                f.write("# Weather Report\n\n")
                f.write("## Guardrail Inputs\n")
                for key, value in guardrails.items():
                    f.write(f"- {key}: {value}\n")
                f.write("\n## Result\n\n")
                f.write(result)

        print(f"  - {format_type.upper()} format: {file_path}")
        return True
    except Exception as e:
        print(f"Error saving {format_type} result: {e}")
        return False

print("\nSaving results to files:")
save_result_to_file(txt_operation.result, file_paths["txt"], "txt", guardrail_inputs)
save_result_to_file(md_operation.result, file_paths["md"], "md", guardrail_inputs)
save_result_to_file(csv_operation.result, file_paths["csv"], "csv", guardrail_inputs)
save_result_to_file(json_operation.result, file_paths["json"], "json", guardrail_inputs)
save_result_to_file(html_operation.result, file_paths["html"], "html", guardrail_inputs)
save_result_to_file(pdf_operation.result, file_paths["pdf"], "pdf", guardrail_inputs)

# Note about PDF format
print("\nNote: The PDF format requires the 'reportlab' package. If not installed, the result will be saved as a text file instead.")
print("To install reportlab: pip install reportlab")

if __name__ == "__main__":
    print("Run this script with your Google API key set as an environment variable:")
    print("export GOOGLE_API_KEY=your_api_key_here")
    print("python guardrails_with_result_destination.py")
