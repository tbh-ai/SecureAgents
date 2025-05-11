#!/usr/bin/env python3
# examples/guardrails/hard_guardrails.py
# Author: Saish (TBH.AI)

"""
Advanced example demonstrating complex guardrails with TBH Secure Agents.
This example shows nested conditional logic, complex data structures,
multiple experts with interdependencies, and advanced template variables.
"""

import os
import sys
import logging
import json

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import the TBH Secure Agents framework
from tbh_secure_agents import Expert, Operation, Squad

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def main():
    """
    Main function demonstrating complex guardrails with TBH Secure Agents.
    """
    print("\n" + "="*80)
    print("TBH SECURE AGENTS - HARD GUARDRAILS EXAMPLE".center(80))
    print("="*80 + "\n")

    # Set your API key
    # You can also set this as an environment variable: GOOGLE_API_KEY
    api_key = os.environ.get('GOOGLE_API_KEY')
    if not api_key:
        print("Please set your GOOGLE_API_KEY environment variable.")
        return

    print("Creating experts with complex template variables...\n")

    # Create a market analyst expert with template variables
    market_analyst = Expert(
        specialty="Market Analyst specializing in {industry_sector} with {experience_years}+ years of experience",
        objective="Analyze {analysis_type} data to provide {insight_depth} insights for {target_audience}",
        background="""You have extensive experience analyzing {industry_sector} markets and trends.
        Your expertise includes {expertise_areas} and you're skilled at translating complex data into
        {communication_style} insights that drive business decisions.""",
        api_key=api_key
    )

    # Create a product strategist expert with template variables
    product_strategist = Expert(
        specialty="Product Strategist for {product_category} in the {industry_sector} sector",
        objective="Develop {strategy_type} strategies based on market analysis and {data_source} data",
        background="""You have a strong background in product development and strategy with particular
        focus on {product_focus}. You excel at identifying {opportunity_type} opportunities and creating
        strategies that align with {alignment_factor} factors.""",
        api_key=api_key
    )

    # Create a competitive analyst expert with template variables
    competitive_analyst = Expert(
        specialty="Competitive Intelligence Analyst focusing on {competitor_tier} competitors",
        objective="Analyze competitive landscape to identify {competitive_insight_type} insights",
        background="""You specialize in analyzing competitor strategies, strengths, weaknesses, and market positioning.
        Your approach emphasizes {analysis_approach} and you're particularly skilled at identifying
        {competitive_factor} factors that influence market dynamics.""",
        api_key=api_key
    )

    print("Creating operations with complex template variables and conditional logic...\n")

    # Create a market analysis operation with complex template variables
    market_analysis_operation = Operation(
        instructions="""
        Conduct a {analysis_depth} analysis of the {industry_sector} market with a focus on {market_segment}.
        
        {time_horizon, select,
          current:Focus on the current state of the market and immediate trends.|
          short_term:Analyze trends and developments expected in the next 6-12 months.|
          medium_term:Project market developments over the next 1-3 years.|
          long_term:Provide a long-term outlook covering the next 3-5+ years.
        }
        
        {geographic_scope, select,
          global:Analyze the global market with attention to regional variations.|
          regional:{region_focus, select, 
            north_america:Focus on North American markets with emphasis on {country_focus}.|
            europe:Focus on European markets with emphasis on {country_focus}.|
            asia_pacific:Focus on Asia-Pacific markets with emphasis on {country_focus}.|
            latin_america:Focus on Latin American markets with emphasis on {country_focus}.|
            middle_east_africa:Focus on Middle East and African markets with emphasis on {country_focus}.
          }|
          country:Focus specifically on the {country_focus} market.|
          local:Focus on local market dynamics in {city_focus}.
        }
        
        Include analysis of the following factors:
        
        {market_size_analysis, select,
          detailed:Provide detailed market size data including current valuation, growth rates, and segmentation.|
          basic:Include basic market size information and growth trajectory.|
          none:Exclude market size analysis.
        }
        
        {competitive_landscape, select,
          comprehensive:Analyze all major players, market share distribution, and competitive dynamics.|
          key_players:Focus only on the top {competitor_count} players and their positioning.|
          none:Exclude competitive landscape analysis.
        }
        
        {growth_drivers, select,
          detailed:Provide in-depth analysis of all factors driving market growth with supporting data.|
          primary:Focus only on the {driver_count} primary growth drivers.|
          none:Exclude growth driver analysis.
        }
        
        {challenges_analysis, select,
          detailed:Provide comprehensive analysis of market challenges, barriers, and threats.|
          primary:Focus only on the {challenge_count} most significant challenges.|
          none:Exclude challenges analysis.
        }
        
        {regulatory_environment, select,
          detailed:Include detailed analysis of regulatory factors affecting the market.|
          overview:Provide a brief overview of key regulatory considerations.|
          none:Exclude regulatory analysis.
        }
        
        {technology_trends, select,
          detailed:Analyze technological developments and their impact on the market in detail.|
          overview:Provide a brief overview of key technological trends.|
          none:Exclude technology trend analysis.
        }
        
        {data_visualization, select,
          recommended:Recommend appropriate data visualizations to represent key findings.|
          none:No data visualization recommendations needed.
        }
        
        Analysis should be {tone} in tone and suitable for {target_audience}.
        """,
        output_format="""A structured market analysis report with clear sections for each analysis component.
        The report should be {format_length} and {format_style} in style.""",
        expert=market_analyst
    )

    # Create a product strategy operation with complex template variables
    product_strategy_operation = Operation(
        instructions="""
        Based on the market analysis, develop a {strategy_scope} product strategy for {company_name} in the {industry_sector} sector.
        
        Use the following inputs from the market analysis:
        - Market size and growth projections
        - Competitive landscape
        - Key growth drivers and challenges
        - Regulatory considerations
        - Technology trends
        
        {strategy_type, select,
          entry:Develop a market entry strategy for a new product in this space.|
          growth:Create a growth strategy for an existing product with {current_market_share}% market share.|
          competitive:Develop a competitive strategy to position against {primary_competitor}.|
          innovation:Create an innovation strategy to leverage {innovation_focus} opportunities.|
          diversification:Develop a diversification strategy to expand from current offerings.
        }
        
        {target_segment, select,
          broad:Target the broad market with a general approach.|
          niche:Focus on the {niche_description} niche segment.|
          multi_segment:Target multiple segments with a differentiated approach for each.
        }
        
        {pricing_strategy, select,
          premium:Develop a premium pricing strategy with emphasis on {premium_factor}.|
          competitive:Create a competitive pricing strategy positioned against key competitors.|
          value:Develop a value-based pricing strategy emphasizing {value_proposition}.|
          economy:Create a cost-leadership pricing strategy to capture price-sensitive segments.|
          freemium:Develop a freemium model with {monetization_approach} for revenue generation.
        }
        
        {distribution_approach, select,
          direct:Focus on direct-to-customer distribution channels.|
          partner:Emphasize partner and reseller channels with {partner_strategy}.|
          omnichannel:Develop an omnichannel approach integrating {channel_list}.|
          digital:Focus on digital distribution through {digital_channels}.
        }
        
        {timeframe, select,
          immediate:Focus on immediate implementation within the next quarter.|
          short_term:Develop a strategy for implementation in the next 6-12 months.|
          medium_term:Create a 1-2 year strategic roadmap.|
          long_term:Develop a long-term 3-5 year strategic vision.
        }
        
        Include the following components:
        
        {product_positioning, select,
          detailed:Provide detailed positioning statements and differentiation factors.|
          basic:Include basic positioning guidance.|
          none:Exclude positioning analysis.
        }
        
        {go_to_market, select,
          comprehensive:Develop a comprehensive go-to-market plan with detailed tactics.|
          outline:Provide an outline of key go-to-market considerations.|
          none:Exclude go-to-market planning.
        }
        
        {resource_requirements, select,
          detailed:Include detailed resource requirements and investment needs.|
          overview:Provide a high-level overview of resource considerations.|
          none:Exclude resource analysis.
        }
        
        {risk_assessment, select,
          comprehensive:Include a comprehensive risk assessment with mitigation strategies.|
          key_risks:Focus only on the {risk_count} most significant risks.|
          none:Exclude risk assessment.
        }
        
        {success_metrics, select,
          detailed:Define detailed KPIs and success metrics for strategy evaluation.|
          basic:Include basic success metrics guidance.|
          none:Exclude success metrics.
        }
        """,
        output_format="A comprehensive product strategy document with actionable recommendations",
        expert=product_strategist
    )

    # Create a competitive analysis operation with complex template variables
    competitive_analysis_operation = Operation(
        instructions="""
        Based on the market analysis and product strategy, conduct a {analysis_depth} competitive analysis focusing on {competitor_tier} competitors in the {industry_sector} sector.
        
        {competitor_scope, select,
          direct:Focus only on direct competitors offering similar products/services.|
          indirect:Include both direct competitors and indirect alternatives.|
          potential:Include direct, indirect, and potential future competitors.|
          ecosystem:Analyze the entire competitive ecosystem including partners and complementary offerings.
        }
        
        {competitor_count, select,
          top:Focus on the top {top_competitor_count} competitors by market share.|
          comprehensive:Include all significant competitors in the space.|
          targeted:Focus specifically on the following competitors: {specific_competitors}.
        }
        
        For each competitor, analyze:
        
        {product_analysis, select,
          detailed:Provide detailed product analysis including features, capabilities, and limitations.|
          overview:Include a high-level overview of product offerings.|
          none:Exclude product analysis.
        }
        
        {pricing_analysis, select,
          detailed:Include detailed pricing analysis with specific figures when available.|
          relative:Provide relative pricing positioning (premium, mid-range, economy).|
          none:Exclude pricing analysis.
        }
        
        {market_position, select,
          detailed:Analyze market positioning, share, and trajectory in detail.|
          basic:Include basic market position information.|
          none:Exclude market position analysis.
        }
        
        {strengths_weaknesses, select,
          detailed:Provide comprehensive SWOT analysis for each competitor.|
          key_points:Focus on key strengths and weaknesses only.|
          none:Exclude strengths and weaknesses analysis.
        }
        
        {strategy_analysis, select,
          detailed:Analyze competitor strategies and likely future moves.|
          overview:Provide a basic overview of apparent strategies.|
          none:Exclude strategy analysis.
        }
        
        {differentiation_factors, select,
          detailed:Analyze in detail how competitors differentiate themselves.|
          key_factors:Focus on key differentiation factors only.|
          none:Exclude differentiation analysis.
        }
        
        {customer_perception, select,
          detailed:Include analysis of customer perception and sentiment.|
          overview:Provide a general overview of market perception.|
          none:Exclude customer perception analysis.
        }
        
        {response_strategy, select,
          detailed:Recommend detailed strategies for responding to each competitor.|
          general:Provide general competitive response guidance.|
          none:Exclude response strategies.
        }
        
        {monitoring_approach, select,
          detailed:Include detailed recommendations for ongoing competitor monitoring.|
          basic:Provide basic monitoring guidance.|
          none:Exclude monitoring recommendations.
        }
        """,
        output_format="A structured competitive analysis with clear insights and actionable recommendations",
        expert=competitive_analyst
    )

    print("Creating a squad with the experts and operations...\n")

    # Create a squad with the experts and operations
    strategy_squad = Squad(
        experts=[market_analyst, product_strategist, competitive_analyst],
        operations=[market_analysis_operation, product_strategy_operation, competitive_analysis_operation],
        process="sequential"  # Operations run in sequence
    )

    print("Defining complex guardrail inputs...\n")

    # Define complex guardrail inputs
    guardrail_inputs = {
        # Shared parameters
        "industry_sector": "artificial intelligence software",
        "market_segment": "enterprise AI solutions",
        
        # Market analyst parameters
        "experience_years": "12",
        "analysis_type": "market and competitive",
        "insight_depth": "strategic",
        "target_audience": "C-suite executives",
        "expertise_areas": "market sizing, competitive intelligence, and trend forecasting",
        "communication_style": "clear, actionable",
        "analysis_depth": "comprehensive",
        "time_horizon": "medium_term",
        "geographic_scope": "regional",
        "region_focus": "north_america",
        "country_focus": "United States and Canada",
        "city_focus": "N/A",
        "market_size_analysis": "detailed",
        "competitive_landscape": "key_players",
        "competitor_count": 5,
        "growth_drivers": "detailed",
        "driver_count": 3,
        "challenges_analysis": "primary",
        "challenge_count": 3,
        "regulatory_environment": "overview",
        "technology_trends": "detailed",
        "data_visualization": "recommended",
        "tone": "authoritative yet accessible",
        "format_length": "comprehensive",
        "format_style": "business-focused",
        
        # Product strategist parameters
        "product_category": "enterprise AI platforms",
        "strategy_type": "growth",
        "data_source": "market and competitive",
        "product_focus": "scalable enterprise solutions",
        "opportunity_type": "differentiation",
        "alignment_factor": "market and technology",
        "strategy_scope": "comprehensive",
        "company_name": "TechInnovate AI",
        "current_market_share": 8,
        "primary_competitor": "Enterprise AI Leaders Inc.",
        "innovation_focus": "generative AI",
        "target_segment": "niche",
        "niche_description": "mid-market enterprises in regulated industries",
        "pricing_strategy": "value",
        "premium_factor": "N/A",
        "value_proposition": "ROI and compliance benefits",
        "monetization_approach": "N/A",
        "distribution_approach": "partner",
        "partner_strategy": "industry-specific solution providers",
        "channel_list": "N/A",
        "digital_channels": "N/A",
        "timeframe": "medium_term",
        "product_positioning": "detailed",
        "go_to_market": "outline",
        "resource_requirements": "overview",
        "risk_assessment": "key_risks",
        "risk_count": 5,
        "success_metrics": "detailed",
        
        # Competitive analyst parameters
        "competitor_tier": "top-tier",
        "competitive_insight_type": "strategic",
        "analysis_approach": "data-driven",
        "competitive_factor": "differentiation and positioning",
        "competitor_scope": "direct",
        "top_competitor_count": 5,
        "specific_competitors": "N/A",
        "product_analysis": "detailed",
        "pricing_analysis": "relative",
        "market_position": "detailed",
        "strengths_weaknesses": "detailed",
        "strategy_analysis": "detailed",
        "differentiation_factors": "detailed",
        "customer_perception": "overview",
        "response_strategy": "detailed",
        "monitoring_approach": "detailed"
    }

    print("Complex guardrail inputs defined. Here are some key parameters:")
    print(f"  - Industry sector: {guardrail_inputs['industry_sector']}")
    print(f"  - Market segment: {guardrail_inputs['market_segment']}")
    print(f"  - Analysis depth: {guardrail_inputs['analysis_depth']}")
    print(f"  - Time horizon: {guardrail_inputs['time_horizon']}")
    print(f"  - Company name: {guardrail_inputs['company_name']}")
    print(f"  - Strategy type: {guardrail_inputs['strategy_type']}")

    print("\nDeploying the squad with complex guardrail inputs...\n")

    # Deploy the squad with the guardrail inputs
    try:
        result = strategy_squad.deploy(guardrails=guardrail_inputs)

        print("\n" + "="*80)
        print("FINAL RESULT".center(80))
        print("="*80 + "\n")
        print(result)
        print("\n" + "="*80)

        # Save the output to a file
        output_file = os.path.join(os.path.dirname(__file__), "hard_guardrails_output.txt")
        with open(output_file, "w") as f:
            f.write("TBH SECURE AGENTS - HARD GUARDRAILS EXAMPLE\n\n")
            f.write("Guardrail inputs (selected):\n")
            for key in ["industry_sector", "market_segment", "analysis_depth", "time_horizon", 
                       "company_name", "strategy_type", "target_segment", "competitor_tier"]:
                f.write(f"  - {key}: {guardrail_inputs[key]}\n")
            f.write("\nResult:\n\n")
            f.write(result)
        
        print(f"\nOutput saved to {output_file}")

    except Exception as e:
        print(f"Error during squad deployment: {e}")

if __name__ == "__main__":
    main()
