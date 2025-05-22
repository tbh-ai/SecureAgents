# Security Profiles Guide

<img width="618" alt="Main" src="https://github.com/user-attachments/assets/dbbf5a4f-7b0b-4f43-9b37-ef77dc761ff1" />

The `tbh_secure_agents` framework includes a `security_profile` parameter in the `Expert` class constructor and a `security_level` parameter in the `Squad` class constructor. These parameters are key parts of the framework's security-first design, providing a mechanism for defining and enforcing different security constraints and capabilities.

> **Note**: Some features described in this guide are currently in beta and may not be available in the public release. These features are marked with [BETA].

**Current Status:** Enhanced Implementation

The security profiles system has been enhanced to provide more flexibility while maintaining strong security. The framework now offers a spectrum of security profiles from minimal (for development and testing) to maximum (for highly sensitive applications).

## Available Security Profiles

The TBH Secure Agents framework now includes the following standardized security profiles:

| Profile | Value | Description | Use Case |
|---------|-------|-------------|----------|
| **Minimal** | `"minimal"` | Only critical security checks | Development and testing |
| **Low** | `"low"` | Basic security checks | Non-sensitive applications |
| **Standard** | `"standard"` | Balanced security (default) | General purpose applications |
| **High** | `"high"` | Strict security validation | Sensitive applications |
| **Maximum** | `"maximum"` | Most stringent security | Highly sensitive applications |

### Legacy Profile Mapping [BETA]

For backward compatibility, the framework maps legacy profile names to the new standardized profiles:

| Legacy Profile | New Profile |
|----------------|------------|
| `default` | `standard` |
| `development`, `testing` | `minimal` |
| `basic` | `low` |
| `high_security`, `code_restricted` | `high` |
| `maximum_security`, `air_gapped` | `maximum` |
| All other specialized profiles | `standard` |

## How to Set Security Profiles

### For Experts

You assign a security profile when creating an `Expert` instance:

```python
from tbh_secure_agents import Expert

# Create an expert with minimal security for development
dev_expert = Expert(
    specialty="Developer",
    objective="Write code",
    security_profile="minimal",  # For development and testing
    api_key=API_KEY
)

# Create an expert with standard security (default)
standard_expert = Expert(
    specialty="Research Assistant",
    objective="Gather information",
    # security_profile defaults to "standard" if not specified
    api_key=API_KEY
)

# Create an expert with high security for sensitive tasks
secure_expert = Expert(
    specialty="Financial Analyst",
    objective="Process financial data",
    security_profile="high",  # For sensitive applications
    api_key=API_KEY
)
```

### For Squads

You set the security level when creating a `Squad` instance:

```python
from tbh_secure_agents import Squad

# Create a squad with minimal security for development
dev_squad = Squad(
    experts=[expert1, expert2],
    operations=[op1, op2],
    security_level="minimal"  # For development and testing
)

# Create a squad with standard security (default)
standard_squad = Squad(
    experts=[expert1, expert2],
    operations=[op1, op2],
    # security_level defaults to "standard" if not specified
)

# Create a squad with high security for sensitive tasks
secure_squad = Squad(
    experts=[expert1, expert2],
    operations=[op1, op2],
    security_level="high"  # For sensitive applications
)
```

## Security Profile Details

### Minimal Security Profile

The minimal security profile is designed for development and testing environments. It skips most security checks and only prevents critical exploits that could harm the system.

**Features:**
- Only checks for critical system commands
- Skips content analysis
- Skips format validation
- Skips context validation
- Skips output validation

**Example Use Case:**
```python
# For rapid development and testing
expert = Expert(
    specialty="Developer",
    objective="Test new features",
    security_profile="minimal",
    api_key=API_KEY
)

squad = Squad(
    experts=[expert],
    operations=[operation],
    security_level="minimal"
)
```

### Low Security Profile

The low security profile provides basic security checks while allowing more flexibility than the standard profile. It's suitable for non-sensitive applications where usability is more important than strict security.

**Features:**
- Checks for critical system commands
- Performs basic structure validation
- Skips detailed content analysis
- Uses permissive thresholds for security checks

**Example Use Case:**
```python
# For non-sensitive applications
expert = Expert(
    specialty="Content Creator",
    objective="Generate creative content",
    security_profile="low",
    api_key=API_KEY
)

squad = Squad(
    experts=[expert],
    operations=[operation],
    security_level="low"
)
```

### Standard Security Profile (Default)

The standard security profile provides a balance between security and usability. It's suitable for most general-purpose applications.

**Features:**
- Comprehensive security checks
- Moderate thresholds for security validation
- Content analysis for sensitive data
- Format validation for outputs
- Context validation between operations

**Example Use Case:**
```python
# For general-purpose applications
expert = Expert(
    specialty="Research Assistant",
    objective="Gather information",
    security_profile="standard",  # This is the default
    api_key=API_KEY
)

squad = Squad(
    experts=[expert],
    operations=[operation],
    security_level="standard"  # This is the default
)
```

### High Security Profile

The high security profile provides strict security validation for sensitive applications. It uses lower thresholds for security checks and performs additional validations.

**Features:**
- Strict thresholds for security validation
- Comprehensive content analysis
- Detailed format validation
- Strict context validation
- Additional checks for expert manipulation and unauthorized access

**Example Use Case:**
```python
# For sensitive applications
expert = Expert(
    specialty="Financial Analyst",
    objective="Analyze financial data",
    security_profile="high",
    api_key=API_KEY
)

squad = Squad(
    experts=[expert],
    operations=[operation],
    security_level="high"
)
```

### Maximum Security Profile

The maximum security profile provides the most stringent security validation for highly sensitive applications. It uses the lowest thresholds for security checks and performs the most comprehensive validations.

**Features:**
- Most stringent thresholds for security validation
- Most comprehensive content analysis
- Most detailed format validation
- Most strict context validation
- Most comprehensive checks for expert manipulation and unauthorized access
- Requires consistent security profiles across all experts

**Example Use Case:**
```python
# For highly sensitive applications
expert = Expert(
    specialty="Security Analyst",
    objective="Analyze security vulnerabilities",
    security_profile="maximum",
    api_key=API_KEY
)

squad = Squad(
    experts=[expert],
    operations=[operation],
    security_level="maximum"
)
```

## How Security Profiles Work

Security profiles influence the behavior of several security checkpoints in the framework:

1. **Pre-Prompt Security Checks**: Before sending prompts to the LLM, the framework checks if the prompt is secure based on the expert's security profile.

2. **Post-Output Security Checks**: After receiving output from the LLM, the framework validates it against the security profile's requirements.

3. **Operation Security Validation**: Before executing operations, the framework checks if they comply with the security profile's constraints.

4. **Context Passing Security**: When passing context between operations, the framework applies security checks based on the profiles of both the source and target experts.

## Security Thresholds

Each security profile has different thresholds for various security checks:

| Check | Minimal | Low | Standard | High | Maximum |
|-------|---------|-----|----------|------|---------|
| Injection Detection | 0.9 | 0.8 | 0.6 | 0.4 | 0.2 |
| Sensitive Data | 0.9 | 0.7 | 0.5 | 0.3 | 0.1 |
| Relevance | 0.1 | 0.2 | 0.4 | 0.6 | 0.8 |
| Reliability | 0.1 | 0.3 | 0.5 | 0.7 | 0.9 |
| Consistency | 0.1 | 0.3 | 0.5 | 0.7 | 0.9 |

Lower thresholds for injection detection and sensitive data mean more strict checking (more likely to block). Higher thresholds for relevance, reliability, and consistency mean more strict checking (more likely to block).

## Security Checks

Each security profile enables or disables different security checks:

| Check | Minimal | Low | Standard | High | Maximum |
|-------|---------|-----|----------|------|---------|
| Critical Exploits | ✅ | ✅ | ✅ | ✅ | ✅ |
| System Commands | ✅ | ✅ | ✅ | ✅ | ✅ |
| Content Analysis | ❌ | ❌ | ✅ | ✅ | ✅ |
| Format Validation | ❌ | ✅ | ✅ | ✅ | ✅ |
| Context Validation | ❌ | ❌ | ✅ | ✅ | ✅ |
| Output Validation | ❌ | ❌ | ✅ | ✅ | ✅ |
| Expert Validation | ❌ | ✅ | ✅ | ✅ | ✅ |

## Best Practices

1. **Use the appropriate security profile for your use case:**
   - Use `minimal` for development and testing only
   - Use `low` for non-sensitive applications where usability is more important
   - Use `standard` for most general-purpose applications
   - Use `high` for sensitive applications
   - Use `maximum` for highly sensitive applications

2. **Be consistent with security profiles:**
   - Use the same security profile for all experts in a squad when possible
   - If mixing security profiles, ensure that the squad's security level is at least as high as the highest expert security profile

3. **Adjust security profiles based on the context:**
   - Use higher security profiles when dealing with sensitive data
   - Use lower security profiles when generating creative content

4. **Monitor security warnings:**
   - Pay attention to security warnings in the logs
   - Address security issues even when they don't block execution

5. **Test with different security profiles:**
   - Test your application with different security profiles to find the right balance
   - Start with a lower security profile and gradually increase it

## Security Profile Inheritance

When operations are executed in a sequential process, security considerations from earlier operations can influence later ones. The framework implements security profile inheritance to ensure consistent security enforcement throughout the execution chain.

For example, if an operation with a `high` security profile passes context to an operation with a `standard` profile, the framework will apply additional security checks to ensure the integrity of the execution chain is maintained.

## Custom Security Profiles

In addition to the standard security profiles, you can create custom security profiles tailored to your specific requirements. Custom profiles allow you to define your own security thresholds and checks.

### Creating a Custom Security Profile

To create a custom security profile, use the `register_custom_profile` function:

```python
from tbh_secure_agents.security_profiles import register_custom_profile

# Register a custom security profile
register_custom_profile(
    name="healthcare",  # Name of the custom profile
    thresholds={
        "injection_score": 0.3,       # Threshold for injection detection
        "sensitive_data": 0.2,        # Threshold for sensitive data detection
        "relevance_score": 0.7,       # Threshold for relevance check
        "reliability_score": 0.8,     # Threshold for reliability check
        "consistency_score": 0.8,     # Threshold for consistency check
    },
    checks={
        "critical_exploits": True,    # Check for critical exploits
        "system_commands": True,      # Check for system commands
        "content_analysis": True,     # Perform content analysis
        "format_validation": True,    # Perform format validation
        "context_validation": True,   # Perform context validation
        "output_validation": True,    # Perform output validation
        "expert_validation": True,    # Perform expert validation
    },
    description="Custom security profile for healthcare applications with strict PII protection"
)
```

### Using a Custom Security Profile

Once registered, you can use your custom security profile with experts and squads:

```python
from tbh_secure_agents import Expert, Squad, Operation

# Create an expert with a custom security profile
expert = Expert(
    specialty="Healthcare Expert",
    objective="Analyze medical data",
    background="Expert in healthcare data analysis",
    security_profile="healthcare",  # Use the custom profile name
    api_key="your-api-key"
)

# Create a squad with a custom security profile
squad = Squad(
    experts=[expert],
    operations=[operation],
    process="sequential",
    security_level="healthcare"  # Use the custom profile name
)
```

### Managing Custom Security Profiles

The framework provides functions to list and retrieve custom security profiles:

```python
from tbh_secure_agents.security_profiles import list_custom_profiles, get_custom_profile

# List all registered custom profiles
profiles = list_custom_profiles()
print(f"Registered custom profiles: {profiles}")

# Get a specific custom profile
profile = get_custom_profile("healthcare")
if profile:
    print(f"Profile description: {profile['description']}")
    print(f"Profile thresholds: {profile['thresholds']}")
    print(f"Profile checks: {profile['checks']}")
```

### Industry-Specific Custom Profiles

Custom security profiles are particularly useful for industry-specific applications with unique security requirements:

#### Healthcare

```python
register_custom_profile(
    name="healthcare",
    thresholds={
        "injection_score": 0.3,
        "sensitive_data": 0.2,
        "relevance_score": 0.7,
        "reliability_score": 0.8,
        "consistency_score": 0.8,
    },
    checks={
        "critical_exploits": True,
        "system_commands": True,
        "content_analysis": True,
        "format_validation": True,
        "context_validation": True,
        "output_validation": True,
        "expert_validation": True,
    },
    description="Custom security profile for healthcare applications with strict PII protection"
)
```

#### Finance

```python
register_custom_profile(
    name="finance",
    thresholds={
        "injection_score": 0.2,
        "sensitive_data": 0.2,
        "relevance_score": 0.8,
        "reliability_score": 0.9,
        "consistency_score": 0.9,
    },
    checks={
        "critical_exploits": True,
        "system_commands": True,
        "content_analysis": True,
        "format_validation": True,
        "context_validation": True,
        "output_validation": True,
        "expert_validation": True,
    },
    description="Custom security profile for financial applications with strict data protection"
)
```

#### Education

```python
register_custom_profile(
    name="education",
    thresholds={
        "injection_score": 0.5,
        "sensitive_data": 0.4,
        "relevance_score": 0.6,
        "reliability_score": 0.7,
        "consistency_score": 0.7,
    },
    checks={
        "critical_exploits": True,
        "system_commands": True,
        "content_analysis": True,
        "format_validation": True,
        "context_validation": True,
        "output_validation": True,
        "expert_validation": True,
    },
    description="Custom security profile for educational applications with balanced security"
)
```

### Best Practices for Custom Profiles

1. **Start with a standard profile as a base**: Use one of the standard profiles as a starting point and adjust the thresholds and checks as needed.

2. **Test thoroughly**: Test your custom profile with a variety of inputs to ensure it provides the right balance of security and usability.

3. **Document your custom profiles**: Keep track of the custom profiles you create and their specific security requirements.

4. **Review and update regularly**: Security requirements change over time, so review and update your custom profiles regularly.

5. **Consider performance implications**: More strict security checks can impact performance, so consider the performance implications of your custom profile.

