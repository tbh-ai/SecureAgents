# Security Profiles

The TBH Secure Agents framework provides a comprehensive security system with configurable security profiles. These profiles allow you to balance security and flexibility based on your specific needs.

## Overview

Security profiles define the level of security validation applied to operations and experts in a squad. Each profile has different thresholds and checks, ranging from minimal security (for maximum flexibility) to maximum security (for highest protection).

## Available Security Profiles

The framework includes the following built-in security profiles:

### Minimal

The minimal security profile provides basic security with minimal restrictions:

- **Purpose**: For development and testing in trusted environments
- **Features**:
  - Basic dangerous operation detection
  - No length limits on instructions
  - No authenticity verification
  - No content analysis
- **Use When**: You need maximum flexibility and are working in a controlled environment

### Low

The low security profile provides moderate security with some flexibility:

- **Purpose**: For development and testing with some security checks
- **Features**:
  - Dangerous operation detection
  - Basic data exfiltration detection
  - High length limits on instructions
  - No authenticity verification
- **Use When**: You need flexibility but want basic security checks

### Standard (Default)

The standard security profile provides a balanced approach to security:

- **Purpose**: For general use in most scenarios
- **Features**:
  - Comprehensive dangerous operation detection
  - Data exfiltration detection
  - Moderate length limits on instructions
  - Basic authenticity verification
- **Use When**: You want a good balance between security and flexibility

### High

The high security profile provides enhanced security with stricter checks:

- **Purpose**: For production use with sensitive data
- **Features**:
  - Strict dangerous operation detection
  - Advanced data exfiltration detection
  - Low length limits on instructions
  - Comprehensive authenticity verification
- **Use When**: You're working with sensitive data and need strong security

### Maximum

The maximum security profile provides the highest level of security:

- **Purpose**: For critical systems and highly sensitive data
- **Features**:
  - Extremely strict dangerous operation detection
  - Advanced data exfiltration detection
  - Very low length limits on instructions
  - Comprehensive authenticity verification
  - Requires all experts to use the same security profile
- **Use When**: You're working with highly sensitive data and need maximum security

## Using Security Profiles

You can specify a security profile when creating a Squad:

```python
from tbh_secure_agents import Expert, Operation, Squad

# Create a squad with the standard security profile (default)
squad = Squad(
    experts=[expert1, expert2],
    operations=[operation1, operation2],
    security_profile="standard"
)

# Create a squad with the high security profile
squad = Squad(
    experts=[expert1, expert2],
    operations=[operation1, operation2],
    security_profile="high"
)
```

## Security Profiles and Recommendations

The security profiles work seamlessly with the recommendation system:

- **Recommendations**: When a security check fails, the system provides recommendations based on the specific security issue
- **Auto-Fix**: If enabled, the system can automatically apply recommendations to fix security issues
- **Preview Changes**: You can preview changes before they're applied

To enable recommendations and auto-fix:

```python
squad = Squad(
    experts=[expert1, expert2],
    operations=[operation1, operation2],
    security_profile="standard",
    enable_recommendations=True,  # Enable recommendations (default)
    auto_fix=True,                # Enable auto-fix
    preview_changes=True          # Show changes before applying
)
```

## Custom Security Profiles

You can create custom security profiles by specifying custom security parameters:

```python
from tbh_secure_agents import Expert, Operation, Squad
from tbh_secure_agents.security_profiles import SecurityProfile

# Create a custom security profile
custom_profile = SecurityProfile(
    name="custom",
    dangerous_operation_threshold=0.7,
    data_exfiltration_threshold=0.8,
    max_instruction_length=10000,
    require_authenticity=True,
    content_analysis=True
)

# Create a squad with the custom security profile
squad = Squad(
    experts=[expert1, expert2],
    operations=[operation1, operation2],
    security_profile=custom_profile
)
```

## Best Practices

1. **Start with Standard**: Begin with the standard security profile and adjust as needed
2. **Match to Environment**: Use lower security profiles in development and higher ones in production
3. **Consider Data Sensitivity**: Choose higher security profiles when working with sensitive data
4. **Enable Recommendations**: Always enable recommendations to get guidance on security issues
5. **Review Auto-Fixes**: When using auto-fix, review the changes to ensure they meet your requirements
