# Hybrid Security Validation and Visualization [BETA]

> **Note**: The features described in this document are currently in beta and may change significantly before final release.

The TBH Secure Agents framework includes a hybrid security validation system that combines rule-based, machine learning, and LLM-based approaches for comprehensive security validation. This document explains how to use these features and the visualization tools that accompany them.

## Hybrid Security Validation

### Overview

The hybrid security validation system combines three different approaches to security validation:

1. **Rule-based Validation**: Uses regex patterns and heuristics to detect security issues
2. **ML-based Validation**: Uses machine learning models to detect security issues
3. **LLM-based Validation**: Uses large language models to detect security issues

By combining these approaches, the system provides more robust security validation than any single approach could provide on its own.

### Components

#### Rule-based Validator

The rule-based validator uses a set of predefined regex patterns and heuristics to detect security issues. It's fast and deterministic, but may miss novel security issues.

#### ML-based Validator

The ML-based validator uses machine learning models trained on security data to detect security issues. It can detect patterns that might be missed by rule-based approaches, but may produce false positives or false negatives.

#### LLM-based Validator

The LLM-based validator uses large language models to analyze content for security issues. It's the most flexible approach and can detect novel security issues, but may be slower and less deterministic than the other approaches.

### Usage

To use the hybrid security validation system, you need to enable it when creating experts or operations:

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

## Security Visualization

The security visualization system provides tools for visualizing security validation results.

### HTML Reports

The most comprehensive visualization is the HTML security report, which provides a detailed view of security validation results:

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

### Visualization Features

The security visualization system includes:

1. **HTML Reports**: Detailed HTML reports with security validation results
2. **Security Score Visualizations**: Visual representations of security scores
3. **Threat Detection Visualizations**: Visual representations of detected threats
4. **Recommendation Visualizations**: Visual representations of security recommendations

## Best Practices

1. **Use the appropriate validation level**: Choose the validation level based on your security requirements
   - `basic`: Fast but less comprehensive
   - `standard`: Balanced approach
   - `comprehensive`: Most thorough but slower

2. **Enable all validation components**: For maximum security, enable all validation components (rule, ML, LLM)

3. **Set appropriate thresholds**: Adjust validation thresholds based on your security requirements

4. **Review visualization reports**: Always review the generated reports to understand security issues

5. **Combine with security profiles**: Use hybrid validation with appropriate security profiles for maximum security
