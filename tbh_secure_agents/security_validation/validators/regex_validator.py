"""
Regex-based security validator.

This module implements a regex-based security validator that checks text
against a set of predefined patterns to detect security issues.
"""

import re
import logging
import json
import os
from typing import Dict, Any, Optional, List, Pattern

from .base_validator import SecurityValidator

# Get a logger for this module
logger = logging.getLogger(__name__)


class RegexValidator(SecurityValidator):
    """
    Regex-based security validator.
    
    This validator checks text against a set of predefined patterns to detect
    security issues. It's fast and reliable for known patterns but may miss
    novel threats.
    """
    
    def __init__(self, patterns_file: Optional[str] = None):
        """
        Initialize the regex validator.
        
        Args:
            patterns_file (Optional[str]): Path to a JSON file containing patterns.
                If not provided, default patterns will be used.
        """
        self.patterns = self._load_patterns(patterns_file)
        self.compiled_patterns: Dict[str, Pattern] = {}
        
    def _load_patterns(self, patterns_file: Optional[str] = None) -> Dict[str, List[Dict[str, Any]]]:
        """
        Load patterns from a file or use default patterns.
        
        Args:
            patterns_file (Optional[str]): Path to a JSON file containing patterns
            
        Returns:
            Dict[str, List[Dict[str, Any]]]: Dictionary of patterns by security level
        """
        if patterns_file and os.path.exists(patterns_file):
            try:
                with open(patterns_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading patterns file: {e}")
        
        # Default patterns if file not provided or loading failed
        return {
            "minimal": [
                {
                    "pattern": r"(rm\s+-rf\s+/|format\s+[a-z]:|\bdd\s+if|mkfs|system\s*\(|exec\s*\()",
                    "category": "critical_system_command",
                    "description": "Critical system command that could harm the system",
                    "suggestion": "Use secure file operations instead of system commands"
                }
            ],
            "standard": [
                {
                    "pattern": r"\b(?:system|exec|eval|subprocess)\s*\(",
                    "category": "command_execution",
                    "description": "Command execution function that could be exploited",
                    "suggestion": "Use secure alternatives or sanitize inputs"
                },
                {
                    "pattern": r"\b(?:rm\s+-rf|rmdir\s+/|format\s+[a-z]:)",
                    "category": "file_deletion",
                    "description": "File deletion command that could be dangerous",
                    "suggestion": "Use secure file operations instead"
                },
                {
                    "pattern": r"\b(?:delete|remove)\s+(?:all|every|database)",
                    "category": "data_deletion",
                    "description": "Data deletion command that could be dangerous",
                    "suggestion": "Use more specific operations with proper safeguards"
                },
                {
                    "pattern": r"\b(?:drop\s+table|drop\s+database)",
                    "category": "database_deletion",
                    "description": "Database deletion command that could be dangerous",
                    "suggestion": "Use database migrations or specific operations"
                }
            ],
            "high": [
                {
                    "pattern": r"\b(?:hack|crack|exploit)\b",
                    "category": "hacking_terminology",
                    "description": "Hacking terminology that suggests malicious intent",
                    "suggestion": "Use more specific and legitimate terminology"
                },
                {
                    "pattern": r"\b(?:bypass|circumvent)\s+(?:security|authentication|authorization)",
                    "category": "security_bypass",
                    "description": "Attempt to bypass security measures",
                    "suggestion": "Use proper authentication and authorization methods"
                },
                {
                    "pattern": r"\b(?:ignore|disregard)\s+(?:previous|instructions|guidelines)",
                    "category": "prompt_injection",
                    "description": "Potential prompt injection attempt",
                    "suggestion": "Remove instructions to ignore or disregard guidelines"
                }
            ],
            "maximum": [
                {
                    "pattern": r"\b(?:sudo|su|runas|administrator|root)\b",
                    "category": "privilege_escalation",
                    "description": "Privilege escalation command",
                    "suggestion": "Use proper permission management"
                },
                {
                    "pattern": r"\b(?:ssh|telnet|ftp|sftp)\s+(?:to|into)",
                    "category": "remote_access",
                    "description": "Remote access command",
                    "suggestion": "Use secure API calls instead of remote access"
                },
                {
                    "pattern": r"\b(?:curl|wget|fetch)\s+(?:http|https|ftp)",
                    "category": "network_request",
                    "description": "Network request command",
                    "suggestion": "Use secure API clients instead of command-line tools"
                }
            ]
        }
        
    def _get_compiled_pattern(self, pattern: str) -> Pattern:
        """
        Get or create a compiled regex pattern.
        
        Args:
            pattern (str): The regex pattern to compile
            
        Returns:
            Pattern: The compiled pattern
        """
        if pattern not in self.compiled_patterns:
            self.compiled_patterns[pattern] = re.compile(pattern, re.IGNORECASE)
        return self.compiled_patterns[pattern]
        
    def validate(self, text: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Validate text using regex patterns.
        
        Args:
            text (str): The text to validate
            context (Optional[Dict[str, Any]]): Additional context for validation
                
        Returns:
            Dict[str, Any]: Validation result
        """
        context = context or {}
        security_level = context.get("security_level", "standard")
        
        # Get patterns for this security level and all lower levels
        all_patterns = []
        if security_level == "minimal":
            all_patterns.extend(self.patterns.get("minimal", []))
        elif security_level == "standard":
            all_patterns.extend(self.patterns.get("minimal", []))
            all_patterns.extend(self.patterns.get("standard", []))
        elif security_level == "high":
            all_patterns.extend(self.patterns.get("minimal", []))
            all_patterns.extend(self.patterns.get("standard", []))
            all_patterns.extend(self.patterns.get("high", []))
        elif security_level == "maximum":
            all_patterns.extend(self.patterns.get("minimal", []))
            all_patterns.extend(self.patterns.get("standard", []))
            all_patterns.extend(self.patterns.get("high", []))
            all_patterns.extend(self.patterns.get("maximum", []))
        
        # Check each pattern
        for pattern_info in all_patterns:
            pattern = pattern_info["pattern"]
            compiled_pattern = self._get_compiled_pattern(pattern)
            
            match = compiled_pattern.search(text)
            if match:
                # For minimal security level, only log warnings but don't block
                if security_level == "minimal" and pattern_info.get("category") != "critical_system_command":
                    logger.warning(f"⚠️ SECURITY WARNING: Matched pattern '{pattern}' but allowing due to minimal security level")
                    continue
                
                # Get the matched text and some context
                matched_text = match.group(0)
                start, end = match.span()
                
                # Get some context around the match
                context_start = max(0, start - 20)
                context_end = min(len(text), end + 20)
                highlighted_text = text[context_start:start] + ">>>" + matched_text + "<<<" + text[end:context_end]
                
                return {
                    "is_secure": False,
                    "method": "regex",
                    "reason": pattern_info.get("description", f"Matched pattern: {pattern}"),
                    "matched_pattern": pattern,
                    "matched_text": matched_text,
                    "highlighted_text": highlighted_text,
                    "category": pattern_info.get("category", "unknown"),
                    "fix_suggestion": pattern_info.get("suggestion", "Review and modify the flagged content")
                }
                
        # All patterns passed
        return {
            "is_secure": True,
            "method": "regex"
        }
