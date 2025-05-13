# Performance Optimization Guide

This guide explains the performance optimization techniques used in the TBH Secure Agents framework and how to use them effectively.

## Overview

The TBH Secure Agents framework includes several performance optimization techniques to improve the efficiency of security checks and other operations. These optimizations are particularly important for applications that process large amounts of data or have strict performance requirements.

## Caching Mechanisms

### Regex Pattern Caching

Regular expression patterns are compiled and cached to avoid recompiling the same patterns multiple times. This significantly improves the performance of security checks that use regex patterns.

```python
# Example of using cached regex patterns
from tbh_secure_agents.security_profiles import get_cached_regex

# Instead of this (slow):
import re
if re.search(pattern, text, re.IGNORECASE):
    # Do something

# Use this (fast):
if get_cached_regex(pattern).search(text):
    # Do something
```

### Security Validation Caching

Security validation results are cached to avoid repeating the same checks for the same inputs. This is particularly useful for operations that are validated multiple times during execution.

```python
# Example of using security validation caching
from tbh_secure_agents.security_profiles import cache_security_validation

# Apply the decorator to your validation method
@cache_security_validation
def validate_security(text):
    # Perform expensive security checks
    return is_secure
```

### Cache Configuration

The caching system is configured with the following parameters:

- **Cache Expiration**: 300 seconds (5 minutes) by default
- **Cache Size**: Unlimited (automatically managed by Python's garbage collector)

## Security Profile Optimizations

### Tiered Security Checks

The framework uses a tiered approach to security checks, performing only the necessary checks based on the security profile:

- **Minimal**: Only critical security checks
- **Low**: Basic security checks
- **Standard**: Balanced security checks
- **High**: Comprehensive security checks
- **Maximum**: Most stringent security checks

This approach ensures that only the necessary checks are performed, improving performance for less security-sensitive applications.

### Early Returns

Security validation methods use early returns to avoid unnecessary checks:

```python
def validate_security(text, security_profile):
    # For minimal security, only perform basic checks
    if security_profile == "minimal":
        # Perform minimal checks
        return result
        
    # For low security, perform basic checks
    if security_profile == "low":
        # Perform low security checks
        return result
        
    # For standard and higher, perform comprehensive checks
    # ...
```

This approach ensures that only the necessary checks are performed based on the security profile.

## Regex Optimization

### Pattern Consolidation

Where possible, multiple regex patterns are consolidated into a single pattern to reduce the number of regex operations:

```python
# Instead of this (slow):
patterns = [r'pattern1', r'pattern2', r'pattern3']
for pattern in patterns:
    if get_cached_regex(pattern).search(text):
        return True

# Use this (faster):
combined_pattern = r'pattern1|pattern2|pattern3'
if get_cached_regex(combined_pattern).search(text):
    return True
```

### Efficient Patterns

Regex patterns are optimized for performance:

- Using non-capturing groups `(?:...)` instead of capturing groups `(...)`
- Using word boundaries `\b` to avoid unnecessary backtracking
- Using character classes `[...]` instead of alternation `|` where possible
- Avoiding excessive use of lookahead/lookbehind assertions

## Parallel Processing

For squads with multiple operations, the framework supports parallel processing to improve performance:

```python
# Example of using parallel processing
squad = Squad(
    experts=[expert1, expert2],
    operations=[op1, op2, op3],
    process="parallel"  # Use parallel processing
)
```

The parallel processing mode executes operations concurrently, which can significantly improve performance for independent operations.

## Memory Management

### Cache Clearing

The framework provides a method to clear caches when they are no longer needed:

```python
from tbh_secure_agents.security_profiles import clear_caches

# Clear all caches
clear_caches()
```

This can be useful for long-running applications to prevent memory leaks.

### Efficient Data Structures

The framework uses efficient data structures to minimize memory usage:

- Using sets for membership testing
- Using dictionaries for fast lookups
- Using generators instead of lists where possible

## Best Practices

### 1. Choose the Right Security Profile

Select the appropriate security profile based on your security requirements:

- Use `minimal` for development and testing
- Use `low` for non-sensitive applications
- Use `standard` for general-purpose applications
- Use `high` for sensitive applications
- Use `maximum` for highly sensitive applications

Using a lower security profile can significantly improve performance.

### 2. Use Parallel Processing When Appropriate

Use parallel processing for squads with multiple independent operations:

```python
squad = Squad(
    experts=[expert1, expert2],
    operations=[op1, op2, op3],
    process="parallel"
)
```

But be careful with operations that depend on each other:

```python
squad = Squad(
    experts=[expert1, expert2],
    operations=[op1, op2, op3],
    process="sequential"  # Use sequential processing for dependent operations
)
```

### 3. Optimize Operation Instructions

Keep operation instructions concise and focused:

```python
# Instead of this (slow):
operation = Operation(
    instructions="Very long and detailed instructions with lots of unnecessary information...",
    expert=expert
)

# Use this (faster):
operation = Operation(
    instructions="Concise and focused instructions",
    expert=expert
)
```

Shorter instructions are faster to validate and process.

### 4. Batch Operations

Group related operations together to reduce overhead:

```python
# Instead of this (slow):
squad1 = Squad(experts=[expert1], operations=[op1])
squad2 = Squad(experts=[expert2], operations=[op2])
squad3 = Squad(experts=[expert3], operations=[op3])

result1 = squad1.deploy()
result2 = squad2.deploy()
result3 = squad3.deploy()

# Use this (faster):
squad = Squad(
    experts=[expert1, expert2, expert3],
    operations=[op1, op2, op3],
    process="parallel"
)

results = squad.deploy()
```

### 5. Monitor Performance

Monitor the performance of your application and identify bottlenecks:

```python
import time

start_time = time.time()
result = squad.deploy()
end_time = time.time()

print(f"Execution time: {end_time - start_time:.2f} seconds")
```

Use this information to optimize your application.

## Advanced Techniques

### Custom Caching

You can implement custom caching for specific use cases:

```python
import functools

def custom_cache(func):
    """Custom caching decorator for specific use cases."""
    cache = {}
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    
    return wrapper
```

### Profiling

Use Python's profiling tools to identify performance bottlenecks:

```python
import cProfile

def profile_execution():
    squad = Squad(experts=[expert], operations=[operation])
    cProfile.runctx('squad.deploy()', globals(), locals())

profile_execution()
```

This will help you identify which parts of your code are taking the most time.

## Conclusion

By following these performance optimization techniques, you can significantly improve the efficiency of your TBH Secure Agents applications while maintaining strong security. Remember to balance performance with security based on your specific requirements.
