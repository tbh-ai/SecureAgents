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

        # Enhanced patterns for production-level security
        return {
            "minimal": [
                {
                    "pattern": r"(rm\s+-rf\s+/|format\s+[a-z]:|\bdd\s+if|mkfs)",
                    "category": "critical_system_command",
                    "description": "Critical destructive system command",
                    "suggestion": "Use secure file operations instead of destructive commands"
                },
                {
                    "pattern": r"system\s*\(\s*['\"].*rm\s+-rf\s+/",
                    "category": "critical_system_command",
                    "description": "Critical destructive system call",
                    "suggestion": "Avoid destructive system commands"
                }
            ],
            "standard": [
                {
                    "pattern": r"system\s*\(\s*['\"].*(?:rm\s+-rf|format|dd\s+if|mkfs)",
                    "category": "command_execution",
                    "description": "Dangerous destructive system command",
                    "suggestion": "Use safer alternatives for file operations"
                },
                {
                    "pattern": r"(?i)\b(?:ignore|disregard|forget|override|bypass)\s+(?:all\s+)?(?:previous\s+)?(?:instructions?|rules?|guidelines?|security)",
                    "category": "prompt_injection",
                    "description": "Potential prompt injection attempt",
                    "suggestion": "Remove instruction override attempts"
                },
                {
                    "pattern": r"(?i)(?:system\s*:|SYSTEM\s*:|admin\s*:|root\s*:)",
                    "category": "prompt_injection",
                    "description": "System role impersonation attempt",
                    "suggestion": "Remove system role impersonation"
                },
                {
                    "pattern": r"(?i)(?:dan\s+mode|maintenance\s+mode)",
                    "category": "prompt_injection",
                    "description": "Mode manipulation attempt",
                    "suggestion": "Remove mode manipulation attempts"
                },
                {
                    "pattern": r"(?i)['\"]?\s*(?:OR|AND)\s+['\"]?1['\"]?\s*=\s*['\"]?1['\"]?",
                    "category": "sql_injection",
                    "description": "Classic SQL injection bypass pattern",
                    "suggestion": "Use parameterized queries"
                },
                {
                    "pattern": r"(?i)UNION\s+(?:ALL\s+)?SELECT",
                    "category": "sql_injection",
                    "description": "SQL UNION injection attempt",
                    "suggestion": "Use parameterized queries"
                },
                {
                    "pattern": r"(?i)WHERE\s+['\"]?1['\"]?\s*=\s*['\"]?1['\"]?",
                    "category": "sql_injection",
                    "description": "SQL WHERE 1=1 bypass pattern",
                    "suggestion": "Use parameterized queries"
                },
                {
                    "pattern": r"(?i)(?:/etc/passwd|/etc/shadow)",
                    "category": "data_exfiltration",
                    "description": "Critical system file access attempt",
                    "suggestion": "Avoid accessing system configuration files"
                }
            ],
            "high": [
                {
                    "pattern": r"(?:import\s+os|from\s+os\s+import|__import__\s*\(\s*['\"]os['\"])",
                    "category": "dangerous_import",
                    "description": "Import of potentially dangerous OS module",
                    "suggestion": "Use specific functions instead of importing entire os module"
                },
                {
                    "pattern": r"\b(?:base64|encode|decode|encrypt|decrypt)\b.*(?:password|key|token|secret)",
                    "category": "credential_exposure",
                    "description": "Potential credential encoding/decoding",
                    "suggestion": "Avoid exposing credentials in operations"
                },
                {
                    "pattern": r"(?i)(?:SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER)\s+.*(?:OR\s+['\"]?1['\"]?\s*=\s*['\"]?1|UNION\s+SELECT)",
                    "category": "sql_injection",
                    "description": "Potential SQL injection pattern",
                    "suggestion": "Use parameterized queries"
                },
                {
                    "pattern": r"(?i)['\"]?\s*(?:OR|AND)\s+['\"]?1['\"]?\s*=\s*['\"]?1['\"]?",
                    "category": "sql_injection",
                    "description": "Classic SQL injection bypass pattern",
                    "suggestion": "Use parameterized queries and input validation"
                },
                {
                    "pattern": r"(?i)UNION\s+(?:ALL\s+)?SELECT",
                    "category": "sql_injection",
                    "description": "SQL UNION injection attempt",
                    "suggestion": "Use parameterized queries"
                },
                {
                    "pattern": r"(?i)(?:WAITFOR\s+DELAY|BENCHMARK\s*\(|SLEEP\s*\()",
                    "category": "sql_injection",
                    "description": "Time-based SQL injection attempt",
                    "suggestion": "Use parameterized queries and timeout controls"
                },
                {
                    "pattern": r"(?i)(?:DROP\s+TABLE|TRUNCATE\s+TABLE|DELETE\s+FROM)",
                    "category": "sql_injection",
                    "description": "Destructive SQL injection attempt",
                    "suggestion": "Use parameterized queries and proper permissions"
                },
                {
                    "pattern": r"\b(?:curl|wget|fetch)\s+.*\|\s*(?:bash|sh|python|perl)",
                    "category": "remote_execution",
                    "description": "Remote script execution pattern",
                    "suggestion": "Download and verify scripts before execution"
                }
            ],
            "maximum": [
                {
                    "pattern": r"(?i)(?:SELECT\s+\*\s+FROM|COPY\s+TO|INTO\s+OUTFILE)",
                    "category": "data_exfiltration",
                    "description": "Potential data exfiltration attempt",
                    "suggestion": "Use specific column selection and secure data handling"
                },
                {
                    "pattern": r"(?i)(?:/etc/passwd|/etc/shadow|/etc/hosts|/etc/group)",
                    "category": "data_exfiltration",
                    "description": "System file access attempt",
                    "suggestion": "Avoid accessing system configuration files"
                },
                {
                    "pattern": r"(?i)(?:dump\s+(?:database|table)|backup\s+(?:database|table))",
                    "category": "data_exfiltration",
                    "description": "Database dump attempt",
                    "suggestion": "Use authorized backup procedures"
                },
                {
                    "pattern": r"(?i)(?:curl.*\|\s*(?:bash|sh)|wget.*\|\s*(?:bash|sh))",
                    "category": "data_exfiltration",
                    "description": "Remote data transmission attempt",
                    "suggestion": "Use secure data transfer methods"
                },
                {
                    "pattern": r"(?:globals|locals|vars|dir)\s*\(\s*\)",
                    "category": "introspection",
                    "description": "Code introspection that could expose internals",
                    "suggestion": "Avoid introspection functions in user input"
                },
                {
                    "pattern": r"(?:__.*__|getattr|setattr|hasattr|delattr)",
                    "category": "attribute_manipulation",
                    "description": "Attribute manipulation that could bypass security",
                    "suggestion": "Restrict attribute access operations"
                },
                {
                    "pattern": r"\b(?:lambda|map|filter|reduce)\s*\(.*(?:exec|eval|import|open)",
                    "category": "functional_injection",
                    "description": "Functional programming injection attempt",
                    "suggestion": "Avoid combining functional programming with dangerous operations"
                },
                {
                    "pattern": r"(?:for\s+.*\s+in\s+)?(?:range|enumerate|zip)\s*\(.*(?:exec|eval|system)",
                    "category": "loop_injection",
                    "description": "Loop-based code injection attempt",
                    "suggestion": "Sanitize loop contents"
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
