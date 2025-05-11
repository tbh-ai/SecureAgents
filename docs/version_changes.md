# TBH Secure Agents: Version Changes

<img width="618" alt="Main" src="https://github.com/user-attachments/assets/dbbf5a4f-7b0b-4f43-9b37-ef77dc761ff1" />

This document outlines the key changes and enhancements in the latest version of the TBH Secure Agents framework.

## New Guardrails System

The most significant enhancement in this version is the introduction of a comprehensive guardrails system that allows for dynamic control of expert behavior at runtime.

### Template Variables

You can now use template variables in expert profiles and operation instructions:

```python
# Expert with template variables
expert = Expert(
    specialty="Content Writer specializing in {domain}",
    objective="Create {content_type} content for {audience}",
    background="You have experience writing {tone} content about {domain}."
)

# Operation with template variables
operation = Operation(
    instructions="Write a {length} article about {topic} for {audience}.",
    output_format="A well-formatted {content_type}"
)
```

These variables are replaced with values from the guardrails when the squad is deployed:

```python
result = squad.deploy(guardrails={
    "domain": "healthcare",
    "content_type": "blog post",
    "audience": "medical professionals",
    "tone": "professional",
    "length": "1000-word",
    "topic": "AI in medical diagnosis"
})
```

### Conditional Formatting with Select Syntax

The new select syntax allows for conditional content based on guardrail values:

```python
operation = Operation(
    instructions="""
    Write a report about {topic}.

    {tone, select,
      formal:Use a professional, academic tone suitable for scholarly publications.|
      conversational:Use a friendly, approachable tone as if speaking directly to the reader.|
      technical:Use precise technical language appropriate for experts in the field.
    }

    {include_examples, select,
      true:Include practical examples to illustrate key points.|
      false:Focus on theoretical concepts without specific examples.
    }
    """,
    expert=content_expert
)
```

This powerful feature enables dynamic instruction generation based on runtime parameters.

## Comprehensive Security Enhancements

We've implemented a complete security overhaul in this version, making TBH Secure Agents one of the most secure multi-agent frameworks available:

### 1. New Security Architecture

- Introduced a modular security architecture with four key components
- Implemented defense-in-depth approach to security
- Added support for multiple security levels (standard, high, maximum)
- Created comprehensive security profiles for different use cases

### 2. Advanced Prompt Defender

- Implemented sophisticated prompt injection detection using multiple methods:
  - Pattern matching with extensive pattern library
  - Semantic analysis of prompt content
  - Contextual understanding to detect subtle attacks
  - Historical pattern analysis to learn from past attacks
- Added detailed threat analysis with threat level scoring
- Implemented specific recommendations for improving prompt security
- Created adaptive defense that learns from detected attacks

### 3. Comprehensive Data Guardian

- Implemented advanced data leakage prevention:
  - Comprehensive PII detection for multiple data types and formats
  - Credential and secret detection
  - Financial information protection
  - Internal information safeguarding
- Added intelligent data sanitization:
  - Consistent redaction of sensitive information
  - Context-aware replacement tokens
  - Support for structured data (JSON) sanitization
- Implemented detailed sensitivity reporting with recommendations

### 4. Secure Multi-Agent Sentinel

- Implemented robust multi-agent security:
  - Unique identity and security tokens for each expert
  - Trust relationship management with dynamic trust levels
  - Message verification and authentication
  - Impersonation and manipulation detection
- Added security incident tracking and reporting
- Implemented secure message passing between agents

### 5. Advanced Reliability Monitor

- Implemented comprehensive reliability monitoring:
  - Real-time execution monitoring with checkpoints
  - Consistency checking between inputs and outputs
  - Repetition and pattern detection
  - Detailed error tracking and reporting
- Added reliability scoring for operations
- Implemented historical execution analysis

## Documentation Improvements

We've reorganized and enhanced the documentation:

- Created a comprehensive security enhancements guide (`security_enhancements.md`) that explains the new security architecture and components
- Added a detailed security usage guide (`security_guide.md`) with practical instructions for using the security features
- Updated all documentation to reflect the new security components and features
- Added security best practices and troubleshooting sections
- Created examples demonstrating the security enhancements in action
- Improved the organization and clarity of all security-related documentation

## API Changes

The API has been updated to support the new features:

### Security Components Integration

- Added new security module with four key components:
  - `PromptDefender`: Advanced prompt injection protection
  - `DataGuardian`: Comprehensive data leakage prevention
  - `AgentSentinel`: Secure multi-agent interaction
  - `ReliabilityMonitor`: Enhanced reliability monitoring
- Updated the Expert class to integrate these components
- Enhanced the Operation and Squad classes to use the security components
- Added security-specific logging and reporting

### Enhanced Security Profiles

- Completely redesigned security profiles with a standardized tiered approach:
  - `minimal`: Only critical security checks for development and testing
  - `low`: Basic security checks for non-sensitive applications
  - `standard`: Balanced security for general purpose applications (default)
  - `high`: Strict security validation for sensitive applications
  - `maximum`: Most stringent security for highly sensitive applications
- Implemented backward compatibility with legacy profile names
- Added configurable security thresholds for each profile level
- Created selective security checks based on profile
- Implemented profile-specific validation logic
- Added detailed security profile documentation and examples

### Template Variable Support

- Added support for template variables in expert profiles (specialty, objective, background)
- Added support for template variables in operation instructions and output formats
- Implemented the `_format_with_inputs` method to handle template variable replacement
- Enhanced security methods to be more flexible with template variables
- Modified the relevance checking to handle template variables appropriately

### Result Destination Feature

- Added the `result_destination` parameter to both Operation and Squad classes
- Implemented automatic saving of operation and squad results to specified file paths
- Added support for multiple file formats (.txt, .md, .csv, .json, .html, .pdf)
- Included metadata and guardrail information in saved files
- Added security checks for the result destination path
- Created comprehensive documentation for the result destination feature
- Added examples demonstrating how to use the result destination feature

## Examples

We've added new examples to demonstrate the new features:

- `examples/security/prompt_injection_defense.py`: Demonstrates the advanced prompt injection defense capabilities
- `examples/security/data_leakage_prevention.py`: Shows how to detect and prevent data leakage
- `examples/security/multi_agent_security.py`: Illustrates secure multi-agent interactions
- `examples/security/reliability_monitoring.py`: Demonstrates the reliability monitoring features
- `examples/security_profiles_demo.py`: Shows how to use the new tiered security profiles system
- `examples/custom_security_profiles_demo.py`: Demonstrates how to create and use custom security profiles
- `examples/performance_test.py`: Tests the performance of different security profiles
- `test_security_enhancements.py`: Comprehensive test script that demonstrates all security enhancements
- `examples/example_guardrails.py`: Basic example of guardrails usage
- `examples/advanced_guardrails.py`: Advanced example with complex template variables and conditional formatting
- `examples/security_guardrails.py`: Security-focused example demonstrating how to use guardrails to implement dynamic security controls
- `examples/result_destination_example.py`: Example demonstrating how to use the result_destination parameter to save operation and squad results to different file formats
- `examples/test_result_destination.py`: Test script for the result_destination feature

## Performance Optimizations

Version 0.3.0 includes significant performance optimizations to improve the efficiency of security checks and other operations:

### 1. Caching Mechanisms

- Implemented regex pattern caching to avoid recompiling the same patterns
- Added security validation result caching to avoid repeating the same checks
- Created configurable cache expiration and management

### 2. Tiered Security Checks

- Optimized security validation to perform only necessary checks based on security profile
- Implemented early returns to avoid unnecessary processing
- Created efficient pattern matching algorithms

### 3. Memory Management

- Added cache clearing functionality to prevent memory leaks
- Implemented efficient data structures for security checks
- Optimized memory usage throughout the framework

### 4. Documentation

- Created comprehensive performance optimization guide
- Added best practices for optimizing application performance
- Included advanced techniques for custom optimizations

## Custom Security Profiles

Version 0.3.0 also introduces custom security profiles, allowing users to define their own security settings:

### 1. Custom Profile Registry

- Implemented a registry for custom security profiles
- Added functions to register, retrieve, and list custom profiles
- Created a mechanism to clear the registry when needed

### 2. Flexible Security Configuration

- Added support for user-defined security thresholds
- Implemented user-defined security checks
- Created a system for profile-specific validation logic

### 3. Industry-Specific Profiles

- Added examples of industry-specific security profiles
- Implemented healthcare, finance, and education profiles
- Created a framework for domain-specific security requirements

### 4. Documentation and Examples

- Updated security profiles guide with custom profiles documentation
- Added examples of creating and using custom profiles
- Included best practices for custom profile development


## Future Directions

In future versions, we plan to:

1. Enhance the security components with machine learning-based detection:
   - ML-based prompt injection detection
   - Anomaly detection for unusual agent behavior
   - Automated threat intelligence integration
2. Implement advanced security features:
   - End-to-end encryption for multi-agent communications
   - Formal verification of security properties
   - Automated security testing and validation
3. Expand the guardrails system with more advanced features
4. Add support for more complex conditional logic
5. Improve the integration with external security systems
6. Add more specialized security profiles for different industries and use cases
7. Implement a security recommendation system that suggests improvements to expert and operation configurations
