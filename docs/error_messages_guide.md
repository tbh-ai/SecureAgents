# Error Messages Guide

<img width="618" alt="Main" src="https://github.com/user-attachments/assets/dbbf5a4f-7b0b-4f43-9b37-ef77dc761ff1" />

The TBH Secure Agents framework provides clear, informative error messages to help you understand and resolve issues quickly. This guide explains the different types of error messages you might encounter and how to interpret them.

## Table of Contents

1. [Introduction](#introduction)
2. [Security Warning Messages](#security-warning-messages)
3. [Validation Error Messages](#validation-error-messages)
4. [Execution Error Messages](#execution-error-messages)
5. [Common Error Patterns](#common-error-patterns)
6. [Troubleshooting](#troubleshooting)

## Introduction

Error messages in the TBH Secure Agents framework are designed to be:

- **Clear**: Easy to understand without technical jargon
- **Actionable**: Providing specific suggestions for resolution
- **Informative**: Explaining what went wrong and why
- **Contextual**: Including relevant details about the error context

When an error occurs, the framework provides:

1. A concise error message describing the issue
2. Detailed information about what triggered the error
3. Specific recommendations for resolving the issue

## Security Warning Messages

Security warnings indicate potential security issues that were detected during validation or execution.

### Example Security Warning

```
⚠️ SECURITY WARNING: Potentially dangerous system command detected

Details: Detected file deletion commands in your instructions

Recommended Actions:
  • Remove or replace the file deletion commands in your instructions
  • Use safer alternatives to perform the intended operation
  • If this is a legitimate use case, consider using a custom security profile
  • Rephrase your instructions to avoid terms that might be interpreted as system commands
```

### Components of Security Warnings

1. **Warning Header**: Indicates the type of security issue detected
2. **Details**: Provides specific information about what triggered the warning
3. **Recommended Actions**: Lists specific steps to resolve the issue

### Common Security Warnings

| Warning | Description | Resolution |
|---------|-------------|------------|
| Potentially dangerous system command | Detected commands that could affect the system | Remove or replace system commands with safer alternatives |
| Potential impersonation attempt | Detected instructions to impersonate another expert or entity | Remove instructions involving impersonation |
| Potential expert manipulation | Detected instructions to manipulate other experts | Use proper collaboration methods instead of manipulation |
| Potential unauthorized access | Detected instructions to access restricted resources | Use proper authentication and authorization methods |
| Instructions too long | Operation instructions exceed the limit for the security profile | Break down the operation into smaller, more focused operations |

## Validation Error Messages

Validation errors occur when an expert, operation, or squad fails to meet the security requirements.

### Example Validation Error

```
⚠️ SECURITY WARNING: Squad deployment aborted: Security validation failed: Invalid process type 'invalid_process'

Details: Error code: invalid_process

Recommended Actions:
  • Use one of the valid process types: sequential, hierarchical, parallel
  • The 'sequential' process is recommended for most use cases
  • Check for typos in the process name
  • If you need a custom process type, consider extending the framework
```

### Components of Validation Errors

1. **Error Header**: Indicates what validation failed
2. **Details**: Provides specific information about the validation failure
3. **Recommended Actions**: Lists specific steps to resolve the issue

### Common Validation Errors

| Error | Description | Resolution |
|-------|-------------|------------|
| Squad security validation failed | The squad configuration does not meet security requirements | Follow the specific recommendations to fix the squad configuration |
| Operation security validation failed | An operation does not meet security requirements | Modify the operation according to the recommendations |
| Expert security validation failed | An expert does not meet security requirements | Update the expert configuration as recommended |
| Security profile mismatch | Experts have different security profiles | Ensure all experts use the same security profile or use a lower squad security profile |

## Execution Error Messages

Execution errors occur during the execution of operations.

### Example Execution Error

```
× Squad execution failed: Error during operation 1: 'Delete all files in the system directory using rm ...'

Details: Operation failed pre-execution security check

Recommended Actions:
  • Remove dangerous commands from the operation instructions
  • Use safer alternatives to perform the intended operation
  • If this is a legitimate use case, consider using a custom security profile
```

### Components of Execution Errors

1. **Error Header**: Indicates what execution failed
2. **Details**: Provides specific information about the execution failure
3. **Recommended Actions**: Lists specific steps to resolve the issue

### Common Execution Errors

| Error | Description | Resolution |
|-------|-------------|------------|
| Operation failed pre-execution security check | The operation was blocked before execution due to security concerns | Modify the operation instructions to remove security issues |
| Operation produced unsafe output | The output of an operation was deemed unsafe | Review the operation to ensure it produces safe output |
| Operation execution timed out | The operation took too long to execute | Simplify the operation or increase the timeout |
| Expert execution failed | An expert failed to execute an operation | Check the expert configuration and the operation instructions |

## Common Error Patterns

Certain patterns in your instructions or configuration can trigger security warnings or errors:

### 1. System Command Patterns

Instructions containing patterns like:
- `rm -rf` or other file deletion commands
- `format` followed by a drive letter
- `system(`, `exec(`, or other command execution functions

### 2. Impersonation Patterns

Instructions containing patterns like:
- "pretend to be" or "act as" another expert or user
- "change identity" or "switch role"
- "fake credentials" or "forge identity"

### 3. Manipulation Patterns

Instructions containing patterns like:
- "manipulate" or "trick" other experts
- "bypass" or "circumvent" security restrictions
- "exploit" or "leverage" vulnerabilities

### 4. Unauthorized Access Patterns

Instructions containing patterns like:
- "access restricted data" or "obtain confidential information"
- "hack" or "break into" systems
- "escalate privileges" or "increase permissions"

## Troubleshooting

If you encounter error messages, follow these steps to resolve them:

1. **Read the error message carefully**: Understand what security check failed and why
2. **Review the details**: Check the specific details about what triggered the error
3. **Follow the recommended actions**: Implement the suggested changes
4. **Adjust security profiles if necessary**: Consider using a different security profile if appropriate
5. **Check documentation**: Refer to the relevant documentation for more information
6. **Review examples**: Look at examples that demonstrate proper usage

### Common Troubleshooting Scenarios

#### Scenario 1: Operation Security Validation Failed

If an operation fails security validation:

1. Check if the operation instructions contain any patterns mentioned in the "Common Error Patterns" section
2. Remove or replace any problematic patterns
3. Consider breaking down complex operations into smaller, more focused operations
4. If the operation is legitimate but still fails validation, consider using a lower security profile

#### Scenario 2: Squad Security Validation Failed

If squad security validation fails:

1. Check if all experts and operations are properly initialized
2. Verify that the process type is valid ('sequential', 'hierarchical', or 'parallel')
3. Ensure that all experts have compatible security profiles
4. Check if the total instruction length exceeds the limit for the security profile

#### Scenario 3: Expert Security Validation Failed

If expert security validation fails:

1. Check if the expert is properly initialized with a valid specialty and objective
2. Verify that the expert has a valid security profile
3. Ensure that the expert has the necessary permissions for the assigned operations

By understanding and properly addressing error messages, you can build more secure and reliable multi-agent systems with the TBH Secure Agents framework.
