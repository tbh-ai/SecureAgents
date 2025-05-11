#!/usr/bin/env python3
# flask_app_generation.py
# Demonstrates a use case: Basic Flask App Generation & README

import os
from tbh_secure_agents import Expert, Operation, Squad

# --- !!! SECURITY WARNING !!! ---
# The following line includes the API key directly in the code.
# This is INSECURE and ONLY for temporary testing due to environment variable issues.
# DO NOT commit this code or use this method in production.
# Use environment variables (`GOOGLE_API_KEY`) for secure key management.
# --- !!! /SECURITY WARNING !!! ---
TESTING_API_KEY = "" # Key provided by user

print("--- Initializing Experts (Flask App Generation) ---")
# Define Experts for the use case
try:
    flask_dev = Expert(
        specialty='Python Web Developer',
        objective='Generate Python code for a simple Flask web application.',
        background='Experienced in creating basic web server applications using Flask.',
        llm_model_name='gemini-2.0-flash-lite',
        security_profile='web_code_gen', # Example profile
        api_key=TESTING_API_KEY
    )

    readme_writer = Expert(
        specialty='Technical Writer for Developers',
        objective='Write clear setup and usage instructions for Python applications.',
        background='Specializes in creating README files for software projects.',
        llm_model_name='gemini-2.0-flash-lite',
        security_profile='readme_standard', # Example profile
        api_key=TESTING_API_KEY
    )
except Exception as e:
    print(f"\nError initializing experts: {e}")
    exit()

print("\n--- Defining Operations (Flask App Generation) ---")
# Define Operations for the use case
operation_flask_code = Operation(
    instructions='Generate the complete Python code for a minimal Flask application in a single file named `app.py`. It should have one route ("/") that returns the text "Hello, Secure World!". Include necessary imports and the standard `if __name__ == "__main__":` block to run the development server.',
    output_format='Complete Python code for the Flask app.',
    expert=flask_dev
)

operation_readme = Operation(
    instructions='Based *only* on the provided Flask application code, write the content for a `README.md` file. The README should explain: 1. What the application does. 2. How to set up a virtual environment and install Flask (`pip install Flask`). 3. How to run the application (`python app.py`). 4. What output to expect in the terminal and how to access the app in a web browser.',
    output_format='Markdown content suitable for a README file.',
    expert=readme_writer
    # Context (the Flask code) will be passed from operation_flask_code
)

print("\n--- Creating Squad (Flask App Generation) ---")
# Create Squad
flask_squad = Squad(
    experts=[flask_dev, readme_writer],
    operations=[operation_flask_code, operation_readme],
    process='sequential'
)

print("\n--- Deploying Squad (Flask App Generation) ---")
# Deploy the Squad
try:
    final_readme_content = flask_squad.deploy()

    print("\n--- Squad Execution Finished (Flask App Generation) ---")

    generated_flask_code = operation_flask_code.result # Get the code from the first operation

    print("\nGenerated Flask App Code (`app.py`):")
    print("------------------------------------")
    print(generated_flask_code if generated_flask_code else "# Error generating Flask code.")
    print("------------------------------------")

    print("\nGenerated README.md Content:")
    print("----------------------------")
    print(final_readme_content if final_readme_content else "# Error generating README content.")
    print("----------------------------")

except Exception as e:
    print(f"\nAn error occurred during squad execution: {e}")

print("\n--- Flask App Generation Example Finished ---")
