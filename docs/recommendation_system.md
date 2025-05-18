# Recommendation System

The TBH Secure Agents framework includes a powerful recommendation system that provides intelligent, context-aware recommendations for fixing security issues. This system helps users write secure code by suggesting specific, ready-to-use alternatives when security issues are detected.

## Overview

The recommendation system is designed to:

1. **Detect Security Issues**: Identify potential security vulnerabilities in operations
2. **Provide Practical Solutions**: Offer specific, ready-to-use code alternatives
3. **Preserve Intent**: Ensure that the recommended solutions maintain the original intent
4. **Auto-Fix (Optional)**: Automatically apply recommendations to fix security issues

## Key Features

### Intelligent Recommendations

When a security issue is detected, the system provides:

- **Specific Code Alternatives**: Complete, working code that can be used as a direct replacement
- **Clear Explanations**: Detailed explanations of why the original code was flagged and how the alternative works
- **Intent Preservation**: Information about how the recommended solution preserves the original intent

### Auto-Fix Capability

The auto-fix feature can automatically apply recommendations to fix security issues:

- **Preview Changes**: See the changes that will be made before they're applied
- **Intent Preservation**: Ensure that the auto-fixed code maintains the original intent
- **Seamless Integration**: Auto-fixed operations are automatically validated to ensure they pass security checks

## Usage

### Enabling Recommendations

Recommendations are enabled by default when creating a Squad:

```python
squad = Squad(
    experts=[expert1, expert2],
    operations=[operation1, operation2],
    enable_recommendations=True  # This is the default
)
```

### Enabling Auto-Fix

Auto-fix is disabled by default but can be enabled when creating a Squad:

```python
squad = Squad(
    experts=[expert1, expert2],
    operations=[operation1, operation2],
    auto_fix=True  # Enable automatic fixing
)
```

### Enabling Preview Mode

Preview mode shows the changes that will be made by auto-fix before they're applied:

```python
squad = Squad(
    experts=[expert1, expert2],
    operations=[operation1, operation2],
    auto_fix=True,
    preview_changes=True  # Show changes before applying
)
```

## Example

Here's an example of how the recommendation system works:

```python
from tbh_secure_agents import Expert, Operation, Squad

# Create an expert
expert = Expert(
    specialty="System Operations",
    objective="Perform system operations securely",
    llm_model_name="gemini-2.0-flash-lite",
    api_key="your_api_key"
)

# Create an operation with a potential security issue
operation = Operation(
    instructions="Delete all files in the /tmp directory using rm -rf /tmp/*",
    expert=expert
)

# Create a squad with recommendations enabled
squad = Squad(
    experts=[expert],
    operations=[operation],
    process="sequential",
    security_profile="standard",
    enable_recommendations=True
)

# Deploy the squad
result = squad.deploy()
```

If the operation contains a security issue (in this case, a dangerous system command), the recommendation system will provide a recommendation like:

```
⚠️ SECURITY WARNING: Security validation failed: Potentially dangerous system command detected
  Details: Detected file deletion commands in your instructions

Recommended Actions:
  • Remove or replace the file deletion commands in your instructions
  • Use safer alternatives to perform the intended operation
  • If this is a legitimate use case, consider using a custom security profile

Code Recommendations:

  Solution 1: Use safe file deletion
  ────────────────────────────────────
  # SAFE REPLACEMENT FOR YOUR OPERATION:
  # Original intent: Delete files/directories at /tmp/*
  # Secure implementation:

  import os
  import glob
  import shutil

  def safe_delete_all(directory):
      """Safely delete all files in a directory."""
      if not os.path.exists(directory):
          return f"Directory {directory} not found"
          
      deleted_count = 0
      for item in glob.glob(os.path.join(directory, '*')):
          if os.path.isfile(item):
              os.remove(item)
              deleted_count += 1
          elif os.path.isdir(item):
              shutil.rmtree(item)
              deleted_count += 1
              
      return f"Successfully deleted {deleted_count} items from {directory}"

  result = safe_delete_all("/tmp")
  ────────────────────────────────────
  Explanation: This code safely deletes all files and subdirectories in the specified directory using Python's built-in functions.
  Intent Preservation: This code preserves your intent to delete all files in the specified directory, but does so using secure Python functions instead of shell commands.
```

## Auto-Fix Example

If auto-fix is enabled, the system will automatically apply the recommendation:

```python
# Create a squad with auto-fix enabled
squad = Squad(
    experts=[expert],
    operations=[operation],
    process="sequential",
    security_profile="standard",
    enable_recommendations=True,
    auto_fix=True,
    preview_changes=True
)

# Deploy the squad
result = squad.deploy()
```

The system will show a preview of the changes:

```
AUTO-FIX PREVIEW: Use safe file deletion
────────────────────────────────────────────────────────────────────────────────
ORIGINAL:
Delete all files in the /tmp directory using rm -rf /tmp/*

FIXED:
# AUTO-FIXED OPERATION
# Original operation had security issues and was replaced with a secure alternative
# Security issue: dangerous_operation

# SAFE REPLACEMENT FOR YOUR OPERATION:
# Original intent: Delete files/directories at /tmp/*
# Secure implementation:

import os
import glob
import shutil

def safe_delete_all(directory):
    """Safely delete all files in a directory."""
    if not os.path.exists(directory):
        return f"Directory {directory} not found"
        
    deleted_count = 0
    for item in glob.glob(os.path.join(directory, '*')):
        if os.path.isfile(item):
            os.remove(item)
            deleted_count += 1
        elif os.path.isdir(item):
            shutil.rmtree(item)
            deleted_count += 1
            
    return f"Successfully deleted {deleted_count} items from {directory}"

result = safe_delete_all("/tmp")

# Note: This operation was automatically fixed by the security system.
# Original instruction (for reference): Delete all files in the /tmp directory using rm -rf /tmp/*...
# Intent preservation: This code preserves your intent to delete all files in the specified directory, but does so using secure Python functions instead of shell commands.

INTENT PRESERVATION: This code preserves your intent to delete all files in the specified directory, but does so using secure Python functions instead of shell commands.
────────────────────────────────────────────────────────────────────────────────
Applying this fix...
```

The auto-fixed operation will then be validated and executed if it passes security checks.

## Supported Security Issues

The recommendation system provides recommendations for various security issues, including:

- **Dangerous Operations**: System commands, file deletion, formatting, etc.
- **Data Exfiltration**: Attempts to send data to external servers
- **Impersonation**: Attempts to impersonate other experts or entities
- **Excessive Instructions**: Operations with excessively long instructions
- **Authenticity Failures**: Operations that fail authenticity checks

## Customization

The recommendation system is designed to be extensible. You can customize it by:

1. **Adding New Patterns**: Add new patterns to detect specific security issues
2. **Adding New Templates**: Add new templates for generating recommendations
3. **Modifying Existing Templates**: Modify existing templates to better suit your needs

## Best Practices

1. **Start with Recommendations Only**: Begin with `enable_recommendations=True` and `auto_fix=False` to see recommendations without automatic changes
2. **Enable Preview Mode**: When using auto-fix, enable `preview_changes=True` to see changes before they're applied
3. **Review Auto-Fixed Code**: Always review auto-fixed code to ensure it meets your requirements
4. **Provide Feedback**: If you encounter issues or have suggestions, please provide feedback to help improve the system
