# TBH Secure Agents Examples

This directory contains comprehensive examples demonstrating the capabilities of the TBH Secure Agents framework. Each example is designed to showcase different aspects of the framework, from basic usage to advanced security features.

## 📁 **Directory Structure**

```
examples/
├── user_friendly/          # 🆕 NEW! Simple, ready-to-run examples
├── basic/                   # Basic framework functionality
├── advanced/                # Advanced features and configurations
└── security/                # Security-focused examples
```

## 🚀 **Quick Start - User-Friendly Examples**

**Perfect for beginners!** The `user_friendly/` directory contains 5 simple, diverse AI agent examples that are ready to run immediately:

### **Available Examples:**

| Example | AI Agent Type | Output Format | Description |
|---------|---------------|---------------|-------------|
| `1_ai_researcher.py` | **AI Researcher** | Markdown (.md) | Research any topic comprehensively |
| `2_ai_code_developer.py` | **AI Code Developer** | Python (.py) | Write code with specific requirements |
| `3_ai_business_analyst.py` | **AI Business Analyst** | JSON (.json) | Analyze business problems and strategies |
| `4_ai_marketing_strategist.py` | **AI Marketing Strategist** | HTML (.html) | Create marketing campaigns |
| `5_ai_financial_advisor.py` | **AI Financial Advisor** | PDF (.pdf) | Provide investment and financial advice |

### **How to Run:**

```bash
# Navigate to user-friendly examples
cd examples/user_friendly/

# Run any example (they all work out of the box!)
python3 1_ai_researcher.py
python3 2_ai_code_developer.py
python3 3_ai_business_analyst.py
python3 4_ai_marketing_strategist.py
python3 5_ai_financial_advisor.py

# Check the generated outputs
ls -la outputs/user_examples/
```

### **What You'll Learn:**

- ✅ **Proper Guardrails Usage**: Template variables in expert profiles and operations
- ✅ **Multiple File Formats**: .md, .py, .json, .html, .pdf outputs
- ✅ **Security Integration**: Minimal security settings for development
- ✅ **Real-World Applications**: Practical AI agents for different domains
- ✅ **Clean Code Patterns**: Simple, readable code without complexity

## 📚 **Other Example Categories**

### **Basic Examples** (`basic/`)

Simple examples demonstrating core framework functionality:
- Creating experts and operations
- Basic squad deployment
- Simple security configurations
- File output basics

### **Advanced Examples** (`advanced/`)

More complex examples showcasing advanced features:
- Complex multi-agent workflows
- Advanced guardrails with conditional logic
- Custom security profiles
- Integration patterns

### **Security Examples** (`security/`)

Examples focused on security features:
- Different security profiles in action
- Security validation demonstrations
- Attack prevention examples
- Hybrid security validation [BETA]

## 🛡️ **Security Profiles Used**

All examples use appropriate security profiles:

- **User-Friendly Examples**: `minimal` - Perfect for learning and development
- **Basic Examples**: `standard` - Balanced security for general use
- **Advanced Examples**: `high` - Strict security for sensitive applications
- **Security Examples**: `maximum` - Most stringent security validation

## 📋 **Prerequisites**

Before running any examples, ensure you have:

1. **Python 3.7+** installed
2. **TBH Secure Agents** framework installed:
   ```bash
   pip install tbh-secure-agents
   ```
3. **Google API Key** set as environment variable:
   ```bash
   export GOOGLE_API_KEY="your_api_key_here"
   ```

## 🔧 **Customization**

All examples are designed to be easily customizable:

### **Change the Expert Specialty:**
```python
# Original
researcher = Expert(
    specialty="AI Researcher specializing in {research_topic}",
    # ...
)

# Customized
researcher = Expert(
    specialty="Medical Researcher specializing in {research_topic}",
    # ...
)
```

### **Modify Guardrails:**
```python
# Original
guardrails = {
    "research_topic": "renewable energy technology",
    "research_depth": "comprehensive"
}

# Customized
guardrails = {
    "research_topic": "artificial intelligence ethics",
    "research_depth": "detailed"
}
```

### **Change Output Format:**
```python
# Change file extension to change format
result_destination="outputs/my_research.pdf"  # PDF output
result_destination="outputs/my_research.html" # HTML output
result_destination="outputs/my_research.json" # JSON output
```

## 📊 **Example Outputs**

When you run the user-friendly examples, you'll get real, usable outputs:

- **Research Reports**: Comprehensive, well-structured research with sources
- **Code Files**: Production-ready code with proper documentation
- **Business Analysis**: Strategic recommendations in structured format
- **Marketing Strategies**: Complete campaign plans with timelines
- **Financial Advice**: Professional investment recommendations

## 🆘 **Troubleshooting**

### **Common Issues:**

1. **API Key Not Set:**
   ```bash
   export GOOGLE_API_KEY="your_api_key_here"
   ```

2. **Permission Errors:**
   ```bash
   chmod +x *.py
   ```

3. **Missing Dependencies:**
   ```bash
   pip install tbh-secure-agents reportlab
   ```

4. **Output Directory Issues:**
   The examples automatically create output directories, but you can create them manually:
   ```bash
   mkdir -p outputs/user_examples
   ```

## 🎯 **Next Steps**

After trying the examples:

1. **Modify the examples** to fit your specific use cases
2. **Experiment with different security profiles** (minimal → standard → high)
3. **Try different file formats** by changing the result_destination
4. **Create your own AI agents** using the patterns from these examples
5. **Explore advanced features** in the other example directories

## 📖 **Documentation**

For more detailed information:
- [Usage Guide](../docs/usage_guide.md) - Core concepts and basic usage
- [Guardrails Guide](../docs/guardrails_comprehensive.md) - Advanced guardrails usage
- [Security Guide](../docs/security_guide.md) - Security best practices
- [Result Destination Guide](../docs/result_destination.md) - File output options

## 🤝 **Contributing**

Found an issue or want to add more examples? Please:
1. Check existing issues on GitHub
2. Create a new issue or pull request
3. Follow the existing code patterns and documentation style

Happy coding with TBH Secure Agents! 🚀
