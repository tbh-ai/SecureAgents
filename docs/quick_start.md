# Quick Start Guide

Get up and running with TBH Secure Agents in minutes! This guide will walk you through the basics and get you creating AI agents right away.

## 🚀 **Installation**

```bash
pip install tbh-secure-agents
```

## 🔑 **Setup API Key**

```bash
# Set your Google API key
export GOOGLE_API_KEY="your_google_api_key_here"
```

Or in Python:
```python
import os
os.environ["GOOGLE_API_KEY"] = "your_google_api_key_here"
```

## 🎯 **Your First AI Agent in 30 Seconds**

```python
from tbh_secure_agents import Expert, Operation

# Create an AI expert
researcher = Expert(
    specialty="AI Researcher",
    objective="Research topics and provide comprehensive information",
    security_profile="minimal"  # Perfect for getting started
)

# Create a task for the expert
research_task = Operation(
    instructions="Research the benefits of renewable energy technology",
    output_format="A comprehensive report with key findings",
    expert=researcher,
    result_destination="my_research_report.md"  # Saves output automatically
)

# Execute the task
result = research_task.execute()
print("Research completed! Check my_research_report.md for the full report.")
```

## 🎨 **Try Different Types of AI Agents**

### **AI Code Developer**
```python
developer = Expert(
    specialty="Python Developer",
    objective="Write clean, well-documented code",
    security_profile="minimal"
)

code_task = Operation(
    instructions="Create a simple web scraper using Python requests",
    output_format="Complete Python code with comments",
    expert=developer,
    result_destination="web_scraper.py"
)

result = code_task.execute()
```

### **AI Business Analyst**
```python
analyst = Expert(
    specialty="Business Analyst",
    objective="Analyze business problems and provide strategic recommendations",
    security_profile="minimal"
)

analysis_task = Operation(
    instructions="Analyze the challenges of remote work and suggest solutions",
    output_format="Business analysis with actionable recommendations",
    expert=analyst,
    result_destination="business_analysis.json"
)

result = analysis_task.execute()
```

## 🛡️ **Using Guardrails for Dynamic Control**

Guardrails let you control your AI agents dynamically using template variables:

```python
# Expert with template variables
writer = Expert(
    specialty="Content Writer specializing in {topic_area}",
    objective="Write {content_type} for {target_audience}",
    security_profile="minimal"
)

# Operation with template variables
writing_task = Operation(
    instructions="Write a {content_type} about {specific_topic} for {target_audience}. Use a {tone} tone and keep it {length}.",
    output_format="Well-structured {content_type}",
    expert=writer,
    result_destination="content_output.md"
)

# Guardrails define the values for template variables
guardrails = {
    "topic_area": "technology",
    "content_type": "blog post",
    "target_audience": "tech enthusiasts",
    "specific_topic": "artificial intelligence trends",
    "tone": "engaging and informative",
    "length": "medium-length"
}

# Execute with guardrails
result = writing_task.execute(guardrails=guardrails)
```

## 📁 **File Formats Supported**

Save your AI outputs in any format:

```python
# Markdown
result_destination="report.md"

# Python code
result_destination="script.py"

# JSON data
result_destination="data.json"

# HTML page
result_destination="webpage.html"

# PDF document
result_destination="document.pdf"

# Plain text
result_destination="notes.txt"

# CSV data
result_destination="spreadsheet.csv"
```

## 🔒 **Security Profiles**

Choose the right security level for your needs:

| Profile | When to Use | Example |
|---------|-------------|---------|
| **minimal** | Learning, development, testing | `security_profile="minimal"` |
| **standard** | General applications (default) | `security_profile="standard"` |
| **high** | Sensitive data, business applications | `security_profile="high"` |
| **maximum** | Highly sensitive, regulated industries | `security_profile="maximum"` |

## 🎯 **Ready-to-Run Examples**

Try our 5 complete examples:

```bash
# Navigate to examples
cd examples/user_friendly/

# Try any of these:
python3 1_ai_researcher.py      # Research any topic
python3 2_ai_code_developer.py  # Write code
python3 3_ai_business_analyst.py # Business analysis
python3 4_ai_marketing_strategist.py # Marketing campaigns
python3 5_ai_financial_advisor.py # Financial advice
```

Each example demonstrates:
- ✅ Different AI agent types
- ✅ Proper guardrails usage
- ✅ Multiple file formats
- ✅ Real, usable outputs

## 🔧 **Common Patterns**

### **Research → Analysis → Report**
```python
# Step 1: Research
researcher = Expert(specialty="Researcher", security_profile="minimal")
research = Operation(
    instructions="Research {topic}",
    expert=researcher,
    result_destination="research.md"
)

# Step 2: Analysis
analyst = Expert(specialty="Data Analyst", security_profile="minimal")
analysis = Operation(
    instructions="Analyze the research findings and identify key trends",
    expert=analyst,
    result_destination="analysis.json"
)

# Step 3: Report
writer = Expert(specialty="Report Writer", security_profile="minimal")
report = Operation(
    instructions="Create an executive summary based on the analysis",
    expert=writer,
    result_destination="executive_summary.pdf"
)

# Execute in sequence
research_result = research.execute(guardrails={"topic": "AI trends"})
analysis_result = analysis.execute()
final_report = report.execute()
```

### **Code Generation with Requirements**
```python
developer = Expert(
    specialty="Software Developer specializing in {language}",
    objective="Write {code_type} following {standards}",
    security_profile="minimal"
)

code_task = Operation(
    instructions="Create a {code_type} in {language} that {functionality}. Follow {standards} and include {requirements}.",
    expert=developer,
    result_destination="generated_code.{extension}"
)

guardrails = {
    "language": "Python",
    "code_type": "web API",
    "standards": "PEP 8",
    "functionality": "handles user authentication",
    "requirements": "error handling and documentation",
    "extension": "py"
}

result = code_task.execute(guardrails=guardrails)
```

## 🆘 **Troubleshooting**

### **Common Issues:**

1. **API Key Error:**
   ```bash
   export GOOGLE_API_KEY="your_actual_api_key"
   ```

2. **Import Error:**
   ```bash
   pip install --upgrade tbh-secure-agents
   ```

3. **File Permission Error:**
   ```bash
   mkdir -p outputs
   chmod 755 outputs
   ```

4. **Security Validation Error:**
   - Try using `security_profile="minimal"` for development
   - Check your instructions for potentially problematic content

## 📚 **Next Steps**

1. **Explore Examples**: Try all 5 user-friendly examples
2. **Read Documentation**: Check out the [Usage Guide](./usage_guide.md)
3. **Experiment**: Modify examples to fit your needs
4. **Security**: Learn about [Security Profiles](./security_guide.md)
5. **Advanced Features**: Explore [Guardrails](./guardrails_comprehensive.md)

## 🎉 **You're Ready!**

You now know enough to start building powerful AI agent systems with TBH Secure Agents. The framework handles the complexity while you focus on creating amazing AI applications.

**Happy coding!** 🚀
