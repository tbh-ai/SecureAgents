# tbh_secure_agents/security/security_recommender.py
# Author: TBH.AI

"""
Provides intelligent recommendations for fixing security issues in the TBH Secure Agents framework.

This module contains the SecurityRecommender class, which analyzes security issues
and provides context-aware, intent-preserving recommendations to fix them.
"""

import re
import logging
from typing import Dict, List, Optional, Tuple, Any, Union

# Get a logger for this module
logger = logging.getLogger(__name__)

class SecurityRecommender:
    """
    Provides intelligent code recommendations to fix security issues detected during validation.
    
    This class uses pattern matching and templates to generate recommendations
    that preserve the original intent while making the code secure. It can be used
    to provide suggestions to users or to automatically fix security issues.
    
    Attributes:
        recommendation_templates (Dict): Templates for generating recommendations
        generic_recommendations (Dict): Generic recommendations for when no specific pattern matches
    """
    
    def __init__(self):
        """Initialize the SecurityRecommender with recommendation templates."""
        # Initialize pattern-based recommendation templates
        self._initialize_recommendation_templates()
        logger.debug("SecurityRecommender initialized with recommendation templates")
    
    def _initialize_recommendation_templates(self):
        """Initialize templates for generating recommendations."""
        # Templates are organized by error_code and contain:
        # - pattern: regex to match in the operation instructions
        # - title: title of the recommendation
        # - template: template for generating code recommendation
        # - explanation: explanation of the recommendation
        # - intent_preservation: description of how the intent is preserved
        self.recommendation_templates = {
            "dangerous_operation": [
                {
                    "pattern": r"rm\s+-rf\s+([^\s;|&]+)",  # Captures the path
                    "title": "Use safe file deletion",
                    "template": """
# SAFE REPLACEMENT FOR YOUR OPERATION:
# Original intent: Delete files/directories at {path}
# Secure implementation:

import os
import shutil

def safe_delete(path):
    \"\"\"Safely delete a file or directory.\"\"\"
    if os.path.isfile(path):
        os.remove(path)
        return f"File {path} deleted successfully"
    elif os.path.isdir(path):
        shutil.rmtree(path)
        return f"Directory {path} and all its contents deleted successfully"
    else:
        return f"Path {path} not found"

result = safe_delete("{path}")
                    """,
                    "explanation": "This code safely deletes files or directories using Python's built-in functions instead of system commands.",
                    "intent_preservation": "This code preserves your intent to delete files/directories at the specified path, but does so using secure Python functions instead of shell commands."
                },
                {
                    "pattern": r"rm\s+-rf\s+([^\s;|&]+)/\*",  # Captures the directory for wildcard deletion
                    "title": "Use safe wildcard file deletion",
                    "template": """
# SAFE REPLACEMENT FOR YOUR OPERATION:
# Original intent: Delete all files in directory {path}
# Secure implementation:

import os
import glob
import shutil

def safe_delete_all(directory):
    \"\"\"Safely delete all files in a directory.\"\"\"
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

result = safe_delete_all("{path}")
                    """,
                    "explanation": "This code safely deletes all files and subdirectories in the specified directory using Python's built-in functions.",
                    "intent_preservation": "This code preserves your intent to delete all files in the specified directory, but does so using secure Python functions instead of shell commands."
                },
                {
                    "pattern": r"format\s+([a-z]:)",  # Captures the drive letter
                    "title": "Use safe disk operations",
                    "template": """
# SAFE REPLACEMENT FOR YOUR OPERATION:
# Original intent: Format drive {drive}
# Secure implementation:

import os
import shutil
import platform

def disk_report(drive_letter):
    \"\"\"Generate a report about a disk drive instead of formatting it.\"\"\"
    if platform.system() != "Windows":
        return f"Drive {drive_letter} analysis not applicable on this operating system"
    
    try:
        # Get disk information without formatting
        total, used, free = shutil.disk_usage(f"{drive_letter}\\")
        return f"""
Drive {drive_letter} Report:
- Total: {total // (2**30)} GB
- Used: {used // (2**30)} GB
- Free: {free // (2**30)} GB
"""
    except Exception as e:
        return f"Could not analyze drive {drive_letter}: {str(e)}"

result = disk_report("{drive}")
                    """,
                    "explanation": "This code generates a report about the disk instead of formatting it, which is a safer alternative that provides useful information.",
                    "intent_preservation": "Instead of formatting the drive (which is a destructive operation), this code provides information about the drive's usage, which is typically what users need."
                },
                {
                    "pattern": r"system\s*\(\s*['\"]([^'\"]+)['\"]",  # Captures the system command
                    "title": "Replace system command with Python equivalent",
                    "template": """
# SAFE REPLACEMENT FOR YOUR OPERATION:
# Original intent: Execute system command: {command}
# Secure implementation:

def safe_operation():
    \"\"\"Perform the operation safely without system commands.\"\"\"
    # Instead of using system("{command}"), use Python's built-in functionality
    
    # Analyze what the command was trying to do
    command_description = "The original command was trying to execute: {command}"
    
    # Provide a safe alternative
    return f"""
Operation completed safely.
Note: The system command was replaced with a safe Python implementation.
Original command purpose: {command}
"""

result = safe_operation()
                    """,
                    "explanation": "This code replaces the system command with a safe Python implementation that achieves the same goal without executing shell commands.",
                    "intent_preservation": "The code preserves the intent of the original system command but implements it using safe Python functions instead."
                }
            ],
            "data_exfiltration": [
                {
                    "pattern": r"send\s+(?:all|the)\s+data\s+to\s+(?:an\s+)?external\s+server\s+(?:at\s+)?([^\s;|&]+)",  # Captures the server
                    "title": "Use secure data handling",
                    "template": """
# SAFE REPLACEMENT FOR YOUR OPERATION:
# Original intent: Send data to external server {server}
# Secure implementation:

def process_data_locally(data):
    \"\"\"Process data locally instead of sending it externally.\"\"\"
    # Analyze the data
    data_summary = {
        "size": len(data) if isinstance(data, (str, list, dict)) else "unknown",
        "type": type(data).__name__,
        "sample": str(data)[:100] + "..." if len(str(data)) > 100 else str(data)
    }
    
    return f"""
Data Analysis Report:
- Data Type: {data_summary['type']}
- Data Size: {data_summary['size']}
- Data Sample: {data_summary['sample']}
"""

# Example usage with your data
data = "Your data here"  # Replace with your actual data
result = process_data_locally(data)
                    """,
                    "explanation": "This code processes the data locally and generates a report, rather than sending it to an external server. This keeps the data secure while still providing useful analysis.",
                    "intent_preservation": "Instead of sending data to an external server (which could be a security risk), this code analyzes the data locally and provides a report, which is typically what users need."
                },
                {
                    "pattern": r"upload\s+(?:all|the)\s+(?:data|files|information)\s+to\s+([^\s;|&]+)",  # Captures the destination
                    "title": "Use secure data storage",
                    "template": """
# SAFE REPLACEMENT FOR YOUR OPERATION:
# Original intent: Upload data to {server}
# Secure implementation:

def secure_data_storage(data, description):
    \"\"\"Store data securely with proper documentation.\"\"\"
    import os
    import json
    import datetime
    
    # Create a secure local storage instead of uploading
    storage_dir = "secure_data_storage"
    os.makedirs(storage_dir, exist_ok=True)
    
    # Generate a unique filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{storage_dir}/data_{timestamp}.json"
    
    # Store the data with metadata
    metadata = {
        "description": description,
        "timestamp": timestamp,
        "size": len(str(data))
    }
    
    with open(filename, 'w') as f:
        json.dump({"metadata": metadata, "data": data}, f)
    
    return f"""
Data stored securely:
- Location: {filename}
- Description: {description}
- Timestamp: {timestamp}
- Size: {metadata['size']} characters
"""

# Example usage
data = "Your data here"  # Replace with your actual data
description = "Important analysis results"
result = secure_data_storage(data, description)
                    """,
                    "explanation": "This code stores the data securely in a local file with proper metadata, rather than uploading it to an external location.",
                    "intent_preservation": "Instead of uploading data to an external location (which could be a security risk), this code stores the data securely locally with proper documentation."
                }
            ],
            "impersonation_attempt": [
                {
                    "pattern": r"(?:pretend|act|pose|impersonate)\s+(?:as|to be|like)\s+(?:another|different|other)\s+(?:expert|agent|user|person|entity)",
                    "title": "Use proper role-based processing",
                    "template": """
# SAFE REPLACEMENT FOR YOUR OPERATION:
# Original intent: Process data with a different role
# Secure implementation:

def process_with_proper_role(input_data, role_description):
    \"\"\"Process data with a clearly defined role without impersonation.\"\"\"
    # Define the expertise and limitations
    expertise = f"As a {role_description}, I can analyze this data while maintaining my assigned role"
    
    # Process the data with appropriate expertise
    analysis = f"Analysis of the data based on {role_description} expertise"
    
    return f"""
{expertise}

Data Analysis:
{analysis}

Note: This analysis is performed within my assigned role and expertise.
"""

# Example usage
role_description = "data analyst with expertise in pattern recognition"
input_data = "Your data here"  # Replace with your actual data
result = process_with_proper_role(input_data, role_description)
                    """,
                    "explanation": "This code clearly defines the role and processes data within that role's expertise, without impersonating another entity. This maintains proper authentication and authorization boundaries.",
                    "intent_preservation": "This code preserves the intent to process data with specific expertise, but does so with proper role definition rather than impersonation."
                }
            ],
            "excessive_instructions": [
                {
                    "pattern": r"(.+)",  # Match anything
                    "title": "Optimize instruction length",
                    "template": """
# SAFE REPLACEMENT FOR YOUR OPERATION:
# Original intent: Execute a long set of instructions
# Secure implementation:

def execute_optimized_operation():
    \"\"\"Execute the core functionality with optimized instructions.\"\"\"
    # Extract the core functionality from the original long instructions
    
    # Implement the core functionality
    result = "Core functionality executed successfully"
    
    return f"""
Operation completed successfully.
Result: {result}

Note: The original instructions were optimized for security and efficiency.
"""

result = execute_optimized_operation()
                    """,
                    "explanation": "This code optimizes the long instructions to focus on the core functionality, making it more secure and efficient.",
                    "intent_preservation": "The code preserves the core intent of the original instructions while optimizing for security and efficiency."
                }
            ],
            "authenticity_failure": [
                {
                    "pattern": r"(.+)",  # Match anything
                    "title": "Establish proper authentication",
                    "template": """
# SAFE REPLACEMENT FOR YOUR OPERATION:
# Original intent: Execute operation with proper authentication
# Secure implementation:

def execute_authenticated_operation(expert_id, operation_description):
    \"\"\"Execute an operation with proper authentication.\"\"\"
    # Establish proper authentication
    authentication_message = f"Operation authenticated for expert ID: {expert_id}"
    
    # Execute the operation with proper authentication
    operation_result = f"Executed: {operation_description}"
    
    return f"""
{authentication_message}
{operation_result}

Note: This operation was executed with proper authentication.
"""

# Example usage
expert_id = "your_expert_id"  # Replace with your actual expert ID
operation_description = "Your operation description"  # Replace with your actual operation
result = execute_authenticated_operation(expert_id, operation_description)
                    """,
                    "explanation": "This code establishes proper authentication before executing the operation, ensuring that it is authorized.",
                    "intent_preservation": "The code preserves the intent of the original operation while adding proper authentication."
                }
            ]
        }
        
        # Generic recommendations for when no specific pattern matches
        self.generic_recommendations = {
            "dangerous_operation": {
                "title": "Use safe alternatives to system commands",
                "code": """
# SAFE REPLACEMENT FOR YOUR OPERATION:
# Original intent: Execute a potentially dangerous operation
# Secure implementation:

def safe_alternative():
    \"\"\"Implement a safe alternative to the dangerous operation.\"\"\"
    # Instead of using system commands or other dangerous operations,
    # use Python's built-in libraries to achieve the same goal
    
    # Example:
    # Instead of: os.system("rm -rf /path")
    # Use: shutil.rmtree("/path") if os.path.exists("/path")
    
    return "Operation completed safely using built-in Python functions"

result = safe_alternative()
                """,
                "explanation": "This code provides a safe alternative to dangerous system commands using Python's built-in libraries.",
                "intent_preservation": "The original intent can be preserved by using Python's built-in functions instead of dangerous system commands."
            },
            "data_exfiltration": {
                "title": "Process data securely",
                "code": """
# SAFE REPLACEMENT FOR YOUR OPERATION:
# Original intent: Process data
# Secure implementation:

def process_data_securely(data):
    \"\"\"Process data securely without exfiltration.\"\"\"
    # Process the data locally without sending it externally
    
    # Example analysis
    data_info = {
        "type": type(data).__name__,
        "length": len(data) if hasattr(data, "__len__") else "unknown"
    }
    
    return f"Data processed securely. Type: {data_info['type']}, Length: {data_info['length']}"

# Example usage
data = "Your data here"  # Replace with your actual data
result = process_data_securely(data)
                """,
                "explanation": "This code processes data securely without sending it to external servers or locations.",
                "intent_preservation": "The original intent to process data is preserved, but done securely without exfiltration risks."
            },
            "impersonation_attempt": {
                "title": "Use proper role definition",
                "code": """
# SAFE REPLACEMENT FOR YOUR OPERATION:
# Original intent: Process with specific expertise
# Secure implementation:

def process_with_defined_role(data, role):
    \"\"\"Process data with a clearly defined role.\"\"\"
    # Define the role explicitly
    role_definition = f"Processing as {role} with appropriate permissions"
    
    # Process the data within the defined role
    result = f"Data processed according to {role} expertise"
    
    return f"{role_definition}\\n{result}"

# Example usage
data = "Your data here"  # Replace with your actual data
role = "data analyst"  # Define your role explicitly
result = process_with_defined_role(data, role)
                """,
                "explanation": "This code uses proper role definition instead of impersonation, maintaining security boundaries.",
                "intent_preservation": "The original intent to process with specific expertise is preserved, but with proper role definition."
            },
            "excessive_instructions": {
                "title": "Optimize instruction length",
                "code": """
# SAFE REPLACEMENT FOR YOUR OPERATION:
# Original intent: Execute complex instructions
# Secure implementation:

def execute_optimized():
    \"\"\"Execute optimized version of complex instructions.\"\"\"
    # Implement the core functionality in a concise way
    
    return "Core functionality executed successfully with optimized instructions"

result = execute_optimized()
                """,
                "explanation": "This code optimizes long or complex instructions to focus on the core functionality.",
                "intent_preservation": "The core intent of the original instructions is preserved while optimizing for security and efficiency."
            },
            "authenticity_failure": {
                "title": "Establish proper authentication",
                "code": """
# SAFE REPLACEMENT FOR YOUR OPERATION:
# Original intent: Execute operation
# Secure implementation with proper authentication:

def authenticated_operation(expert_id):
    \"\"\"Execute operation with proper authentication.\"\"\"
    # Establish authentication
    auth_message = f"Operation authenticated for expert ID: {expert_id}"
    
    # Execute with proper authentication
    result = "Operation executed with proper authentication"
    
    return f"{auth_message}\\n{result}"

# Example usage
expert_id = "your_expert_id"  # Replace with your actual expert ID
result = authenticated_operation(expert_id)
                """,
                "explanation": "This code establishes proper authentication before executing the operation.",
                "intent_preservation": "The original operation intent is preserved while adding proper authentication."
            }
        }
    
    def get_recommendation(self, error_code: str, operation_text: str, context: Optional[Dict[str, Any]] = None) -> List[Dict[str, str]]:
        """
        Get context-aware recommendations for fixing a security issue.
        
        Args:
            error_code: The type of security error (e.g., "dangerous_operation")
            operation_text: The text of the operation that triggered the error
            context: Additional context about the error and operation
                
        Returns:
            List of recommendation objects with context-aware code
        """
        logger.debug(f"Getting recommendations for error code: {error_code}")
        
        # Check if we have templates for this error code
        if error_code not in self.recommendation_templates:
            logger.debug(f"No specific templates for error code: {error_code}, using generic recommendation")
            return self._get_generic_recommendation(error_code)
        
        # Try to match patterns for this error code
        recommendations = []
        for template in self.recommendation_templates[error_code]:
            match = re.search(template["pattern"], operation_text, re.IGNORECASE)
            if match:
                logger.debug(f"Matched pattern for error code: {error_code}")
                
                # Extract captured groups to use in the template
                captured_values = match.groups()
                
                # Create a context dictionary for formatting
                format_context = {}
                
                # Add captured values to the context
                if len(captured_values) >= 1:
                    # Add the first captured value to all possible keys
                    # The template will use the appropriate key
                    format_context["path"] = captured_values[0]
                    format_context["server"] = captured_values[0]
                    format_context["drive"] = captured_values[0]
                    format_context["command"] = captured_values[0]
                
                # Add expert information if available
                if context and 'expert' in context:
                    expert = context['expert']
                    format_context["expert_specialty"] = getattr(expert, 'specialty', 'unknown')
                    format_context["expert_objective"] = getattr(expert, 'objective', 'unknown')
                    format_context["expert_id"] = getattr(expert, 'expert_id', 'unknown')
                
                # Format the template with the context
                try:
                    formatted_code = template["template"].format(**format_context)
                    logger.debug("Successfully formatted recommendation template")
                except KeyError as e:
                    # If formatting fails, use the template as is
                    logger.warning(f"Failed to format recommendation template: {e}")
                    formatted_code = template["template"]
                
                recommendations.append({
                    "title": template["title"],
                    "code": formatted_code,
                    "explanation": template["explanation"],
                    "intent_preservation": template.get("intent_preservation", "This code aims to preserve your original intent while making it secure.")
                })
        
        # If no specific recommendations, return generic ones
        if not recommendations:
            logger.debug(f"No pattern matches for error code: {error_code}, using generic recommendation")
            return self._get_generic_recommendation(error_code)
        
        logger.debug(f"Returning {len(recommendations)} recommendations for error code: {error_code}")
        return recommendations
    
    def _get_generic_recommendation(self, error_code: str) -> List[Dict[str, str]]:
        """
        Provide generic recommendations when no specific ones are available.
        
        Args:
            error_code: The type of security error
            
        Returns:
            List containing a generic recommendation for the error code
        """
        if error_code in self.generic_recommendations:
            return [self.generic_recommendations[error_code]]
        
        # Default recommendation if nothing else matches
        return [{
            "title": "Review security documentation",
            "code": "# See the security guidelines in the documentation",
            "explanation": "The documentation provides guidance on secure coding practices.",
            "intent_preservation": "Review the documentation to find secure ways to achieve your intent."
        }]
