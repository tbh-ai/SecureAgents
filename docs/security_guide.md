# Security Guide for TBH Secure Agents Framework

This guide provides practical instructions for using the security features of the TBH Secure Agents framework to build secure multi-agent systems.

> **Note**: Some features described in this guide are currently in beta and may not be available in the public release. These features are marked with [BETA].

## Table of Contents

1. [Getting Started with Security](#getting-started-with-security)
2. [Choosing Security Profiles](#choosing-security-profiles)
3. [Creating Secure Experts](#creating-secure-experts)
4. [Securing Operations](#securing-operations)
5. [Building Secure Squads](#building-secure-squads)
6. [Advanced Security Configuration](#advanced-security-configuration)
7. [Security Best Practices](#security-best-practices)
8. [Troubleshooting](#troubleshooting)

## Getting Started with Security

The TBH Secure Agents framework includes comprehensive security features that are enabled by default. To get started with security:

1. Import the necessary components:

```python
from tbh_secure_agents import Expert, Operation, Squad
```

2. Create experts with appropriate security profiles:

```python
expert = Expert(
    specialty="Data Analyst",
    objective="Analyze data securely and accurately",
    security_profile="high",  # Use the standardized profile name
    api_key=YOUR_API_KEY
)
```

3. Create operations and squads as needed, and the security features will be automatically applied.

## Choosing Security Profiles

The framework supports several security profiles to accommodate different security requirements:

| Profile | Value | Description | Use Cases |
|---------|-------|-------------|-----------|
| **Minimal** | `"minimal"` | Only critical security checks | Development and testing |
| **Standard** | `"standard"` | Balanced security (default) | General purpose applications |
| **High** | `"high"` | Strict security validation | Sensitive applications |
| **Maximum** | `"maximum"` | Most stringent security | Highly sensitive applications |

### Legacy Profile Mapping [BETA]

For backward compatibility, the framework maps legacy profile names to the new standardized profiles:

| Legacy Profile | New Profile |
|----------------|------------|
| `default` | `standard` |
| `development`, `testing` | `minimal` |
| `basic` | `standard` |
| `high_security`, `code_restricted` | `high` |
| `maximum_security`, `air_gapped` | `maximum` |
| All other specialized profiles | `standard` |

Choose the security profile that best matches your security requirements:

```python
# For handling sensitive customer data
customer_expert = Expert(
    specialty="Customer Support",
    objective="Help customers with their inquiries",
    security_profile="high",  # High security for PII protection
    api_key=YOUR_API_KEY
)

# For financial applications
finance_expert = Expert(
    specialty="Financial Advisor",
    objective="Provide financial advice",
    security_profile="maximum",  # Maximum security for financial data
    api_key=YOUR_API_KEY
)
```

## Creating Secure Experts

When creating experts, consider the following security aspects:

1. **Choose an appropriate security profile**:

```python
expert = Expert(
    specialty="Security Analyst",
    objective="Analyze security threats",
    security_profile="high",  # Use the standardized profile name
    api_key=YOUR_API_KEY
)
```

2. **Provide clear and specific objectives**:

```python
# Good: Specific and clear objective
expert = Expert(
    specialty="Data Analyst",
    objective="Analyze sales data to identify trends and patterns, without revealing individual customer information",
    security_profile="high",  # High security for PII protection
    api_key=YOUR_API_KEY
)

# Bad: Vague objective
expert = Expert(
    specialty="Data Analyst",
    objective="Analyze data",
    security_profile="high",  # High security for PII protection
    api_key=YOUR_API_KEY
)
```

3. **Add background information to guide the expert's behavior**:

```python
expert = Expert(
    specialty="Healthcare Advisor",
    objective="Provide general health information",
    background="You are a healthcare advisor who provides general health information. You do not provide medical diagnoses or prescribe medications. You always protect patient privacy and never ask for or store personal health information.",
    security_profile="high",  # High security for healthcare data
    api_key=YOUR_API_KEY
)
```

## Securing Operations

Operations represent tasks that experts perform. To secure operations:

1. **Write clear and specific instructions**:

```python
# Good: Clear and specific instructions
operation = Operation(
    instructions="Analyze the attached sales data and identify the top 5 product categories by revenue. Do not include any customer names or identifiers in your analysis.",
    expert=data_analyst
)

# Bad: Vague instructions
operation = Operation(
    instructions="Analyze the sales data",
    expert=data_analyst
)
```

2. **Set appropriate security checks** [BETA]:

```python
operation = Operation(
    instructions="Analyze the customer feedback and summarize the main themes",
    expert=data_analyst,
    content_safety_enabled=True,  # Enable content safety checks [BETA]
    reliability_threshold=0.8,     # Set high reliability threshold [BETA]
    max_tokens=2000               # Limit output size
)
```

3. **Handle operation results securely**:

```python
result = operation.execute()

# Check if the operation was successful
if operation.status == "completed":
    # Process the result
    processed_result = process_result(result)
else:
    # Handle the error
    error_message = f"Operation failed: {operation.status}"
    logger.error(error_message)
```

## Building Secure Squads

Squads coordinate multiple experts to complete complex tasks. To build secure squads:

1. **Choose the appropriate process type**:

```python
# Sequential processing for tasks that depend on each other
squad = Squad(
    experts=[research_expert, analysis_expert, summary_expert],
    operations=[research_operation, analysis_operation, summary_operation],
    process="sequential"
)

# Parallel processing for independent tasks [BETA]
squad = Squad(
    experts=[data_expert, security_expert, compliance_expert],
    operations=[data_operation, security_operation, compliance_operation],
    process="parallel"  # Parallel processing is in beta
)
```

2. **Configure context passing securely** [BETA]:

```python
# Enable context passing with security checks
squad = Squad(
    experts=[research_expert, analysis_expert, summary_expert],
    operations=[research_operation, analysis_operation, summary_operation],
    process="sequential",
    context_passing=True,  # Enable context passing
    context_security=True  # Enable security checks on passed context [BETA]
)
```

3. **Set squad-level security options**:

```python
squad = Squad(
    experts=[research_expert, analysis_expert, summary_expert],
    operations=[research_operation, analysis_operation, summary_operation],
    process="sequential",
    security_level="high",  # Set high security level for the squad
    audit_enabled=True      # Enable comprehensive auditing [BETA]
)
```

## Advanced Security Configuration [BETA]

For advanced security needs, you can directly configure the security components. These features are currently in beta.

1. **Customize the PromptDefender** [BETA]:

```python
from tbh_secure_agents.security.prompt_defender import PromptDefender

# Create a custom prompt defender with maximum security
prompt_defender = PromptDefender(security_level="maximum")

# Use it with an expert
expert = Expert(
    specialty="Security Analyst",
    objective="Analyze security threats",
    security_profile="high",  # Use the standardized profile name
    api_key=YOUR_API_KEY
)

# Replace the default prompt defender
expert.prompt_defender = prompt_defender
```

2. **Customize the DataGuardian** [BETA]:

```python
from tbh_secure_agents.security.data_guardian import DataGuardian

# Create a custom data guardian with custom patterns
custom_patterns = {
    'company_id': [r'COMP-\d{6}'],
    'project_code': [r'PRJ-[A-Z]{3}-\d{4}']
}

data_guardian = DataGuardian(
    security_level="high",
    custom_patterns=custom_patterns
)

# Use it with an expert
expert.data_guardian = data_guardian
```

3. **Configure the ReliabilityMonitor** [BETA]:

```python
from tbh_secure_agents.security.reliability_monitor import ReliabilityMonitor

# Create a custom reliability monitor with adjusted thresholds
reliability_monitor = ReliabilityMonitor(security_level="high")

# Adjust specific thresholds
reliability_monitor.thresholds['consistency_threshold'] = 0.9
reliability_monitor.thresholds['repetition_threshold'] = 0.1

# Use it with an expert
expert.reliability_monitor = reliability_monitor
```

## Security Best Practices

Follow these best practices to maximize security:

1. **Use the highest appropriate security profile** for your use case
2. **Sanitize all inputs** before passing them to experts
3. **Validate all outputs** before using them
4. **Enable content safety checks** for all operations
5. **Set appropriate reliability thresholds** based on your requirements
6. **Monitor operation execution** and watch for security incidents
7. **Implement proper error handling** for security failures
8. **Regularly review security logs** for potential issues
9. **Keep the framework updated** to benefit from the latest security enhancements
10. **Conduct regular security testing** of your multi-agent systems

## Troubleshooting [BETA]

Common security-related issues and how to resolve them. These troubleshooting tips are for beta features and may change in future releases.

### Prompt Security Check Failures [BETA]

If you encounter prompt security check failures:

```
Error: Prompt failed pre-execution security check for expert 'Data Analyst'.
```

**Solution**:
- Review the prompt for potential injection attempts
- Remove any instructions that ask the expert to ignore or override its constraints
- Avoid phrases like "ignore previous instructions" or "pretend to be"
- Check the logs for specific patterns that triggered the security check

### Output Security Check Failures [BETA]

If you encounter output security check failures:

```
Error: Expert 'Data Analyst' generated an insecure response that could not be safely processed.
```

**Solution**:
- Check if the expert is generating sensitive information
- Consider using a more restrictive security profile
- Enable output sanitization for high security profiles
- Review the logs for specific issues detected in the output

### Context Passing Security Issues [BETA]

If you encounter context passing security issues:

```
Warning: Context passing blocked: Previous result deemed unsafe for operation
```

**Solution**:
- Ensure that operations don't generate sensitive information that needs to be passed to other operations
- Enable context sanitization to automatically remove sensitive information
- Consider restructuring your squad to avoid passing sensitive context
- Review the security profiles of your experts to ensure they're appropriate for the data being handled

## Hybrid Security Validation [BETA]

The TBH Secure Agents framework now includes a hybrid security validation system that combines rule-based, machine learning, and LLM-based approaches for comprehensive security validation.

### Using Hybrid Security Validation

```python
from tbh_secure_agents import Expert, Operation, Squad
from tbh_secure_agents.security_validation import HybridValidator

# Create an expert with hybrid security validation
expert = Expert(
    specialty="Security Analyst",
    objective="Analyze security threats",
    security_profile="high",
    hybrid_validation=True  # Enable hybrid validation
)

# Create an operation with hybrid security validation
operation = Operation(
    instructions="Analyze the security vulnerabilities in this code",
    expert=expert,
    hybrid_validation_level="comprehensive"  # Options: "basic", "standard", "comprehensive"
)

# Execute the operation
result = operation.execute()
```

### Hybrid Validation Components

The hybrid validation system includes three main components:

1. **Rule-based Validation**: Uses regex patterns and heuristics to detect security issues
2. **ML-based Validation**: Uses machine learning models to detect security issues
3. **LLM-based Validation**: Uses large language models to detect security issues

Each component has different strengths and weaknesses, and the hybrid approach combines them for more robust security validation.

## Security Visualization [BETA]

The TBH Secure Agents framework now includes visualization features for security validation results.

### HTML Security Reports

```python
from tbh_secure_agents import Expert, Operation
from tbh_secure_agents.visualization import generate_security_report

# Create and execute an operation
expert = Expert(
    specialty="Security Analyst",
    objective="Analyze security threats",
    security_profile="high"
)

operation = Operation(
    instructions="Analyze the security vulnerabilities in this code",
    expert=expert
)

result = operation.execute()

# Generate an HTML security report
report_path = generate_security_report(
    operation=operation,
    result=result,
    output_path="outputs/security_report.html",
    include_visualizations=True
)

print(f"Security report generated at: {report_path}")
```

### Security Visualization Features

The security visualization system includes:

1. **HTML Reports**: Detailed HTML reports with security validation results
2. **Security Score Visualizations**: Visual representations of security scores
3. **Threat Detection Visualizations**: Visual representations of detected threats
4. **Recommendation Visualizations**: Visual representations of security recommendations

## Beta Features Note

Features marked with [BETA] in this guide are currently under development and testing. They may change significantly before final release or may be removed entirely. Use these features with caution in non-production environments.

Beta features include:
- Hybrid Security Validation system
- Security Visualization and HTML reports
- Advanced security configuration components (PromptDefender, DataGuardian, ReliabilityMonitor)
- Parallel processing in squads
- Context security validation
- Comprehensive auditing
- Custom security parameters for operations
- Detailed troubleshooting for security issues

For the most stable experience, use the standard features without beta components until they are officially released.
