#!/usr/bin/env python3
# code_security_review.py
# Demonstrates a more complex use case: Code Review, Security Advice, Refactoring

import os
from tbh_secure_agents import Expert, Operation, Squad

# --- !!! SECURITY WARNING !!! ---
# Using a hardcoded API key for testing ONLY. Replace with environment variables for production.
TESTING_API_KEY = "" # Key provided by user
# --- !!! /SECURITY WARNING !!! ---

# --- Input Code Snippet ---
original_code = """
import os
import subprocess

# WARNING: This code has potential security issues for demonstration purposes.
def execute_command(user_input):
    # Directly using user input in a shell command is dangerous
    command = "echo 'User provided: ' && echo " + user_input
    print(f"Executing: {command}")
    # Using shell=True with user input is highly risky
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout
"""
# --- /Input Code Snippet ---

print("--- Initializing Experts (Code Security Review) ---")
try:
    reviewer = Expert(
        specialty='Security Code Reviewer',
        objective='Identify potential security vulnerabilities in Python code snippets, focusing on command injection and unsafe practices.',
        background='Experienced in static code analysis and identifying common security pitfalls.',
        llm_model_name='gemini-2.0-flash-lite',
        security_profile='code_review_strict',
        api_key=TESTING_API_KEY
    )

    advisor = Expert(
        specialty='Security Best Practices Advisor',
        objective='Provide specific, actionable recommendations to fix identified security vulnerabilities in Python code.',
        background='Expert in secure coding practices and mitigating risks like command injection.',
        llm_model_name='gemini-2.0-flash-lite',
        security_profile='security_advice_standard',
        api_key=TESTING_API_KEY
    )

    refactorer = Expert(
        specialty='Python Code Refactorer',
        objective='Rewrite Python code snippets to incorporate security improvements based on provided suggestions.',
        background='Skilled in modifying code while preserving intended functionality but enhancing security.',
        llm_model_name='gemini-2.0-flash-lite',
        security_profile='code_refactor_safe',
        api_key=TESTING_API_KEY
    )
except Exception as e:
    print(f"\nError initializing experts: {e}")
    exit()

print("\n--- Defining Operations (Code Security Review) ---")
operation_review = Operation(
    instructions=f'Review the following Python code for potential security vulnerabilities, especially related to command injection and the use of subprocess with shell=True. List the identified issues clearly. Code:\n```python\n{original_code}\n```',
    output_format='A list of identified security vulnerabilities.',
    expert=reviewer
)

operation_suggest = Operation(
    instructions='Based *only* on the provided security review findings, suggest specific code changes or alternative approaches to mitigate the identified vulnerabilities in the original code snippet.',
    output_format='Actionable suggestions for improving the code\'s security.',
    expert=advisor
    # Context: Review findings from operation_review
)

operation_refactor = Operation(
    instructions=f'Rewrite the original Python code snippet provided below, incorporating *only* the security suggestions provided in the context. Ensure the core functionality (executing some form of command safely, if possible, or demonstrating safe handling) is addressed. Original Code:\n```python\n{original_code}\n```',
    output_format='The refactored Python code snippet incorporating security improvements.',
    expert=refactorer
    # Context: Security suggestions from operation_suggest
)

print("\n--- Creating Squad (Code Security Review) ---")
security_analysis_squad = Squad(
    experts=[reviewer, advisor, refactorer],
    operations=[operation_review, operation_suggest, operation_refactor],
    process='sequential'
)

print("\n--- Deploying Squad (Code Security Review) ---")
try:
    final_refactored_code = security_analysis_squad.deploy()

    print("\n--- Squad Execution Finished (Code Security Review) ---")

    review_findings = operation_review.result
    suggestions = operation_suggest.result

    print("\nOriginal Code:")
    print("----------------")
    print(original_code)
    print("----------------")

    print("\nSecurity Review Findings:")
    print("-------------------------")
    print(review_findings if review_findings else "# Error generating review.")
    print("-------------------------")

    print("\nImprovement Suggestions:")
    print("------------------------")
    print(suggestions if suggestions else "# Error generating suggestions.")
    print("------------------------")

    print("\nRefactored Code:")
    print("------------------")
    print(final_refactored_code if final_refactored_code else "# Error generating refactored code.")
    print("------------------")

except Exception as e:
    print(f"\nAn error occurred during squad execution: {e}")

print("\n--- Code Security Review Example Finished ---")
