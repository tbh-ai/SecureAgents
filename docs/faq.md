# Frequently Asked Questions (FAQ)

## 🚀 **Getting Started**

### **Q: How do I get started with TBH Secure Agents?**
A: Follow these simple steps:
1. Install: `pip install tbh-secure-agents`
2. Set API key: `export GOOGLE_API_KEY="your_key"`
3. Try the [Quick Start Guide](./quick_start.md) or run the user-friendly examples

### **Q: Do I need coding experience to use this framework?**
A: Basic Python knowledge is helpful, but our user-friendly examples are designed for beginners. Start with the examples in `examples/user_friendly/` - they're simple and well-documented.

### **Q: What's the difference between Expert, Operation, and Squad?**
A: 
- **Expert**: An AI agent with specific skills (like "Data Analyst" or "Writer")
- **Operation**: A task for an expert to complete (like "analyze this data")
- **Squad**: A team of experts working together on multiple operations

## 🔑 **API Keys & Setup**

### **Q: Where do I get a Google API key?**
A: Go to [Google AI Studio](https://aistudio.google.com/), sign in, and click "Get API Key". It's free to start.

### **Q: Can I use other AI models besides Google Gemini?**
A: Currently, the framework is optimized for Google Gemini. Support for other models may be added in future versions.

### **Q: Is my API key secure?**
A: Yes, when you use environment variables. Never hardcode API keys in your source code. The framework handles API communication securely.

## 🛡️ **Security**

### **Q: What security profiles should I use?**
A: 
- **minimal**: Perfect for learning and development
- **standard**: Good for general applications (default)
- **high**: Use for sensitive business data
- **maximum**: For highly regulated industries

### **Q: Why did my operation fail security validation?**
A: The security system protects against potentially harmful content. Try:
1. Using `security_profile="minimal"` for development
2. Reviewing your instructions for problematic content
3. Checking the error message for specific guidance

### **Q: Can I disable security features?**
A: Security features are core to the framework and cannot be completely disabled. However, `minimal` security profile provides the most permissive settings for development.

## 📁 **File Formats & Outputs**

### **Q: What file formats are supported for outputs?**
A: All major formats:
- `.md` (Markdown)
- `.py` (Python code)
- `.json` (JSON data)
- `.html` (Web pages)
- `.pdf` (Documents)
- `.txt` (Plain text)
- `.csv` (Spreadsheets)

### **Q: Where are my output files saved?**
A: Files are saved to the path you specify in `result_destination`. The framework automatically creates directories if they don't exist.

### **Q: Can I save outputs to cloud storage?**
A: Currently, outputs are saved locally. You can then upload them to cloud storage using standard Python libraries.

## 🔧 **Guardrails**

### **Q: What are guardrails and why should I use them?**
A: Guardrails let you control AI behavior dynamically using template variables. Instead of hardcoding instructions, you can make them flexible:

```python
# With guardrails
instructions="Write a {content_type} about {topic} for {audience}"
guardrails={"content_type": "blog post", "topic": "AI", "audience": "beginners"}
```

### **Q: How do template variables work?**
A: Put variables in curly braces `{variable_name}` in your expert profiles or operation instructions. Then provide values in the guardrails dictionary.

### **Q: Can I use conditional logic in guardrails?**
A: Yes! Use the select syntax:
```python
instructions="""
{tone, select,
  formal:Use professional language|
  casual:Use friendly, conversational language
}
"""
```

## 🎯 **Examples & Use Cases**

### **Q: What examples are available?**
A: We have 5 user-friendly examples:
1. **AI Researcher** - Research any topic
2. **AI Code Developer** - Write code
3. **AI Business Analyst** - Business analysis
4. **AI Marketing Strategist** - Marketing campaigns
5. **AI Financial Advisor** - Financial advice

### **Q: Can I modify the examples for my needs?**
A: Absolutely! The examples are designed to be customized. Change the expert specialties, guardrails, or instructions to fit your specific use case.

### **Q: What are some real-world applications?**
A: 
- **Content Creation**: Blogs, articles, social media posts
- **Code Generation**: Scripts, APIs, documentation
- **Business Analysis**: Market research, strategy planning
- **Data Analysis**: Reports, insights, visualizations
- **Customer Support**: FAQ responses, help documentation

## 🐛 **Troubleshooting**

### **Q: I'm getting import errors. What should I do?**
A: Try:
1. `pip install --upgrade tbh-secure-agents`
2. Check Python version (3.7+ required)
3. Restart your Python environment

### **Q: My operations are taking too long. How can I speed them up?**
A: 
1. Use shorter, more specific instructions
2. Try `security_profile="minimal"` for development
3. Reduce output length requirements
4. Check your internet connection

### **Q: I'm getting "API quota exceeded" errors.**
A: You've hit Google's API limits. Wait a bit or upgrade your Google AI Studio plan for higher quotas.

### **Q: The AI output isn't what I expected. How can I improve it?**
A: 
1. Make instructions more specific and detailed
2. Use guardrails to control behavior
3. Provide examples in your instructions
4. Adjust the expert's specialty and objective

## 💡 **Best Practices**

### **Q: How should I structure my AI workflows?**
A: Start simple:
1. **Single Operation**: One expert, one task
2. **Sequential Operations**: Chain tasks together
3. **Complex Workflows**: Use squads for multi-expert collaboration

### **Q: How do I handle errors gracefully?**
A: Always use try-catch blocks:
```python
try:
    result = operation.execute()
    print("Success!")
except Exception as e:
    print(f"Error: {e}")
```

### **Q: Should I use squads or individual operations?**
A: 
- **Individual Operations**: For simple, standalone tasks
- **Squads**: When you need multiple experts or complex workflows

## 🔄 **Updates & Support**

### **Q: How do I update to the latest version?**
A: `pip install --upgrade tbh-secure-agents`

### **Q: Where can I get help if I'm stuck?**
A: 
1. Check this FAQ and documentation
2. Try the examples in `examples/user_friendly/`
3. Open an issue on GitHub
4. Contact support at saish.shinde.jb@gmail.com

### **Q: How do I report bugs or request features?**
A: Open an issue on the [GitHub repository](https://github.com/saishshinde15/tbh.ai_SecureAgents-Developer_Edition-Alpha.git) with:
- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Your Python and framework versions

### **Q: Is there a community or forum?**
A: Currently, GitHub issues are the main support channel. A community forum may be added based on user demand.

## 🚀 **Advanced Usage**

### **Q: Can I create custom security profiles?**
A: This is a beta feature. Check the [Security Guide](./security_guide.md) for advanced security configuration options.

### **Q: How do I integrate this with my existing applications?**
A: The framework is designed to be modular. You can integrate individual experts and operations into existing Python applications easily.

### **Q: Can I run this in production?**
A: Yes, but use appropriate security profiles (`high` or `maximum`) and follow security best practices. Test thoroughly before deployment.

---

**Still have questions?** Check our [documentation](./index.md) or contact us at saish.shinde.jb@gmail.com
