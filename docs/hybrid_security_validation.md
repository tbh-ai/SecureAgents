# Hybrid Security Validation and Visualization [BETA]

> **Note**: The features described in this document are currently in beta and may change significantly before final release.

The TBH Secure Agents framework includes a hybrid security validation system that combines rule-based, machine learning, and LLM-based approaches for comprehensive security validation. This document explains how to use these features and the visualization tools that accompany them.

## Table of Contents

1. [Hybrid Security Validation](#hybrid-security-validation)
   - [Overview](#overview)
   - [Components](#components)
   - [Usage](#usage)
   - [Configuration](#configuration)
2. [Security Visualization](#security-visualization)
   - [HTML Reports](#html-reports)
   - [Visualization Features](#visualization-features)
   - [Customization](#customization)
3. [Integration Examples](#integration-examples)
4. [Best Practices](#best-practices)
5. [Troubleshooting](#troubleshooting)

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

### Configuration

You can configure the hybrid security validation system using the following parameters:

#### Expert Configuration

- `hybrid_validation`: Boolean, whether to enable hybrid validation for this expert
- `hybrid_validation_components`: List of strings, which components to enable ("rule", "ml", "llm")

#### Operation Configuration

- `hybrid_validation_level`: String, the level of validation to perform ("basic", "standard", "comprehensive")
- `hybrid_validation_timeout`: Integer, the maximum time in seconds to spend on validation
- `hybrid_validation_threshold`: Float, the threshold for considering a validation result as a security issue

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

### Customization

You can customize the security visualizations using the following parameters:

- `include_visualizations`: Boolean, whether to include visualizations in the report
- `visualization_type`: String, the type of visualizations to include ("basic", "advanced")
- `theme`: String, the theme to use for visualizations ("light", "dark")
- `logo_path`: String, the path to a custom logo to include in the report

## Integration Examples

### Integration with Squad

```python
from tbh_secure_agents import Expert, Operation, Squad
from tbh_secure_agents.visualization import generate_squad_security_report

# Create experts and operations
expert1 = Expert(
    specialty="Security Analyst",
    objective="Analyze security threats",
    security_profile="high",
    hybrid_validation=True
)

expert2 = Expert(
    specialty="Code Reviewer",
    objective="Review code for security issues",
    security_profile="high",
    hybrid_validation=True
)

operation1 = Operation(
    instructions="Analyze the security vulnerabilities in this code",
    expert=expert1,
    hybrid_validation_level="comprehensive"
)

operation2 = Operation(
    instructions="Review the code for security best practices",
    expert=expert2,
    hybrid_validation_level="comprehensive"
)

# Create and deploy a squad
squad = Squad(
    experts=[expert1, expert2],
    operations=[operation1, operation2],
    process="sequential"
)

result = squad.deploy()

# Generate a squad security report
report_path = generate_squad_security_report(
    squad=squad,
    result=result,
    output_path="outputs/squad_security_report.html",
    include_visualizations=True
)

print(f"Squad security report generated at: {report_path}")
```

## Best Practices

1. **Use the appropriate validation level**: Choose the validation level based on your security requirements
   - `basic`: Fast but less comprehensive
   - `standard`: Balanced approach
   - `comprehensive`: Most thorough but slower

2. **Enable all validation components**: For maximum security, enable all validation components (rule, ML, LLM)

3. **Set appropriate thresholds**: Adjust validation thresholds based on your security requirements

4. **Review visualization reports**: Always review the generated reports to understand security issues

5. **Combine with security profiles**: Use hybrid validation with appropriate security profiles for maximum security

## Troubleshooting

### Common Issues

1. **Slow validation**: If validation is too slow, try using a lower validation level or disabling some components

2. **False positives**: If you're getting too many false positives, try adjusting the validation thresholds

3. **Visualization errors**: If visualizations aren't rendering correctly, check that you have the required dependencies installed

4. **Missing ML models**: If ML validation is failing, ensure that the required ML models are available

### Getting Help

If you encounter issues with the hybrid security validation or visualization features, please:

1. Check the documentation for updates
2. Look for examples in the `examples/` directory
3. Open an issue on the GitHub repository
4. Contact the maintainer at saish.shinde.jb@gmail.com
