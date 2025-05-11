#!/usr/bin/env python3
# story_concept_marketing.py
# Demonstrates a use case: Story Concept & Marketing Blurb

import os
from tbh_secure_agents import Expert, Operation, Squad

# --- !!! SECURITY WARNING !!! ---
# The following line includes the API key directly in the code.
# This is INSECURE and ONLY for temporary testing due to environment variable issues.
# DO NOT commit this code or use this method in production.
# Use environment variables (`GOOGLE_API_KEY`) for secure key management.
# --- !!! /SECURITY WARNING !!! ---
TESTING_API_KEY = "" # Key provided by user

print("--- Initializing Experts (Story Concept & Marketing) ---")
# Define Experts for the new use case
try:
    story_writer = Expert(
        specialty='Creative Story Writer',
        objective='Generate a unique and compelling short story concept about a time-traveling librarian.',
        background='An imaginative author specializing in science fiction and fantasy.',
        llm_model_name='gemini-2.0-flash-lite',
        security_profile='creative_standard', # Example profile
        api_key=TESTING_API_KEY
    )

    marketer = Expert(
        specialty='Marketing Specialist',
        objective='Write a catchy promotional blurb for a new story concept.',
        background='Expert in crafting short, engaging descriptions to attract readers.',
        llm_model_name='gemini-2.0-flash-lite',
        security_profile='marketing_safe', # Example profile
        api_key=TESTING_API_KEY
    )
except Exception as e:
    print(f"\nError initializing experts: {e}")
    exit()

print("\n--- Defining Operations (Story Concept & Marketing) ---")
# Define Operations for the use case
operation_concept = Operation(
    instructions='Create a short story concept (1 paragraph) featuring a librarian who discovers a hidden time-travel device within an ancient book.',
    output_format='A paragraph outlining the core story idea, main character, and conflict.',
    expert=story_writer
)

operation_blurb = Operation(
    instructions='Based *only* on the provided story concept, write a short (2-3 sentences) promotional blurb designed to intrigue potential readers.',
    output_format='A catchy marketing blurb for the story concept.',
    expert=marketer
    # Context (the story concept) will be passed from operation_concept
)

print("\n--- Creating Squad (Story Concept & Marketing) ---")
# Create Squad
story_squad = Squad(
    experts=[story_writer, marketer],
    operations=[operation_concept, operation_blurb],
    process='sequential'
)

print("\n--- Deploying Squad (Story Concept & Marketing) ---")
# Deploy the Squad
try:
    final_blurb = story_squad.deploy()

    print("\n--- Squad Execution Finished (Story Concept & Marketing) ---")
    print("\nFinal Result (Marketing Blurb):")
    print("---------------------------------")
    print(final_blurb)
    print("---------------------------------")

    # You might also want to access the intermediate result (the concept) if needed
    # print("\nIntermediate Result (Story Concept):")
    # print(operation_concept.result) # Accessing the result stored in the operation object

except Exception as e:
    print(f"\nAn error occurred during squad execution: {e}")

print("\n--- Story Concept & Marketing Example Finished ---")
