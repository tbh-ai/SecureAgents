# Comprehensive Guardrails Guide

<img width="618" alt="Main" src="https://github.com/user-attachments/assets/dbbf5a4f-7b0b-4f43-9b37-ef77dc761ff1" />

## Introduction to Guardrails

Guardrails in the TBH Secure Agents framework provide a powerful way to dynamically control and guide the behavior of experts without modifying your core code. They serve as both a security mechanism and a flexibility tool, allowing you to set boundaries and provide dynamic inputs at runtime.

### Security-First Design

The guardrails system is built with a security-first approach, providing:

- **Input Validation and Sanitization**: All guardrail inputs are validated and sanitized to prevent injection attacks
- **Dynamic Security Constraints**: Apply security rules that can adapt to different contexts
- **Runtime Security Controls**: Adjust security parameters without changing your code
- **Secure Context Passing**: Safely pass information between experts with appropriate validation

This approach ensures that your multi-agent systems remain secure even when handling dynamic, user-provided inputs.

## How Guardrails Work

Guardrails are implemented as a dictionary of key-value pairs that are passed to the Squad's `deploy()` method. These inputs go through a multi-stage security process:

1. **Validation**: Each input is validated for type, length, and content
2. **Sanitization**: Inputs are sanitized to remove potentially harmful content
3. **Security Scanning**: Inputs are scanned for patterns that might indicate security threats
4. **Context Integration**: Validated inputs are added to the Squad's security context
5. **Template Processing**: Inputs are used to fill template variables in expert profiles and operation instructions
6. **Security Enforcement**: Security rules are applied based on the combined context

This comprehensive approach ensures that guardrails enhance both flexibility and security.

## Basic Usage

### Simple Guardrails

```python
# Create your experts and operations
expert = Expert(...)
operation = Operation(...)

# Create your squad
squad = Squad(experts=[expert], operations=[operation])

# Define guardrail inputs with security parameters
guardrails = {
    "topic": "Artificial Intelligence",
    "tone": "professional",
    "max_length": 500,
    "security_level": "high",
    "allowed_data_sources": ["internal_db", "approved_apis"]
}

# Deploy the squad with guardrails
result = squad.deploy(guardrails=guardrails)
```

### Complex Guardrails

Guardrails can include complex data structures, which are all validated for security:

```python
guardrails = {
    "user_profile": {
        "name": "John Doe",
        "preferences": ["technology", "science", "business"],
        "expertise_level": "intermediate"
    },
    "data_points": [10, 25, 30, 15, 20],
    "include_charts": True,
    "compliance_level": "strict",
    "security_constraints": {
        "pii_handling": "redact",
        "data_retention": "temporary",
        "output_validation": "strict"
    }
}
```

## Template Variables

One of the most powerful features of guardrails is the ability to use template variables in your expert profiles and operation instructions. This allows you to create flexible templates that can be filled with different values at runtime.

### Template Variables in Expert Profiles

You can use template variables in expert profiles to dynamically adjust their specialty, objective, and background:

```python
# Expert with template variables
security_expert = Expert(
    specialty="Security Specialist focusing on {security_domain}",
    objective="Identify and mitigate {threat_type} threats in {system_type} systems",
    background="You have {experience_years} years of experience in {security_domain} security and specialize in {methodology} analysis."
)
```

When you deploy the squad with guardrails, these template variables will be replaced with the corresponding values:

```python
guardrails = {
    "security_domain": "network",
    "threat_type": "advanced persistent",
    "system_type": "enterprise",
    "experience_years": "15+",
    "methodology": "threat modeling"
}
```

This would effectively transform the expert's profile to:

```
Specialty: Security Specialist focusing on network
Objective: Identify and mitigate advanced persistent threats in enterprise systems
Background: You have 15+ years of experience in network security and specialize in threat modeling analysis.
```

### Template Variables in Operation Instructions

You can also use template variables in operation instructions:

```python
# Operation with template variables and security focus
security_operation = Operation(
    instructions="""
    Perform a {assessment_type} assessment of the {target_system} system.
    Focus on identifying {vulnerability_type} vulnerabilities.
    Apply the {security_standard} security standard during your assessment.
    The scope of this assessment is limited to {scope}.
    
    Security classification: {security_classification}
    Data handling requirements: {data_handling}
    """,
    output_format="A comprehensive {assessment_type} security report",
    expert=security_expert
)
```

When deployed with appropriate guardrails, these variables will be replaced with the actual values, maintaining security constraints.

## Conditional Formatting with Select Syntax

The select syntax allows you to create conditional content based on the value of a variable. This is particularly useful for implementing dynamic security controls.

### Basic Select Syntax

The basic syntax for conditional formatting is:

```
{variable, select, 
  option1:text for option1|
  option2:text for option2|
  option3:text for option3
}
```

For example:

```python
operation = Operation(
    instructions="""
    Analyze the security of {system_name}.
    
    {security_level, select, 
      high:Apply the most stringent security checks and document all potential vulnerabilities regardless of severity.|
      medium:Focus on significant security issues that could lead to system compromise.|
      low:Identify only critical security flaws that require immediate attention.
    }
    
    {include_remediation, select,
      true:For each vulnerability, provide detailed remediation steps.|
      false:Focus only on identifying vulnerabilities without remediation details.
    }
    """,
    expert=security_expert
)
```

If the guardrail `security_level` is set to `high`, the instruction will become:

```
Analyze the security of [system_name].

Apply the most stringent security checks and document all potential vulnerabilities regardless of severity.
```

### Security-Focused Select Syntax

You can use the select syntax to implement dynamic security controls:

```python
operation = Operation(
    instructions="""
    Analyze the provided data and extract insights.
    
    {data_sensitivity, select,
      confidential:Apply strict PII redaction. Do not include any personally identifiable information in your output.|
      restricted:Redact sensitive personal information but include anonymized demographic data.|
      public:Include all relevant information but avoid specific identifiers.
    }
    
    {output_format, select,
      technical:Provide detailed technical analysis with all data points.|
      executive:Provide high-level insights suitable for executive review.|
      compliance:Format the output to meet {compliance_standard} requirements.
    }
    """,
    expert=data_analyst
)
```

## Security Considerations for Guardrails

The TBH Secure Agents framework implements several security measures specifically for guardrails:

### 1. Input Validation and Sanitization

All guardrail inputs undergo rigorous validation and sanitization:

- **Type Checking**: Ensures inputs match expected types
- **Length Limits**: Prevents resource exhaustion attacks
- **Content Validation**: Checks for potentially malicious content
- **Pattern Matching**: Detects known attack patterns
- **HTML Sanitization**: Removes potentially harmful HTML tags

### 2. Template Variable Security

Template variables are processed with security in mind:

- **Escape Sequences**: Special characters are properly escaped
- **Context-Aware Replacement**: Variables are replaced in a context-aware manner
- **Recursive Validation**: Nested variables are validated at each level
- **Format String Protection**: Prevents format string attacks

### 3. Security Profile Integration

Guardrails integrate with the security profile system:

- **Profile-Specific Validation**: Different security profiles apply different validation rules
- **Dynamic Security Levels**: Security levels can be adjusted through guardrails
- **Security Inheritance**: Security constraints are inherited through the operation chain

### 4. Secure Context Passing

When context is passed between operations, guardrails ensure security:

- **Context Validation**: Context is validated before passing
- **Trust-Based Sharing**: Context sharing is based on trust levels between experts
- **Sanitization**: Context is sanitized based on security profiles
- **Relevance Checking**: Context is checked for relevance to the target operation

### 5. Security Incident Tracking

The framework tracks security incidents related to guardrails:

- **Logging**: All security checks are logged
- **Incident Recording**: Security incidents are recorded for later analysis
- **Audit Trail**: A complete audit trail is maintained
- **Threshold Monitoring**: Incidents are monitored against thresholds

## Real-World Security Examples

### Example 1: Secure Data Analysis

```python
# Create a data security expert
data_security_expert = Expert(
    specialty="Data Security Analyst specializing in {data_type} protection",
    objective="Analyze data securely while maintaining {compliance_standard} compliance",
    background="You have expertise in secure data handling and privacy protection.",
    security_profile="pii_protection"
)

# Create a secure data analysis operation
secure_analysis_operation = Operation(
    instructions="""
    Analyze the provided {data_type} data securely.
    
    {security_level, select, 
      maximum:Apply the strictest security controls. Redact all PII. Use secure processing methods only.|
      high:Apply strong security controls. Redact sensitive PII. Prioritize security over detail.|
      standard:Apply standard security controls. Anonymize PII where possible.
    }
    
    {compliance_standard, select, 
      GDPR:Ensure all processing complies with GDPR requirements including data minimization.|
      HIPAA:Follow HIPAA guidelines for protected health information.|
      PCI-DSS:Apply PCI-DSS controls for payment card information.
    }
    
    {data_retention, select,
      none:Do not retain any of the analyzed data after processing.|
      temporary:Retain processed data only for the duration of this analysis.|
      anonymized:Retain only anonymized data after processing.
    }
    """,
    output_format="A secure analysis report compliant with {compliance_standard}",
    expert=data_security_expert
)

# Deploy with security-focused guardrails
result = secure_squad.deploy(guardrails={
    "data_type": "financial",
    "compliance_standard": "GDPR",
    "security_level": "maximum",
    "data_retention": "none",
    "pii_types": ["names", "account_numbers", "addresses"],
    "allowed_processing_methods": ["secure_aggregation", "differential_privacy"],
    "security_logging": "verbose"
})
```

### Example 2: Secure Code Review

```python
# Create a code security expert
code_security_expert = Expert(
    specialty="Code Security Reviewer specializing in {language} applications",
    objective="Identify security vulnerabilities in {application_type} code",
    background="You have expertise in secure coding practices and vulnerability detection.",
    security_profile="code_restricted"
)

# Create a secure code review operation
code_review_operation = Operation(
    instructions="""
    Review the provided {language} code for security vulnerabilities.
    
    {vulnerability_focus, select, 
      OWASP_Top_10:Focus on identifying OWASP Top 10 vulnerabilities.|
      CWE_Top_25:Focus on identifying CWE Top 25 vulnerabilities.|
      custom:Focus on {custom_vulnerability_types}.
    }
    
    {severity_threshold, select, 
      critical:Report only critical vulnerabilities that could lead to system compromise.|
      high:Report critical and high severity vulnerabilities.|
      all:Report all vulnerabilities regardless of severity.
    }
    
    {include_remediation, select,
      detailed:Provide detailed remediation steps for each vulnerability.|
      basic:Provide basic remediation guidance.|
      none:Focus only on vulnerability identification.
    }
    
    {code_execution, select,
      none:Do not execute any code during the review.|
      static_only:Perform static analysis only.|
      sandboxed:Perform limited execution in a secure sandbox.
    }
    """,
    output_format="A comprehensive security review report",
    expert=code_security_expert
)

# Deploy with security-focused guardrails
result = security_squad.deploy(guardrails={
    "language": "Python",
    "application_type": "web",
    "vulnerability_focus": "OWASP_Top_10",
    "severity_threshold": "high",
    "include_remediation": "detailed",
    "code_execution": "none",
    "security_standards": ["NIST", "ISO27001"],
    "secure_coding_guidelines": "PEP 8 with security extensions"
})
```

## Best Practices for Secure Guardrails

When using guardrails, follow these security best practices:

1. **Validate External Inputs**: If guardrail values come from user input, validate them before passing them to the framework
2. **Use Security Profiles**: Combine guardrails with appropriate security profiles for enhanced protection
3. **Apply Least Privilege**: Only provide the minimum necessary information in guardrails
4. **Avoid Sensitive Data**: Don't include sensitive data in guardrail inputs
5. **Monitor Security Logs**: Regularly review security logs for potential issues
6. **Test Security Controls**: Test your guardrails with different inputs to ensure security controls work as expected
7. **Use Type Hints**: Add type hints to your code to indicate what types of values are expected for each guardrail
8. **Document Security Requirements**: Document the security requirements for each guardrail
9. **Apply Defense in Depth**: Don't rely solely on guardrails for security; use multiple layers of protection
10. **Regular Security Reviews**: Regularly review your guardrails for potential security issues

## Guardrails and Security Profiles

Guardrails work seamlessly with security profiles to provide comprehensive security:

```python
# Create a high-security expert
secure_expert = Expert(
    specialty="Security Analyst",
    objective="Provide secure analysis of {data_type} data",
    security_profile="high_security",
    api_key=API_KEY
)

# Create a squad with high security level
secure_squad = Squad(
    experts=[secure_expert],
    operations=[...],
    security_level="high"
)

# Deploy with guardrails that include security parameters
result = secure_squad.deploy(guardrails={
    "data_type": "financial",
    "compliance_level": "strict",
    "allowed_data_sources": ["internal_db", "approved_apis"],
    "pii_handling": "redact_all",
    "security_checks": ["input_validation", "output_sanitization", "context_validation"],
    "audit_level": "comprehensive"
})
```

This approach allows you to dynamically adjust security parameters based on runtime requirements while maintaining a strong security posture.

## Advanced Security Features

### 1. Security Parameter Inheritance

Guardrails can define security parameters that are inherited throughout the operation chain:

```python
guardrails = {
    "security_inheritance": {
        "pii_handling": "redact",
        "output_validation": "strict",
        "context_passing": "validated"
    }
}
```

### 2. Security Checkpoints

You can define specific security checkpoints in your operations:

```python
operation = Operation(
    instructions="""
    Analyze the provided data.
    
    {security_checkpoint, select,
      pre_processing:Validate all inputs before processing.|
      during_processing:Apply continuous security validation during processing.|
      post_processing:Validate all outputs after processing.
    }
    """,
    expert=analyst
)
```

### 3. Dynamic Trust Levels

Guardrails can define trust levels between experts:

```python
guardrails = {
    "trust_levels": {
        "data_analyst": {
            "security_expert": 0.8,
            "reporting_expert": 0.6
        }
    }
}
```

## Examples in the Repository

For complete working examples, see:

- `examples/example_guardrails.py`: Basic example of guardrails usage
- `examples/advanced_guardrails.py`: Advanced example with complex template variables and conditional formatting
- `examples/security_guardrails.py`: Example focusing on security-specific guardrails

## Conclusion

Guardrails in the TBH Secure Agents framework provide a powerful mechanism for both flexibility and security. By combining dynamic inputs with comprehensive security controls, they enable you to build secure, adaptable multi-agent systems that can respond to changing requirements while maintaining a strong security posture.

The security-first design ensures that even when using dynamic, user-provided inputs, your multi-agent systems remain protected against common security threats, making guardrails an essential tool for building secure AI applications.
