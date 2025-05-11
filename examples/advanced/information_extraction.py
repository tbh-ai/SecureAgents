#!/usr/bin/env python3
# information_extraction.py
# Demonstrates a use case: Information Extraction & Reporting

import os
from tbh_secure_agents import Expert, Operation, Squad

# --- !!! SECURITY WARNING !!! ---
# The following line includes the API key directly in the code.
# This is INSECURE and ONLY for temporary testing due to environment variable issues.
# DO NOT commit this code or use this method in production.
# Use environment variables (`GOOGLE_API_KEY`) for secure key management.
# --- !!! /SECURITY WARNING !!! ---
TESTING_API_KEY = "" # Key provided by user

# --- Input Data ---
source_text = """
Dr. Evelyn Reed, a renowned astrophysicist based in Geneva, presented her groundbreaking research
on dark matter detection using novel sensor arrays deployed via high-altitude balloons over Antarctica.
Her work, funded by the Global Science Foundation, suggests that previously undetected particles
might interact weakly with standard matter under specific cryogenic conditions. The project,
codenamed 'Cosmic Whisper', aims to map these interactions over the next five years.
"""
# --- /Input Data ---


print("--- Initializing Experts (Information Extraction) ---")
# Define Experts for the use case
try:
    extractor = Expert(
        specialty='Data Analyst specializing in Text Analysis',
        objective='Extract key named entities (people, organizations, locations, projects, concepts) from provided text.',
        background='Expert in identifying structured information within unstructured text.',
        llm_model_name='gemini-2.0-flash-lite',
        security_profile='data_extraction_strict', # Example profile
        api_key=TESTING_API_KEY
    )

    reporter = Expert(
        specialty='Report Generator',
        objective='Synthesize extracted information into a clear, concise bullet-point summary.',
        background='Skilled at summarizing key findings for quick review.',
        llm_model_name='gemini-2.0-flash-lite',
        security_profile='reporting_concise', # Example profile
        api_key=TESTING_API_KEY
    )
except Exception as e:
    print(f"\nError initializing experts: {e}")
    exit()

print("\n--- Defining Operations (Information Extraction) ---")
# Define Operations for the use case
operation_extract = Operation(
    instructions=f'From the following text, identify and list the key named entities (People, Organizations, Locations, Project Names, Key Concepts). Text:\n\n{source_text}',
    output_format='A list or structured representation of the extracted entities.',
    expert=extractor
)

operation_report = Operation(
    instructions='Based *only* on the provided list of extracted entities, generate a short bullet-point report summarizing the key information.',
    output_format='A concise summary in bullet points.',
    expert=reporter
    # Context (extracted entities) will be passed from operation_extract
)

print("\n--- Creating Squad (Information Extraction) ---")
# Create Squad
analysis_squad = Squad(
    experts=[extractor, reporter],
    operations=[operation_extract, operation_report],
    process='sequential'
)

print("\n--- Deploying Squad (Information Extraction) ---")
# Deploy the Squad
try:
    final_report = analysis_squad.deploy()

    print("\n--- Squad Execution Finished (Information Extraction) ---")

    extracted_entities = operation_extract.result # Get the entities from the first operation

    print("\nExtracted Entities:")
    print("---------------------")
    print(extracted_entities if extracted_entities else "# Error extracting entities.")
    print("---------------------")

    print("\nGenerated Summary Report:")
    print("-------------------------")
    print(final_report if final_report else "# Error generating report.")
    print("-------------------------")

except Exception as e:
    print(f"\nAn error occurred during squad execution: {e}")

print("\n--- Information Extraction Example Finished ---")
