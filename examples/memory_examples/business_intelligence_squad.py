#!/usr/bin/env python3
"""
Business Intelligence Squad Example
==================================
Real-world multi-agent system demonstrating:
- Business intelligence analysis workflow
- Market research, competitive analysis, and strategic recommendations
- Advanced guardrails with conditional logic
- Multiple output formats and result destinations
- Memory-enabled experts for knowledge accumulation
- Context passing for collaborative intelligence
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from tbh_secure_agents import Expert, Operation, Squad

# Set API key for testing
# os.environ["GOOGLE_API_KEY"] = "your-api-key-here"

def main():
    """
    Business Intelligence Squad with three specialized experts:
    1. Market Analyst - Analyzes market conditions and trends
    2. Business Strategist - Develops strategic recommendations
    3. Intelligence Reporter - Creates executive reports and dashboards
    """
    
    # Create outputs directory
    os.makedirs("outputs/business_intelligence", exist_ok=True)
    
    print("📊 Business Intelligence Squad")
    print("=" * 50)
    print("Analyzing market conditions and generating strategic intelligence...")
    print()
    
    # 1. CREATE BUSINESS INTELLIGENCE EXPERTS
    print("👔 Creating Business Intelligence Team...")
    
    # Market Analyst with advanced template variables
    market_analyst = Expert(
        specialty="Market Analyst specializing in {market_sector} and {analysis_type}",
        objective="Analyze {market_focus} trends and provide {analysis_depth} market intelligence",
        background="Expert in {analytical_methods} with access to {data_sources} and {market_coverage} scope",
        security_profile="minimal",
        memory_duration="long_term",
        user_id="market_analyst_001"
    )
    
    # Business Strategist with strategic focus
    business_strategist = Expert(
        specialty="Business Strategist for {business_domain} in {industry_vertical}",
        objective="Develop {strategy_type} strategies based on {strategic_focus}",
        background="Strategic planning expert with {strategy_approach} methodology and {business_experience} experience",
        security_profile="minimal", 
        memory_duration="long_term",
        user_id="business_strategist_001"
    )
    
    # Intelligence Reporter for executive communications
    intelligence_reporter = Expert(
        specialty="Business Intelligence Reporter for {reporting_domain}",
        objective="Create {report_type} reports for {executive_audience}",
        background="Expert in {reporting_style} with focus on {communication_approach} and {presentation_format}",
        security_profile="minimal",
        memory_duration="long_term", 
        user_id="intelligence_reporter_001"
    )
    
    print("✅ Created specialized BI team with memory capabilities")
    print()
    
    # 2. CREATE ADVANCED OPERATIONS WITH CONDITIONAL GUARDRAILS
    print("📈 Setting up Advanced BI Operations...")
    
    # Market Analysis Operation with complex conditional logic
    market_analysis_operation = Operation(
        instructions="""
        Conduct comprehensive market analysis for {market_sector} focusing on {market_focus}.
        
        Analysis Framework:
        {analysis_type, select,
          competitive: Focus on competitor analysis, market share, and positioning strategies.|
          trend: Analyze market trends, growth patterns, and emerging opportunities.|
          financial: Examine financial performance, valuation metrics, and investment flows.|
          comprehensive: Cover all aspects including competitive landscape, trends, and financials.
        }
        
        {analysis_depth, select,
          executive: High-level strategic overview for C-suite decision making.|
          tactical: Detailed operational insights for department heads and managers.|
          deep_dive: Exhaustive analysis for specialists and detailed planning.
        }
        
        Required Analysis Components:
        - Market size and growth projections for {time_horizon}
        - Key player analysis and market positioning
        - {analytical_methods} methodology application
        - Risk assessment and opportunity identification
        - {market_coverage} geographic and segment coverage
        
        Data Sources: {data_sources}
        Analytical Methods: {analytical_methods}
        Time Horizon: {time_horizon}
        Geographic Scope: {market_coverage}
        
        {industry_insights, select,
          emerging: Focus on new market entrants and disruptive technologies.|
          established: Analyze mature market dynamics and optimization opportunities.|
          hybrid: Balance emerging trends with established market analysis.
        }
        
        Ensure analysis supports {strategic_objective} with actionable insights.
        """,
        expected_output="Comprehensive market analysis report for {market_sector}",
        expert=market_analyst,
        result_destination={
            "format": "md",
            "file_path": "outputs/business_intelligence/01_market_analysis.md"
        }
    )
    
    # Strategic Planning Operation building on market analysis
    strategic_planning_operation = Operation(
        instructions="""
        Develop strategic recommendations based on the market analysis provided.
        
        Strategic Framework:
        {strategy_type, select,
          growth: Focus on market expansion and revenue growth strategies.|
          competitive: Develop competitive positioning and differentiation strategies.|
          innovation: Emphasize R&D, product development, and technological advancement.|
          operational: Optimize internal processes and operational efficiency.|
          comprehensive: Integrate all strategic dimensions for holistic planning.
        }
        
        Strategic Planning Components:
        - Strategic objectives aligned with {strategic_objective}
        - Competitive positioning and differentiation strategy
        - Resource allocation and investment priorities
        - Risk mitigation and contingency planning
        - Implementation roadmap with {time_horizon} timeline
        
        {strategic_focus, select,
          market_entry: Strategies for entering new markets or segments.|
          market_expansion: Growth strategies within existing markets.|
          market_defense: Defensive strategies against competitive threats.|
          market_optimization: Efficiency and performance optimization strategies.
        }
        
        Strategy Approach: {strategy_approach}
        Business Domain: {business_domain}
        Industry Vertical: {industry_vertical}
        
        {priority_framework, select,
          revenue: Prioritize revenue generation and top-line growth.|
          profitability: Focus on margin improvement and bottom-line optimization.|
          market_share: Emphasize market position and competitive advantage.|
          balanced: Balance revenue, profitability, and market position objectives.
        }
        
        Provide specific, actionable recommendations with clear success metrics.
        """,
        expected_output="Strategic plan with specific recommendations for {business_domain}",
        expert=business_strategist,
        result_destination={
            "format": "md",
            "file_path": "outputs/business_intelligence/02_strategic_plan.md"
        }
    )
    
    # Executive Reporting Operation for final intelligence package
    executive_reporting_operation = Operation(
        instructions="""
        Create an executive intelligence report synthesizing market analysis and strategic recommendations.
        
        Report Structure:
        {report_type, select,
          dashboard: Visual dashboard format with key metrics and KPIs.|
          briefing: Concise executive briefing for board presentations.|
          comprehensive: Detailed report for strategic planning sessions.|
          action_plan: Implementation-focused document with specific next steps.
        }
        
        Executive Communication Requirements:
        - Executive summary for {executive_audience}
        - Key findings and strategic implications
        - Recommended actions with priority rankings
        - Success metrics and performance indicators
        - Risk assessment and mitigation strategies
        
        {reporting_style, select,
          analytical: Data-driven presentation with detailed analysis.|
          narrative: Story-driven approach with clear business impact.|
          visual: Chart and graphic-heavy format for quick comprehension.|
          hybrid: Combination of analytical depth with visual clarity.
        }
        
        {communication_approach, select,
          consultative: Advisory tone with recommended next steps.|
          informational: Fact-based presentation for internal decision making.|
          persuasive: Compelling case for specific strategic directions.|
          collaborative: Team-oriented approach for collective decision making.
        }
        
        Presentation Format: {presentation_format}
        Target Audience: {executive_audience}
        Business Context: {business_context}
        
        {urgency_level, select,
          immediate: Critical decisions required within days.|
          quarterly: Strategic planning for next quarter.|
          annual: Long-term strategic planning horizon.|
          ongoing: Regular intelligence updates and monitoring.
        }
        
        Ensure the report enables informed strategic decision making.
        """,
        expected_output="Executive intelligence report ready for {executive_audience}",
        expert=intelligence_reporter,
        result_destination={
            "format": "html",
            "file_path": "outputs/business_intelligence/03_executive_report.html"
        }
    )
    
    print("✅ Created advanced BI operations with conditional guardrails")
    print()
    
    # 3. CREATE BUSINESS INTELLIGENCE SQUAD
    print("🎯 Assembling Business Intelligence Squad...")
    
    bi_squad = Squad(
        experts=[market_analyst, business_strategist, intelligence_reporter],
        operations=[market_analysis_operation, strategic_planning_operation, executive_reporting_operation],
        process="sequential",
        security_profile="minimal",
        result_destination={
            "format": "json",
            "file_path": "outputs/business_intelligence/bi_intelligence_package.json"
        }
    )
    
    print("✅ BI Squad assembled with sequential intelligence workflow")
    print()
    
    # 4. COMPREHENSIVE GUARDRAILS FOR BUSINESS INTELLIGENCE
    print("🛡️  Configuring Advanced BI Guardrails...")
    
    guardrails = {
        # Market Analyst Configuration
        "market_sector": "fintech and digital payments",
        "analysis_type": "comprehensive",
        "market_focus": "mobile payment adoption and cryptocurrency integration",
        "analysis_depth": "tactical",
        "analytical_methods": "quantitative analysis, competitor benchmarking, and trend analysis",
        "data_sources": "industry reports, financial filings, and market research databases",
        "market_coverage": "North America and European markets",
        "time_horizon": "next 18 months",
        "industry_insights": "hybrid",
        
        # Business Strategist Configuration  
        "business_domain": "financial technology",
        "industry_vertical": "digital payments and fintech",
        "strategy_type": "comprehensive",
        "strategic_focus": "market_expansion",
        "strategy_approach": "data-driven with agile implementation",
        "business_experience": "enterprise fintech and payments industry",
        "strategic_objective": "market leadership in mobile payments",
        "priority_framework": "balanced",
        
        # Intelligence Reporter Configuration
        "reporting_domain": "fintech executive intelligence",
        "report_type": "briefing",
        "executive_audience": "C-suite executives and board members",
        "reporting_style": "hybrid",
        "communication_approach": "consultative",
        "presentation_format": "executive dashboard with narrative insights",
        "business_context": "rapid fintech market evolution and competitive pressure",
        "urgency_level": "quarterly",
        
        # Project-wide Intelligence Parameters
        "intelligence_priority": "competitive positioning and market opportunity",
        "confidentiality_level": "internal executive use",
        "distribution_scope": "senior leadership team",
        "update_frequency": "quarterly with monthly highlights"
    }
    
    print("✅ Advanced guardrails configured for fintech intelligence analysis")
    print()
    
    # 5. DEPLOY BUSINESS INTELLIGENCE SQUAD
    print("🚀 Deploying Business Intelligence Squad...")
    print("   📊 Market Analysis: Analyzing fintech and digital payments landscape")
    print("   🎯 Strategic Planning: Developing market expansion strategies")
    print("   📋 Executive Reporting: Creating C-suite intelligence briefing")
    print()
    
    try:
        # Deploy the BI squad with comprehensive guardrails
        result = bi_squad.deploy(guardrails=guardrails)
        
        print("🎉 Business Intelligence Analysis Completed!")
        print()
        print("📁 Intelligence Package Generated:")
        print("   • Market Analysis: outputs/business_intelligence/01_market_analysis.md")
        print("   • Strategic Plan: outputs/business_intelligence/02_strategic_plan.md") 
        print("   • Executive Report: outputs/business_intelligence/03_executive_report.html")
        print("   • Intelligence Package: outputs/business_intelligence/bi_intelligence_package.json")
        print()
        
        # 6. STORE INTELLIGENCE INSIGHTS IN MEMORY
        print("🧠 Storing Intelligence Insights...")
        
        market_analyst.remember(
            content="Fintech mobile payments showing 35% YoY growth with cryptocurrency integration as key differentiator",
            tags=["fintech", "mobile_payments", "growth_trends", "cryptocurrency", "market_intelligence"]
        )
        
        business_strategist.remember(
            content="Market expansion strategies require focus on regulatory compliance and user experience optimization",
            tags=["market_expansion", "fintech_strategy", "regulatory_compliance", "user_experience"]
        )
        
        intelligence_reporter.remember(
            content="Executive briefings on fintech require balance of technical innovation and business impact",
            tags=["executive_reporting", "fintech_intelligence", "business_communication"]
        )
        
        print("✅ Intelligence insights stored for future analysis")
        print()
        
        # 7. DEMONSTRATE ADVANCED FEATURES
        print("🎯 Advanced Framework Features Demonstrated:")
        print("   ✅ Complex conditional guardrails with select logic")
        print("   ✅ Multi-format outputs (Markdown, HTML, JSON)")
        print("   ✅ Business intelligence workflow simulation")
        print("   ✅ Memory-enabled collaborative intelligence")
        print("   ✅ Executive-level reporting and communication")
        print("   ✅ Strategic planning with market analysis integration")
        print("   ✅ Scalable guardrails for different analysis types")
        print("   ✅ Professional business use case demonstration")
        print()
        
        if result:
            print("📋 Executive Summary:")
            print(f"   {result[:250]}...")
        
        return result
        
    except Exception as e:
        print(f"❌ Error during BI squad deployment: {str(e)}")
        return None

def demonstrate_alternative_bi_focus():
    """
    Shows how the same BI squad can be reconfigured for different industries
    """
    print("\n" + "="*60)
    print("🔄 Alternative BI Configuration")
    print("="*60)
    
    alternative_guardrails = {
        "market_sector": "healthcare technology",
        "analysis_type": "trend",
        "market_focus": "telemedicine and digital health adoption",
        "analysis_depth": "executive",
        "industry_insights": "emerging",
        "strategy_type": "innovation",
        "strategic_focus": "market_entry",
        "report_type": "comprehensive",
        "urgency_level": "immediate"
    }
    
    print("✅ Same BI framework, different industry focus:")
    print("   Original: Fintech and digital payments analysis")
    print("   Alternative: Healthcare technology and telemedicine")
    print("🎯 Demonstrates framework flexibility across industries")

if __name__ == "__main__":
    result = main()
    demonstrate_alternative_bi_focus()
    
    print("\n" + "="*60)
    print("📊 Business Intelligence Squad Complete!")
    print("="*60)
    print("Demonstrated advanced multi-agent business intelligence capabilities:")
    print("• Complex conditional guardrails for flexible analysis")
    print("• Professional BI workflow with market analysis and strategy")
    print("• Multiple output formats for different stakeholder needs")
    print("• Memory-enabled intelligence accumulation")
    print("• Executive-level reporting and strategic communication")
    print("• Scalable framework for cross-industry intelligence")
