# Best Practices Guide

This guide provides best practices for building secure, efficient, and maintainable AI agent systems with TBH Secure Agents.

## 🛡️ **Security Best Practices**

### **Choose Appropriate Security Profiles**

```python
# ✅ Good: Match security to use case
development_expert = Expert(
    specialty="Developer",
    security_profile="minimal"  # For development/testing
)

production_expert = Expert(
    specialty="Financial Analyst", 
    security_profile="high"  # For sensitive data
)

# ❌ Bad: Using minimal security in production
production_expert = Expert(
    specialty="Financial Analyst",
    security_profile="minimal"  # Too permissive for production
)
```

### **Secure API Key Management**

```python
# ✅ Good: Use environment variables
import os
os.environ["GOOGLE_API_KEY"] = "your_key"  # Only for testing

# ✅ Better: Set in shell
# export GOOGLE_API_KEY="your_key"

# ❌ Bad: Hardcoded in source
expert = Expert(
    specialty="Analyst",
    api_key="hardcoded_key_here"  # Never do this!
)
```

### **Input Validation**

```python
# ✅ Good: Validate inputs before processing
def create_analysis_expert(user_input):
    # Validate input
    if not user_input or len(user_input) > 1000:
        raise ValueError("Invalid input length")
    
    # Sanitize input
    clean_input = user_input.strip()
    
    return Expert(
        specialty=f"Analyst specializing in {clean_input}",
        security_profile="standard"
    )
```

## 🎯 **Expert Design Best Practices**

### **Clear and Specific Specialties**

```python
# ✅ Good: Specific and clear
expert = Expert(
    specialty="Python Developer specializing in web APIs",
    objective="Write clean, secure REST API code following PEP 8",
    background="Expert in Flask, FastAPI, and security best practices"
)

# ❌ Bad: Vague and unclear
expert = Expert(
    specialty="Developer",
    objective="Write code"
)
```

### **Use Template Variables for Flexibility**

```python
# ✅ Good: Flexible with template variables
expert = Expert(
    specialty="Content Writer specializing in {domain}",
    objective="Create {content_type} for {audience}",
    background="Expert in writing {tone} content about {domain}"
)

# ❌ Bad: Hardcoded and inflexible
expert = Expert(
    specialty="Content Writer specializing in technology",
    objective="Create blog posts for developers"
)
```

## 📝 **Operation Design Best Practices**

### **Clear and Detailed Instructions**

```python
# ✅ Good: Detailed and specific
operation = Operation(
    instructions="""
    Analyze the provided sales data and create a comprehensive report that includes:
    1. Top 5 performing products by revenue
    2. Monthly sales trends for the last 6 months
    3. Customer segment analysis
    4. Actionable recommendations for improvement
    
    Format the output as a professional business report with clear sections and bullet points.
    Do not include any customer names or personal information.
    """,
    expert=analyst
)

# ❌ Bad: Vague and unclear
operation = Operation(
    instructions="Analyze the sales data",
    expert=analyst
)
```

### **Appropriate Output Formats**

```python
# ✅ Good: Match format to content
code_operation = Operation(
    instructions="Create a Python web scraper",
    output_format="Complete Python code with comments and error handling",
    expert=developer,
    result_destination="scraper.py"  # Python file for code
)

report_operation = Operation(
    instructions="Create a business analysis report",
    output_format="Professional report with sections and recommendations",
    expert=analyst,
    result_destination="report.pdf"  # PDF for formal reports
)
```

## 🔧 **Guardrails Best Practices**

### **Use Meaningful Variable Names**

```python
# ✅ Good: Clear variable names
guardrails = {
    "analysis_timeframe": "last 6 months",
    "target_audience": "executive leadership",
    "report_format": "executive summary",
    "include_recommendations": True,
    "confidentiality_level": "internal use only"
}

# ❌ Bad: Unclear variable names
guardrails = {
    "time": "6 months",
    "people": "executives",
    "format": "summary"
}
```

### **Validate Guardrail Inputs**

```python
# ✅ Good: Validate guardrail values
def validate_guardrails(guardrails):
    required_keys = ["topic", "audience", "tone"]
    for key in required_keys:
        if key not in guardrails:
            raise ValueError(f"Missing required guardrail: {key}")
    
    if guardrails["tone"] not in ["formal", "casual", "technical"]:
        raise ValueError("Invalid tone value")
    
    return guardrails

# Use validation
guardrails = validate_guardrails({
    "topic": "AI trends",
    "audience": "developers", 
    "tone": "technical"
})
```

## 📁 **File Management Best Practices**

### **Organized Directory Structure**

```python
# ✅ Good: Organized structure
import os

# Create organized directories
os.makedirs("outputs/reports/monthly", exist_ok=True)
os.makedirs("outputs/code/scripts", exist_ok=True)
os.makedirs("outputs/data/analysis", exist_ok=True)

# Use descriptive filenames with timestamps
from datetime import datetime
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

operation = Operation(
    instructions="Generate monthly sales report",
    expert=analyst,
    result_destination=f"outputs/reports/monthly/sales_report_{timestamp}.pdf"
)
```

### **Handle File Permissions**

```python
# ✅ Good: Check and handle file permissions
import os
import stat

def ensure_writable_directory(path):
    os.makedirs(path, exist_ok=True)
    # Ensure directory is writable
    os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IROTH | stat.S_IXOTH)

ensure_writable_directory("outputs/reports")
```

## 🔄 **Error Handling Best Practices**

### **Comprehensive Error Handling**

```python
# ✅ Good: Comprehensive error handling
def execute_analysis_safely(operation, guardrails=None):
    try:
        result = operation.execute(guardrails=guardrails)
        return {"success": True, "result": result}
    
    except SecurityError as e:
        logger.error(f"Security validation failed: {e}")
        return {"success": False, "error": "Security check failed", "details": str(e)}
    
    except APIError as e:
        logger.error(f"API error: {e}")
        return {"success": False, "error": "API communication failed", "retry": True}
    
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return {"success": False, "error": "Unexpected error occurred"}

# Use the safe execution
result = execute_analysis_safely(analysis_operation, guardrails)
if result["success"]:
    print("Analysis completed successfully!")
else:
    print(f"Analysis failed: {result['error']}")
```

### **Logging Best Practices**

```python
# ✅ Good: Structured logging
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('tbh_agents.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Log important events
logger.info(f"Starting operation: {operation.instructions[:50]}...")
logger.info(f"Using security profile: {expert.security_profile}")
logger.info(f"Operation completed successfully in {execution_time:.2f}s")
```

## 🚀 **Performance Best Practices**

### **Optimize Instructions**

```python
# ✅ Good: Concise but complete instructions
operation = Operation(
    instructions="Summarize the key findings from the attached research paper in 3 bullet points",
    expert=researcher
)

# ❌ Bad: Overly verbose instructions
operation = Operation(
    instructions="""
    Please read through the entire research paper that I have attached to this request
    and then provide me with a comprehensive summary that covers all the important
    points but also make sure to keep it concise and not too long but also not too
    short and make sure you include the most important findings...
    """,
    expert=researcher
)
```

### **Use Appropriate Security Profiles**

```python
# ✅ Good: Match security to environment
if environment == "development":
    security_profile = "minimal"  # Faster for development
elif environment == "production":
    security_profile = "high"     # Secure for production
```

## 🧪 **Testing Best Practices**

### **Test with Different Security Profiles**

```python
# ✅ Good: Test across security profiles
def test_operation_across_profiles():
    profiles = ["minimal", "standard", "high"]
    
    for profile in profiles:
        expert = Expert(
            specialty="Test Analyst",
            security_profile=profile
        )
        
        operation = Operation(
            instructions="Analyze test data",
            expert=expert
        )
        
        try:
            result = operation.execute()
            print(f"✅ {profile} profile: Success")
        except Exception as e:
            print(f"❌ {profile} profile: Failed - {e}")
```

### **Validate Outputs**

```python
# ✅ Good: Validate operation outputs
def validate_analysis_output(result):
    """Validate that analysis output meets requirements"""
    if not result:
        return False, "Empty result"
    
    if len(result) < 100:
        return False, "Result too short"
    
    required_sections = ["summary", "findings", "recommendations"]
    for section in required_sections:
        if section.lower() not in result.lower():
            return False, f"Missing {section} section"
    
    return True, "Valid output"

# Use validation
result = operation.execute()
is_valid, message = validate_analysis_output(result)
if not is_valid:
    print(f"Output validation failed: {message}")
```

## 📚 **Documentation Best Practices**

### **Document Your Experts**

```python
# ✅ Good: Well-documented expert
class FinancialAnalyst:
    """
    Financial analysis expert for investment recommendations.
    
    Security Profile: high (handles sensitive financial data)
    Use Cases: Investment analysis, risk assessment, portfolio optimization
    Limitations: Cannot provide personalized financial advice
    """
    
    def __init__(self):
        self.expert = Expert(
            specialty="Financial Analyst specializing in investment analysis",
            objective="Provide data-driven investment insights and risk assessments",
            background="Expert in financial markets, risk analysis, and investment strategies",
            security_profile="high"
        )
```

### **Comment Complex Guardrails**

```python
# ✅ Good: Documented guardrails
guardrails = {
    # Analysis parameters
    "timeframe": "last 12 months",        # Historical data period
    "risk_tolerance": "moderate",          # Client risk preference
    
    # Output formatting
    "report_format": "executive_summary",  # Format for stakeholders
    "include_charts": True,                # Visual representations
    
    # Compliance requirements
    "regulatory_compliance": "SEC",        # Regulatory framework
    "confidentiality": "restricted"       # Data handling level
}
```

## 🔄 **Maintenance Best Practices**

### **Regular Updates**

```python
# ✅ Good: Check for updates regularly
# pip install --upgrade tbh-secure-agents

# Version compatibility check
import tbh_secure_agents
print(f"Framework version: {tbh_secure_agents.__version__}")
```

### **Monitor Performance**

```python
# ✅ Good: Monitor execution times
import time

start_time = time.time()
result = operation.execute()
execution_time = time.time() - start_time

logger.info(f"Operation completed in {execution_time:.2f} seconds")

# Alert if execution takes too long
if execution_time > 30:  # 30 seconds threshold
    logger.warning(f"Slow operation detected: {execution_time:.2f}s")
```

## 🎯 **Summary**

Following these best practices will help you:
- ✅ Build more secure AI agent systems
- ✅ Create maintainable and readable code
- ✅ Optimize performance and reliability
- ✅ Handle errors gracefully
- ✅ Test thoroughly across different scenarios

Remember: Start simple, test thoroughly, and gradually add complexity as needed!
