#!/usr/bin/env python3
"""
AI Researcher and Writer Example

This example demonstrates a simple AI Researcher and Writer team using
the TBH Secure Agents framework with hybrid security validation.
"""

import os
from tbh_secure_agents import Expert, Operation, Squad
from tbh_secure_agents.security_validation import enable_hybrid_validation

# Set the API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyA3ZxbIXpR3yNkZwGDznrztdQmgnU16DJI"

# Enable hybrid validation with report generation
enable_hybrid_validation(enable_reports=True)

# Create output directory
os.makedirs("research_output", exist_ok=True)

# Create the AI Researcher expert with minimal security
researcher = Expert(
    specialty="AI Research",
    objective="Research AI topics and provide comprehensive information",
    security_profile="minimal"  # Changed from standard to minimal
)

# Create the AI Writer expert with minimal security
writer = Expert(
    specialty="Technical Writing",
    objective="Create well-structured, clear technical content",
    security_profile="minimal"  # Changed from standard to minimal
)

# Create the research operation with very simple, safe content
research_operation = Operation(
    instructions="Write a short paragraph about artificial intelligence.",
    expert=researcher,
    result_destination="research_output/research_findings.md"
)

# Create the writing operation with very simple, safe content
writing_operation = Operation(
    instructions="Based on the research findings, write a short article about AI.",
    expert=writer,
    result_destination="research_output/final_article.md"
)

# Create the research and writing squad with minimal security
ai_team = Squad(
    name="AI Research and Writing Team",
    experts=[researcher, writer],
    operations=[research_operation, writing_operation],
    process="sequential",
    security_profile="minimal",  # Changed from standard to minimal
    result_destination="research_output/complete_project.md"
)

# Deploy the squad to execute the operations
ai_team.deploy()
