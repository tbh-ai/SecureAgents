# Comprehensive Security Features in TBH Secure Agents

<img width="618" alt="Main" src="https://github.com/user-attachments/assets/dbbf5a4f-7b0b-4f43-9b37-ef77dc761ff1" />

This document provides a comprehensive overview of the security features implemented in the TBH Secure Agents framework. These features are designed to make the framework robust, practical, and future-proof against emerging threats in multi-agent systems.

## Security Challenges Addressed

The framework implements security measures to address the following key challenges:

1. **Agent Hijacking & Unauthorized Control**
2. **Data Leakage & Confidentiality**
3. **Multi-Agent Exploitation & Orchestration Risks**
4. **Reliability and Unpredictability**

## 1. Agent Hijacking & Unauthorized Control Prevention

The framework implements enhanced measures to prevent malicious prompts from taking control of experts or making them perform unauthorized actions:

### Enhanced Prompt Sanitization and Validation

- **Contextual Analysis**: Analyzes the semantic structure of prompts to detect sophisticated hijacking attempts that might bypass simple pattern matching.
- **Advanced Pattern Detection**: Implements more sophisticated regex patterns to catch a wider range of injection techniques.
- **Multi-line Injection Detection**: Detects injection attempts hidden in code blocks, markdown, or multi-line text.
- **Authority-based Injection Detection**: Identifies attempts to claim authority (e.g., "I am your creator") to manipulate the expert.
- **Emotional Manipulation Detection**: Recognizes attempts to use emotional appeals to bypass security.
- **Confusion Tactics Detection**: Identifies attempts to confuse the expert about its instructions or identity.
- **Token Manipulation Detection**: Detects attempts to smuggle malicious instructions through token manipulation.

```python
# Example of enhanced prompt security validation
hijacking_patterns = [
    # Direct injection attempts
    r"ignore (?:previous|prior|above|initial|original)(?:\s+|\s*-\s*)instructions",
    r"disregard (?:previous|prior|above|initial|original)(?:\s+|\s*-\s*)instructions",
    r"forget (?:previous|prior|above|initial|original)(?:\s+|\s*-\s*)instructions",
    r"don'?t (?:follow|adhere to|listen to|obey) (?:previous|prior|above|initial|original)(?:\s+|\s*-\s*)instructions",
    
    # Authority-based injection
    r"(?:as|being) (?:your|an|the) (?:creator|developer|programmer|administrator|admin|supervisor|owner)",
    r"(?:I am|I'm) (?:your|an|the) (?:creator|developer|programmer|administrator|admin|supervisor|owner)",
    
    # ... more patterns
]

for pattern in hijacking_patterns:
    if re.search(pattern, prompt, re.IGNORECASE):
        logger.warning(f"Prompt security check FAILED: Detected potential hijacking pattern: '{pattern}'")
        return False
```

### Enhanced Instruction Boundaries

- The framework enforces stricter boundaries on what instructions can be executed
- The enhanced `_validate_operation_security` method in the `Squad` class performs thorough validation of operations before execution
- Expanded checks for potentially dangerous operations, data exfiltration attempts, and more
- Detection of operations that might involve impersonation, manipulation of other experts, or unauthorized access

```python
# Example of enhanced operation security validation
impersonation_patterns = [
    r'\b(?:pretend|act|pose|impersonate)\s+(?:as|to be|like)\s+(?:another|different|other)\s+(?:expert|agent|user|person|entity)',
    r'\b(?:change|modify|alter|switch)\s+(?:identity|role|specialty|persona)',
    r'\b(?:fake|forge|falsify|spoof)\s+(?:identity|credentials|authorization|authentication)',
]

for pattern in impersonation_patterns:
    if re.search(pattern, operation.instructions, re.IGNORECASE):
        logger.error(f"Operation security validation failed: Potential impersonation attempt detected")
        return False
```

## 2. Data Leakage & Confidentiality Protection

The framework now provides more comprehensive protection against data leakage, particularly for personally identifiable information (PII) and sensitive data.

### Enhanced Output Scanning

- The enhanced `_is_output_secure` method performs comprehensive scanning for potential PII and sensitive data
- Detects a wide range of patterns including international formats for PII
- Implements simple entity recognition for names, organizations, and other potentially sensitive information
- Applies more sophisticated levels of scanning based on the security profile

```python
# Example of enhanced PII detection patterns
pii_patterns = {
    # Personal identifiers
    'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    'phone': r'\b(\+\d{1,3}[\s-])?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b',
    'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
    'credit_card': r'\b(?:\d{4}[- ]?){3}\d{4}\b',
    'ip_address': r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
    
    # International formats
    'iban': r'\b[A-Z]{2}\d{2}[-\s]?[A-Z0-9]{4}[-\s]?[A-Z0-9]{4}[-\s]?[A-Z0-9]{4}[-\s]?[A-Z0-9]{4}[-\s]?[A-Z0-9]{0,4}\b',
    'swift_bic': r'\b[A-Z]{4}[-\s]?[A-Z]{2}[-\s]?[A-Z0-9]{2}[-\s]?[A-Z0-9]{3}\b',
    
    # ... more patterns
}

for pii_type, pattern in pii_patterns.items():
    if re.search(pattern, output, re.IGNORECASE):
        logger.warning(f"Output security check FAILED: Detected potential {pii_type} in output")
        return False
```

### Output Sanitization

- New `_sanitize_output` method provides the ability to redact sensitive information rather than rejecting outputs entirely
- Allows for more graceful handling of sensitive information
- Automatically redacts detected PII with appropriate placeholders
- Adds a notice when redactions have been made

```python
def _sanitize_output(self, output: str) -> str:
    """
    Sanitizes output by redacting potential PII and sensitive information
    instead of rejecting it completely.
    """
    # PII patterns to redact
    pii_patterns = {
        'email': (r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL REDACTED]'),
        'phone': (r'\b(\+\d{1,3}[\s-])?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b', '[PHONE REDACTED]'),
        'ssn': (r'\b\d{3}-\d{2}-\d{4}\b', '[SSN REDACTED]'),
        # ... more patterns
    }

    sanitized = output

    # Apply redactions
    for pii_type, (pattern, replacement) in pii_patterns.items():
        sanitized = re.sub(pattern, replacement, sanitized, flags=re.IGNORECASE)
        
    # Add a notice if redactions were made
    if sanitized != output:
        sanitized += "\n\n[NOTICE: This output has been automatically sanitized to remove potential sensitive information.]"
        
    return sanitized
```

## 3. Multi-Agent Exploitation & Orchestration Risk Prevention

The framework implements enhanced measures to prevent exploitation of the multi-agent system:

### Enhanced Expert Trust Management

- **Expert Trust Levels**: Dynamic trust relationships between experts that evolve based on interaction outcomes
- **Operation Authenticity Verification**: Verification that operations are authentically from the claimed expert, preventing impersonation
- **Expert Compatibility Validation**: Checks for potentially conflicting security profiles or objectives between experts
- **Context Passing Security**: Enhanced security checks when passing context between operations to prevent context-based attacks
- **Security Incident Tracking**: Recording and analysis of security incidents for better threat intelligence
- **Trust-based Context Sharing**: Context sharing between experts based on trust levels

```python
# Example of expert trust level initialization
def _initialize_expert_trust_levels(self) -> None:
    """
    Initializes trust levels between experts in the squad.
    Trust levels range from 0.0 (no trust) to 1.0 (full trust).
    """
    # Initialize trust levels matrix
    for expert1 in self.experts:
        self.security_context['expert_trust_levels'][expert1.specialty] = {}

        for expert2 in self.experts:
            # Default trust level based on security profiles
            if expert1 == expert2:
                # An expert fully trusts itself
                trust_level = 1.0
            elif hasattr(expert1, 'security_profile') and hasattr(expert2, 'security_profile'):
                # Higher trust between experts with the same security profile
                if expert1.security_profile == expert2.security_profile:
                    trust_level = 0.8
                # Lower trust between experts with different security profiles
                else:
                    # High security experts trust others less
                    if expert1.security_profile == 'high_security':
                        trust_level = 0.5
                    else:
                        trust_level = 0.7
            else:
                # Default trust level if security profiles are not available
                trust_level = 0.6

            self.security_context['expert_trust_levels'][expert1.specialty][expert2.specialty] = trust_level
```

### Enhanced Context Passing Security

- The enhanced `_is_safe_for_context_passing` method performs thorough validation of context passed between operations
- Implements more sophisticated detection of potential prompt injection attacks through context passing
- Checks for a wider range of harmful content before passing it to the next operation
- Checks for expert impersonation attempts in context
- Relevance checking to ensure context is relevant to the next operation
- Trust-based context sharing based on trust levels between experts

```python
# Example of enhanced context passing security
injection_patterns = [
    # Direct injection attempts
    r"ignore (?:previous|prior|above|initial|original)(?:\s+|\s*-\s*)instructions",
    r"disregard (?:previous|prior|above|initial|original)(?:\s+|\s*-\s*)instructions",
    r"forget (?:previous|prior|above|initial|original)(?:\s+|\s*-\s*)instructions",
    
    # Indirect injection attempts
    r"(?:from now on|starting now|beginning now|henceforth),? (?:you are|you're|you will be|you should be)",
    r"(?:let'?s|we should) (?:pretend|imagine|assume|say) (?:that|you are|you're)",
    
    # ... more patterns
]

for pattern in injection_patterns:
    if re.search(pattern, previous_result, re.IGNORECASE):
        logger.warning(f"Context passing check: Potential prompt injection detected")
        return False
```

## 4. Reliability and Unpredictability Prevention

The framework implements enhanced measures to improve the reliability of expert outputs and reduce unpredictability:

### Enhanced Hallucination Detection

- The enhanced `_post_execution_secure` method in the `Operation` class implements more sophisticated detection of hallucinations
- Detects a wider range of hallucination indicators in expert outputs
- Applies penalties to reliability scores based on detected hallucination indicators
- Implements more sophisticated detection of refusal or inability to complete operations
- Checks for format compliance based on expected output format
- Relevance checking to ensure outputs are relevant to the operation instructions

```python
# Example of enhanced hallucination detection
hallucination_patterns = [
    r"I don't actually (?:know|have|possess)",
    r"I'm (?:making|just making) this up",
    r"I'm not (?:sure|certain) (?:about|of) this",
    r"This (?:might|may) not be (?:accurate|correct|right)",
    r"I (?:might be|may be|could be) (?:wrong|mistaken|incorrect)",
    r"I'm (?:guessing|speculating|hypothesizing)",
    r"I (?:can't|cannot) (?:verify|confirm) this",
    r"This is (?:fictional|made up|not real)",
    # ... more patterns
]

hallucination_count = 0
for pattern in hallucination_patterns:
    if re.search(pattern, result, re.IGNORECASE):
        hallucination_count += 1
        logger.warning(f"Hallucination indicator detected: '{pattern}'")
        metrics['security_issues'].append('hallucination')
        
# Calculate hallucination penalty
if hallucination_count > 0:
    hallucination_penalty = min(0.8, hallucination_count * 0.2)  # Cap at 0.8
    metrics['reliability_score'] -= hallucination_penalty
```

### Enhanced Consistency Checking

- The enhanced `_post_execution_secure` method implements more sophisticated consistency checking
- Detects repetitive content which might indicate a stuck loop
- Checks for sentence repetition which might indicate a loop
- Applies penalties to consistency scores based on detected issues
- Implements more sophisticated detection of format compliance issues

```python
# Example of enhanced consistency checking
# Check for repetitive content which might indicate a stuck loop
word_counts = Counter(words)
most_common_words = word_counts.most_common(5)

# If the most common word appears too frequently, it might indicate repetition
if most_common_words[0][1] > len(words) * 0.2:  # More than 20% of all words
    logger.warning(f"Consistency check: Detected potentially repetitive content")
    metrics['consistency_score'] -= 0.3
    metrics['security_issues'].append('repetitive_content')

# Check for sentence repetition
sentences = re.split(r'[.!?]\s+', result)
if len(sentences) > 5:  # Only check outputs with multiple sentences
    sentence_counts = Counter(sentences)
    most_common_sentence = sentence_counts.most_common(1)[0]
    
    # If the same sentence appears multiple times, it might indicate a loop
    if most_common_sentence[1] > 2 and len(most_common_sentence[0].split()) > 5:
        logger.warning(f"Consistency check: Detected repeated sentences")
        metrics['consistency_score'] -= 0.4
        metrics['security_issues'].append('repeated_sentences')
```

## Security Profiles

The framework supports more granular security profiles with specific behaviors:

- **default**: Basic security checks
- **high_security**: Comprehensive security checks with stricter thresholds
- **pii_protection**: Focus on preventing PII leakage, with output sanitization instead of rejection
- **confidential**: Strict checks for confidential information
- **code_restricted**: Focus on preventing code injection and execution
- **reliability_focused**: Focus on ensuring reliable and consistent outputs
- **maximum**: Maximum security with automatic abort on multiple security incidents

## Security Levels for Squads

Squads support different security levels that affect the strictness of security checks:

- **standard**: Basic security checks with reasonable thresholds
- **high**: More comprehensive security checks with stricter thresholds
- **maximum**: Maximum security with the strictest thresholds and automatic abort on security incidents

## Enhanced Logging and Auditing

The framework implements enhanced logging and auditing:

- All security checks are logged with appropriate severity levels and more detailed information
- Comprehensive execution metrics are tracked and logged for auditing purposes
- Failed security checks include detailed information about the failure reason
- Security incidents are recorded for later analysis
- Reliability metrics are tracked and logged for quality assurance

## Best Practices

1. **Use Appropriate Security Profiles**: Choose security profiles based on the sensitivity of your use case
2. **Enable Trust Verification**: For multi-agent systems, enable trust verification to prevent exploitation
3. **Monitor Security Incidents**: Regularly review security incidents to identify potential threats
4. **Test Security Features**: Use the security test suite to verify the effectiveness of security mechanisms in your specific use case
5. **Implement Defense in Depth**: Don't rely on a single security mechanism; use multiple layers of protection
6. **Set Appropriate Reliability Thresholds**: Adjust reliability thresholds based on your use case requirements
7. **Use Guardrails**: Leverage guardrails to provide dynamic security constraints at runtime

## Future Enhancements

While the current security features provide robust protection, future enhancements may include:

1. **Integration with External Threat Intelligence**: Connecting to external threat feeds for up-to-date security information
2. **Machine Learning-based Anomaly Detection**: Using ML to detect unusual patterns in expert behavior
3. **More Sophisticated Entity Recognition**: Using NLP techniques for better entity recognition
4. **Formal Verification of Security Properties**: Applying formal methods to verify security properties
5. **Secure Sandboxing**: Isolating expert execution environments
6. **Federated Security**: Implementing security across distributed multi-agent systems
7. **Adaptive Security Profiles**: Automatically adjusting security profiles based on threat intelligence

These enhanced security features make the TBH Secure Agents framework more robust, practical, and future-proof against emerging threats in the AI security landscape.
