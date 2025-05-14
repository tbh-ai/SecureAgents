"""
TBH Secure Agents - Stakeholder Demo

This example demonstrates a comprehensive use case for the TBH Secure Agents framework:
A competitive analysis project using multiple experts working together.

Features demonstrated:
1. Creating specialized experts with different roles
2. Defining multiple operations with clear instructions
3. Using a Squad for coordinated multi-expert execution
4. Using guardrails to control expert behavior
5. Saving results to multiple formats

To run this example:
1. Install the package: pip install tbh-secure-agents
2. Set your Google API key as an environment variable: export GOOGLE_API_KEY=your_api_key
3. Run the script: python stakeholder_demo.py
"""

import os
from tbh_secure_agents import Expert, Operation, Squad

# Create output directory
os.makedirs("output", exist_ok=True)

# Set API key (replace with your actual API key or set as environment variable)
API_KEY = os.environ.get("GOOGLE_API_KEY", "AIzaSyAwkWbBba6t9O15Ok0bsxFmBRoFfhokmVA")  # Using a demo API key

# Create specialized experts with minimal security profiles
market_researcher = Expert(
    specialty="Market Researcher",
    objective="Research market trends and competitive landscape in {industry}",
    background="Expert in market research with focus on competitive analysis",
    security_profile="minimal",
    api_key=API_KEY
)

competitor_analyst = Expert(
    specialty="Competitor Analyst",
    objective="Analyze competitor strategies and identify their strengths and weaknesses",
    background="Specialized in competitive intelligence and strategic analysis",
    security_profile="minimal",
    api_key=API_KEY
)

strategy_consultant = Expert(
    specialty="Strategy Consultant",
    objective="Develop strategic recommendations based on market and competitor analysis",
    background="Experienced consultant with expertise in business strategy development",
    security_profile="minimal",
    api_key=API_KEY
)

# Define operations with clear instructions
market_research = Operation(
    instructions="""
    Research the current state of the {industry} industry with focus on {focus_area}.

    Include:
    1. Market size and growth rate
    2. Key market segments
    3. Major trends shaping the industry
    4. Regulatory factors affecting the market

    Keep your research professional, factual, and concise.
    Focus only on well-established business facts.
    """,
    expert=market_researcher
)

competitor_analysis = Operation(
    instructions="""
    Based on the market research, analyze the top 3 competitors in the {industry} industry.

    For each competitor, identify:
    1. Their market positioning
    2. Key strengths
    3. Notable weaknesses
    4. Recent strategic moves

    Keep your analysis objective and fact-based.
    """,
    expert=competitor_analyst
)

strategy_recommendations = Operation(
    instructions="""
    Based on the market research and competitor analysis, develop strategic recommendations.

    Your recommendations should:
    1. Identify 3-5 key opportunities
    2. Suggest specific strategic initiatives
    3. Outline potential implementation approaches
    4. Consider potential risks and mitigation strategies

    Format your recommendations in a clear, actionable format.
    """,
    expert=strategy_consultant,
    result_destination="output/strategic_recommendations.md"
)

# Create a squad with the experts and operations
competitive_analysis_squad = Squad(
    experts=[market_researcher, competitor_analyst, strategy_consultant],
    operations=[market_research, competitor_analysis, strategy_recommendations],
    process="sequential",  # Operations run in sequence, passing results as context
    result_destination={
        "format": "json",
        "file_path": "output/competitive_analysis_summary.json"
    }
)

# Define guardrails to control expert behavior
guardrails = {
    "industry": "cloud computing",
    "focus_area": "AI and machine learning services",
    "time_frame": "last 12 months",
    "target_audience": "enterprise customers"
}

# Deploy the squad with guardrails
result = competitive_analysis_squad.deploy(guardrails=guardrails)
