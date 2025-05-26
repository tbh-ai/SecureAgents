#!/usr/bin/env python3
"""
AI Researcher and Writer Example with Security Mechanisms
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
        objective="Conduct thorough research on {research_topic} focusing on {research_focus}",
        background="You are an expert researcher with access to {data_sources} and must ensure {content_accuracy}",
        security_profile="minimal"
    )

    # Create Writer expert with template variables
    writer = Expert(
        specialty="Technical Writer specializing in {writing_domain}",
        objective="Transform research findings into {writing_style} content for {target_audience}",
        background="You excel at creating {content_type} content with {content_length} approach",
        security_profile="minimal"
    )

    # Research operation with template variables
    research_operation = Operation(
        instructions="""
        Research the current state of {research_topic} in 2024, focusing on {research_focus}.

        {research_depth, select,
          comprehensive:Include detailed analysis of capabilities, limitations, recent developments, and future trends.|
          focused:Focus on key developments and current capabilities.|
          overview:Provide a high-level overview of the current state.
        }

        Include information about major models and recent developments.
        Ensure all information comes from {data_sources}.
        """,
        expected_output="Comprehensive research report with key findings about {research_topic}",
        expert=researcher,
        result_destination="outputs/research_findings.md"
    )

    # Writing operation with template variables
    writing_operation = Operation(
        instructions="""
        Write a {writing_style} article about {research_topic} based on the research findings.

        {content_structure, select,
          academic:Use formal academic structure with abstract, introduction, methodology, findings, and conclusion.|
          professional:Use professional business structure with executive summary, key points, and recommendations.|
          accessible:Use accessible structure with clear headings, bullet points, and easy-to-understand language.
        }

        Target audience: {target_audience}
        Content length: {content_length}
        Writing tone: {writing_tone}
        """,
        expected_output="Well-structured {content_type} about {research_topic}",
        expert=writer,
        result_destination="outputs/llm_evolution_article.md"
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
        "research_domain": "artificial intelligence",
        "research_topic": "large language models",
        "research_focus": "capabilities, limitations, and recent developments",
        "data_sources": "publicly available information and research papers",
        "content_accuracy": "factual and well-sourced information",
        "research_depth": "comprehensive",

        # Writer expert variables
        "writing_domain": "technical communication",
        "writing_style": "professional",
        "target_audience": "technical professionals",
        "content_type": "article",
        "content_length": "comprehensive but concise",
        "content_structure": "professional",
        "writing_tone": "informative and engaging"
    }

    # Deploy the squad with guardrails
    result = ai_content_squad.deploy(guardrails=guardrails)

    return result

if __name__ == "__main__":
    main()
