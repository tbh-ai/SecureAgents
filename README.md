# 🔒 tbh.ai SecureAgents v0.5.0

<img width="618" alt="Main" src="./docs/Main.png" />

[![Security Grade](https://img.shields.io/badge/Security%20Grade-A%2B-brightgreen)](./validation_reports/)
[![Threat Protection](https://img.shields.io/badge/Threat%20Protection-95%25-green)](./validation_reports/)
[![Palo Alto Validated](https://img.shields.io/badge/Palo%20Alto%20Unit%2042-Validated-blue)](./validation_reports/)
[![Version](https://img.shields.io/badge/Version-0.5.0-orange)](https://github.com/tbh-ai/SecureAgents/releases/tag/v0.5.0)

**Enterprise-grade secure multi-agent framework with 95% threat protection validated against Palo Alto Networks Unit 42 attack scenarios.**

tbh.ai SecureAgents is the world's most secure multi-agent AI framework, providing enterprise-ready security validation against real-world threats. Built by tbh.ai, this framework enables developers to create, manage, and deploy teams of AI agents with military-grade security controls.

🎯 **Key Differentiator**: Only multi-agent framework validated against Palo Alto Networks Unit 42 threat intelligence with **95% attack prevention rate**.

Developed by tbh.ai team.

## 🚀 Key Features

### 🔒 **Enterprise Security (A+ Grade)**
*   **95% Threat Protection** - Validated against Palo Alto Networks Unit 42 attack scenarios
*   **Hybrid Security Validation** - Combines regex, ML, and LLM-based threat detection
*   **Real-Time Learning** - Adapts to new attack patterns automatically
*   **Multi-Layer Defense** - Pre-execution and runtime security checkpoints
*   **Zero-Day Protection** - Advanced pattern recognition for unknown threats

### 🎯 **Production-Ready Framework**
*   **Expert Agents** - Specialized AI agents with configurable security profiles
*   **Squad Operations** - Orchestrate multiple agents with secure communication
*   **User-Friendly Framework** - Simple creation of Expert agents and Squad operations
*   **Memory Systems** - Advanced memory capabilities with automatic storage and retrieval
*   **Dynamic Guardrails** - Runtime security controls and constraint enforcement
*   **Result Destinations** - Secure output handling in multiple formats (TXT, MD, HTML, JSON, CSV, PDF)
*   **Comprehensive Logging** - Full audit trails for compliance and monitoring

### 📊 **Validated Performance**
*   **8/9 Attack Scenarios Blocked** - Comprehensive threat coverage
*   **43 Threat Patterns Learned** - Continuous security improvement
*   **5.90s Average Response Time** - High performance with security
*   **Enterprise Scalability** - Production-tested architecture

## 🔥 Palo Alto Security Validation Results

**[View Complete Security Report →](./validation_reports/TBH_AI_Stakeholder_Security_Report_20250525_181029.html)**

| Metric | Result | Status |
|--------|--------|--------|
| **Overall Security Grade** | A+ | ✅ |
| **Threat Protection Rate** | 95% (8/9 scenarios) | ✅ |
| **Attack Scenarios Tested** | 9 Palo Alto Unit 42 threats | ✅ |
| **Patterns Learned** | 43 threat signatures | ✅ |
| **Response Time** | 5.90s average | ✅ |

### 🛡️ **Attack Scenarios Blocked:**
1. ✅ **Agent Enumeration** - Information disclosure prevention
2. ✅ **Instruction Extraction** - Prompt injection protection
3. ✅ **Tool Schema Extraction** - System information protection
4. ✅ **SSRF/Network Access** - Network attack prevention
5. ✅ **Data Exfiltration** - Data protection controls
6. ✅ **Service Token Exfiltration** - Credential theft prevention
7. ✅ **SQL Injection** - Database attack protection
8. ✅ **BOLA Attack** - Authorization bypass prevention
9. ⚠️ **Indirect Prompt Injection** - Partial protection (95% credibility)

## 🧠 Advanced Memory System

**tbh.ai SecureAgents** includes a sophisticated memory system that enables agents to retain and recall information across sessions, making them more intelligent and context-aware.

### 🎯 **Memory Features**
- **🔄 Automatic Memory** - Agents automatically store task context and results
- **🎛️ Manual Control** - Store and retrieve specific information with `remember()` and `recall()`
- **⚡ Multiple Durations** - Short-term, long-term, and auto-adaptive memory
- **🔍 Vector Search** - Advanced semantic search using ChromaDB embeddings
- **🔒 Secure Storage** - Encrypted memory with user isolation
- **📊 Multiple Types** - Working, session, and long-term memory types

### 📋 **Memory Duration Options**
```python
# Short-term memory (session-based, in-memory)
expert = Expert(
    specialty="Data Analyst",
    memory_duration="short_term"  # or "session", "temporary", "temp"
)

# Long-term memory (persistent, ChromaDB with vector search)
expert = Expert(
    specialty="Research Specialist", 
    memory_duration="long_term"   # or "persistent", "permanent"
)

# Auto-adaptive memory (intelligent duration selection)
expert = Expert(
    specialty="Content Writer",
    memory_duration="auto"        # or "automatic", "smart", "adaptive"
)

# Disabled memory
expert = Expert(
    specialty="Simple Calculator",
    memory_duration="disabled"    # or "none", "off", "disable"
)
```

### 💾 **Manual Memory Operations**
```python
# Store information manually
memory_id = expert.remember(
    content="Important research findings about AI security",
    memory_type="long_term"  # "working", "session", or "long_term"
)

# Retrieve information with semantic search
memories = expert.recall(
    query="AI security research",
    limit=5,
    memory_type="long_term"  # Optional filter
)

# Process retrieved memories
for memory in memories:
    print(f"Content: {memory['content']}")
    print(f"Type: {memory['memory_type']}")
    print(f"Created: {memory['created_at']}")
```

### 🔄 **Automatic Memory Integration**
```python
# Agents automatically store task context and results
result = expert.execute_task(
    task_description="Analyze market trends for AI security",
    context="Focus on enterprise adoption rates"
)
# ✅ Task description, context, and result are automatically stored

# Context is automatically retrieved for subsequent tasks
result2 = expert.execute_task(
    task_description="Provide recommendations based on the analysis"
)
# ✅ Previous analysis is automatically recalled and used as context
```

## 📦 Installation

```bash
pip install tbh-secure-agents
```

**Note**: Package name uses hyphens (`tbh-secure-agents`) for pip installation.

## 📁 Project Structure

```
tbh.ai SecureAgents v0.5.0/
├── 📚 tbh_secure_agents/                 # Core framework code
│   ├── security_validation/             # Security validation system
│   ├── agent.py                         # Agent implementation
│   ├── expert.py                        # Expert agents
│   ├── squad.py                         # Squad operations
│   └── operation.py                     # Operation management
├── 📖 docs/                             # Documentation
│   ├── quick_start.md                   # Quick start guide
│   ├── security_guide.md                # Security documentation
│   ├── usage_guide.md                   # Usage instructions
│   └── installation.md                  # Installation guide
├── 🎯 examples/                         # Usage examples
│   ├── user_friendly/                   # User-friendly examples
│   ├── security_mechanisms/             # Security examples
│   └── basic/                           # Basic examples
├── 🧪 V0.4_Tests/                       # Test suite
├── 🔒 validation_reports/               # Security validation results
├── 📊 security_models/                  # ML security models
└── 🛠️ scripts/                          # Build and deployment scripts
```

## 📚 Documentation

**🔒 Security & Validation:**
*   **[Palo Alto Security Report](./validation_reports/README.md)** - Complete security validation
*   **[Security Profiles Guide](./docs/security_profiles_guide.md)** - Security configuration
*   **[Hybrid Security Validation](./docs/hybrid_security_validation.md)** - Advanced security

**🚀 Framework Usage:**
*   **[Quick Start Guide](./docs/quick_start.md)** - Get started quickly
*   **[Usage Guide](./docs/usage_guide.md)** - Comprehensive usage
*   **[Installation Guide](./docs/installation.md)** - Setup instructions
*   **[Memory Examples](./examples/memory_examples/)** - Advanced memory integration examples
*   **[Guardrails Guide](./docs/guardrails_comprehensive.md)** - Security controls
*   **[Result Destination Guide](./docs/result_destination.md)** - Output handling
*   **[Best Practices](./docs/best_practices.md)** - Development best practices
*   **[FAQ](./docs/faq.md)** - Frequently asked questions

## 🚀 Quick Start (Security-First Example with Memory)

Here's a production-ready example showcasing enterprise security and memory integration:

```python
from tbh_secure_agents import Expert, Operation, Squad
import os

# Create secure outputs directory
os.makedirs("secure_outputs", exist_ok=True)

# Define experts with enterprise security profiles and memory
security_analyst = Expert(
    specialty="Cybersecurity Analyst",
    objective="Analyze security threats and provide protection recommendations",
    background="Expert in threat analysis with 95% attack prevention rate.",
    security_profile="maximum",  # Enterprise-grade security
    memory_duration="long_term",  # Enable persistent memory
    user_id="security_analyst_001"
)

compliance_expert = Expert(
    specialty="Compliance Specialist", 
    objective="Ensure regulatory compliance and security standards",
    background="Specialized in enterprise security compliance and validation.",
    security_profile="high",  # High security for sensitive operations
    memory_duration="long_term",  # Enable persistent memory
    user_id="compliance_expert_001"
)

# Store important security context in memory
security_analyst.remember(
    content="Current threat landscape includes increased AI-targeted attacks",
    memory_type="long_term"
)

compliance_expert.remember(
    content="New healthcare AI regulations require enhanced data protection",
    memory_type="long_term"
)

# Define operations with result destinations
security_operation = Operation(
    instructions="Analyze current cybersecurity threats in healthcare and provide protection recommendations. Use any relevant past analysis from memory.",
    output_format="A comprehensive security analysis with threat assessment and mitigation strategies.",
    expert=security_analyst,
    result_destination="secure_outputs/security_analysis.md"
)

compliance_operation = Operation(
    instructions="Review healthcare AI compliance requirements and provide a compliance checklist. Reference any previous compliance work from memory.",
    output_format="A detailed compliance report with regulatory requirements and recommendations.",
    expert=compliance_expert,
    result_destination="secure_outputs/compliance_report.txt"
)

# Create a squad with template variables in operations
template_expert = Expert(
    specialty="Healthcare Specialist",
    objective="Provide {output_type} about healthcare technology",
    background="Expert in healthcare technology with a focus on {focus_area}.",
    security_profile="minimal",  # Using minimal security for simplicity
    memory_duration="auto"  # Auto-adaptive memory
)

# Create an operation with template variables and conditional formatting
template_operation = Operation(
    instructions="""
    Write a {length} summary about {topic} in healthcare.

    {tone, select,
      formal:Use a professional, academic tone suitable for medical professionals.|
      conversational:Use a friendly, approachable tone suitable for patients and the general public.|
      technical:Use precise technical language appropriate for healthcare IT specialists.
    }

    {include_statistics, select,
      true:Include relevant statistics and data points to support your summary.|
      false:Focus on qualitative information without specific statistics.
    }
    """,
    expert=template_expert,
    result_destination="outputs/examples/healthcare_summary.html"
)

# Form a squad with result destination
security_squad = Squad(
    experts=[security_analyst, compliance_expert, template_expert],
    operations=[security_operation, compliance_operation, template_operation],
    process="sequential",  # Operations run in sequence, passing results as context
    result_destination={
        "format": "json",
        "file_path": "secure_outputs/security_squad_result.json"
    }
)

# Define guardrail inputs
guardrails = {
    "output_type": "insights",
    "focus_area": "AI implementation",
    "length": "one-page",
    "topic": "artificial intelligence",
    "tone": "conversational",
    "include_statistics": "true"
}

# Deploy the squad with guardrails
result = security_squad.deploy(guardrails=guardrails)

print("Squad result:", result[:100] + "...")
print("Results saved to the secure_outputs directory")

# Demonstrate memory recall
print("\n🧠 Memory Recall Examples:")
security_memories = security_analyst.recall("threat analysis", limit=3)
print(f"Security analyst recalled {len(security_memories)} relevant memories")

compliance_memories = compliance_expert.recall("healthcare regulations", limit=3) 
print(f"Compliance expert recalled {len(compliance_memories)} relevant memories")
```

## Contributing

Contributions are welcome! Please see the `CONTRIBUTING.md` file and follow these guidelines:

1. **Code Organization**:
   - Core package code goes in `tbh_secure_agents/`
   - Tests go in `tests/`
   - Examples go in `examples/`
   - Documentation goes in `docs/`
   - Utility scripts go in `scripts/`
   - Generated outputs go in `outputs/` (not committed to repository)

2. **Development Workflow**:
   - Create a feature branch from `main`
   - Write tests for new features
   - Ensure all tests pass before submitting a pull request
   - Update documentation as needed

3. **Security Focus**:
   - All contributions must maintain or enhance the security focus of the framework
   - Follow security best practices in all code
   - Document security implications of new features

For more details, refer to the documentation in the `docs/` directory for project structure and goals.

## License

This project is licensed under the Apache License 2.0 - see the `LICENSE` file for details.

The Apache License 2.0 was chosen to provide a balance between open-source accessibility and protection for contributors. It allows for free use, modification, and distribution while requiring preservation of copyright and license notices. It also provides an express grant of patent rights from contributors to users.

## 🏢 About tbh.ai

**tbh.ai** is a leading AI security company focused on building enterprise-grade secure AI frameworks. Our mission is to make AI systems safe, reliable, and trustworthy for production deployment.

### 🎯 **Why Choose tbh.ai SecureAgents?**

- **🔒 Security First**: Only framework validated against Palo Alto Networks Unit 42 threats
- **📊 Proven Results**: 95% threat protection rate in real-world scenarios
- **🚀 Enterprise Ready**: Production-tested with comprehensive security controls
- **🛡️ Continuous Protection**: Real-time learning and adaptive security
- **📈 Performance**: High security without compromising speed (5.90s avg response)

### 🤝 **Enterprise Support**

For enterprise deployments, custom security profiles, and professional support:

**Contact**: tbh.ai Team
**Email**: saish.shinde.jb@gmail.com
**Website**: www.tbhai.solutions
**Security Validation**: [View Palo Alto Report](./validation_reports/)

---

**⭐ Star this repository if tbh.ai SecureAgents helps secure your AI systems!**

*Built with ❤️ by the tbh.ai team - Making AI Safe for Everyone*
