#!/usr/bin/env python3
"""
Simple AI Researcher and Writer Example with Security Mechanisms
Demonstrates AI researcher and writer collaboration with guardrails, result_destination, and low security profile.
"""

import os
from tbh_secure_agents import Expert, Squad, Operation

# Set API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyA3ZxbIXpR3yNkZwGDznrztdQmgnU16DJI"

def main():
    # Create outputs directory
    os.makedirs("outputs", exist_ok=True)

    # Create AI Researcher expert with template variables
    researcher = Expert(
        specialty="AI Research Analyst specializing in {research_domain}",
        objective="Research {research_topic} and provide {research_style} analysis",
        background="You focus on {research_focus} using {data_sources}",
        security_profile="minimal"
    )

    # Create Writer expert with template variables
    writer = Expert(
        specialty="Technical Writer specializing in {writing_domain}",
        objective="Create {content_type} content for {target_audience}",
        background="You write in {writing_style} style with {content_approach} approach",
        security_profile="minimal"
    )

    # Research operation with template variables
    research_operation = Operation(
        instructions="""
        Research {research_topic} focusing on {research_focus}.

        {research_depth, select,
          basic:Provide a basic overview with key points.|
          detailed:Provide detailed analysis with examples.|
          comprehensive:Provide comprehensive analysis with multiple perspectives.
        }

        Use {data_sources} and ensure {content_quality}.
        """,
        expected_output="Research analysis about {research_topic}",
        expert=researcher,
        result_destination="outputs/research_analysis.md"
    )

    # Writing operation with template variables
    writing_operation = Operation(
        instructions="""
        Create a {content_type} about {research_topic}.

        {writing_format, select,
          summary:Write a concise summary with key takeaways.|
          article:Write a structured article with introduction, body, and conclusion.|
          report:Write a formal report with executive summary and detailed sections.
        }

        Target audience: {target_audience}
        Writing style: {writing_style}
        """,
        expected_output="{content_type} about {research_topic}",
        expert=writer,
        result_destination="outputs/final_content.md"
    )

    # Create squad with both experts and operations
    ai_content_squad = Squad(
        experts=[researcher, writer],
        operations=[research_operation, writing_operation],
        process="sequential",
        security_profile="minimal"
    )

    # Define guardrails for the squad with template variable values
    guardrails = {
        # Research expert variables
        "research_domain": "software development",
        "research_topic": "Python programming best practices",
        "research_focus": "code quality and maintainability",
        "data_sources": "established programming guidelines",
        "content_quality": "accurate and practical information",
        "research_depth": "detailed",
        "research_style": "practical",

        # Writer expert variables
        "writing_domain": "technical documentation",
        "content_type": "guide",
        "target_audience": "software developers",
        "writing_style": "clear and practical",
        "content_approach": "example-driven",
        "writing_format": "article"
    }

    # Deploy the squad with guardrails
    result = ai_content_squad.deploy(guardrails=guardrails)

    return result

if __name__ == "__main__":
    main()
