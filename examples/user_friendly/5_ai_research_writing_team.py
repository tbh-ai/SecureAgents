#!/usr/bin/env python3
"""
Example 5: AI Research & Writing Team
=====================================

This example shows how to create a team of AI agents (Squad) that work
together - a researcher and writer collaborating on a complete project.

Features demonstrated:
- Creating multiple Expert agents
- Using Squad for team collaboration
- Sequential workflow (research then write)
- Using guardrails for team coordination
- Saving final result in JSON format
"""

import os

# Set your Google API key (replace with your actual key)
# os.environ["GOOGLE_API_KEY"] = "your-api-key-here"

from tbh_secure_agents import Expert, Operation, Squad

def main():
    # Create outputs directory
    os.makedirs("outputs/user_examples", exist_ok=True)

    # Create AI team members
    researcher = Expert(
        specialty="Research Specialist",
        objective="Conduct thorough research and gather comprehensive information",
        security_profile="minimal"
    )

    writer = Expert(
        specialty="Content Writer",
        objective="Transform research into engaging, well-written content",
        security_profile="minimal"
    )

    # Define team guardrails
    team_guardrails = {
        "factual_content": True,
        "no_harmful_content": True,
        "professional_tone": True,
        "data_privacy": True,
        "project_topic": "sustainable technology trends",
        "target_audience": "business executives",
        "content_length": "comprehensive but concise",
        "include_data": True,
        "include_recommendations": True
    }

    # Create research operation
    research_operation = Operation(
        instructions="Research the latest trends in sustainable technology, including market data, key innovations, and industry outlook.",
        output_format="Comprehensive research findings with data, trends, and key insights",
        expert=researcher,
        result_destination="outputs/user_examples/sustainability_research.md"
    )

    # Create writing operation (will use research results as context)
    writing_operation = Operation(
        instructions="Based on the research findings, write an executive summary about sustainable technology trends for business leaders.",
        output_format="Professional executive summary with key insights and actionable recommendations",
        expert=writer,
        result_destination="outputs/user_examples/sustainability_executive_summary.md"
    )

    # Create the AI team (Squad)
    research_writing_team = Squad(
        experts=[researcher, writer],
        operations=[research_operation, writing_operation],
        process="sequential",  # Research first, then write
        result_destination={
            "format": "json",
            "file_path": "outputs/user_examples/team_project_results.json"
        }
    )

    # Deploy the team
    print("👥 Starting AI Research & Writing Team...")
    print("Team: Research Specialist + Content Writer")
    print("Project: Sustainable Technology Trends")
    print("Process: Sequential (Research → Write)")
    print("Final Output: outputs/user_examples/team_project_results.json")
    print()

    try:
        final_result = research_writing_team.deploy(guardrails=team_guardrails)
        print("✅ Team project completed successfully!")
        print()
        print("📄 Individual Results:")
        print(f"   Research: {research_operation.result_destination}")
        print(f"   Writing: {writing_operation.result_destination}")
        print(f"   Team Summary: {research_writing_team.result_destination['file_path']}")
        print()
        print("Preview of final team result:")
        print("-" * 50)
        print(final_result[:300] + "..." if len(final_result) > 300 else final_result)

    except Exception as e:
        print(f"❌ Error during team collaboration: {e}")

if __name__ == "__main__":
    main()
