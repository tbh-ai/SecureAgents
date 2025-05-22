"""
Security profiles for TBH Secure Agents.

This module defines the security profiles and their behaviors in the framework.
It includes caching mechanisms for improved performance.
"""

import logging
import re
import time
import hashlib
import functools
from enum import Enum
from typing import Dict, Any, List, Optional, Callable, Tuple, Pattern, Set

logger = logging.getLogger(__name__)

# Cache for compiled regex patterns
_REGEX_CACHE: Dict[str, Pattern] = {}

# Cache for security validation results
_VALIDATION_CACHE: Dict[str, Tuple[bool, float]] = {}

# Cache expiration time in seconds
CACHE_EXPIRATION = 300  # 5 minutes

# Registry for custom security profiles
_CUSTOM_PROFILES: Dict[str, Dict[str, Any]] = {}

class SecurityProfile(Enum):
    """Security profile levels for the framework."""
    MINIMAL = "minimal"
    LOW = "low"
    STANDARD = "standard"
    HIGH = "high"
    MAXIMUM = "maximum"
    CUSTOM = "custom"  # Special value for custom profiles

    @classmethod
    def from_string(cls, profile_str: str) -> 'SecurityProfile':
        """
        Convert a string to a SecurityProfile enum.

        If the string matches a standard profile, returns that profile.
        If the string matches a registered custom profile, returns CUSTOM.
        Otherwise, defaults to STANDARD.

        Args:
            profile_str: The profile string to convert

        Returns:
            SecurityProfile enum value
        """
        # Check if it's a standard profile
        try:
            return cls(profile_str.lower())
        except ValueError:
            # Check if it's a registered custom profile
            if profile_str.lower() in _CUSTOM_PROFILES:
                return cls.CUSTOM

            # Default to standard
            logger.warning(f"Unknown security profile '{profile_str}', defaulting to STANDARD")
            return cls.STANDARD

    @classmethod
    def get_profile_description(cls, profile: 'SecurityProfile') -> str:
        """
        Get a description of the security profile.

        Args:
            profile: The security profile to describe

        Returns:
            Description string
        """
        descriptions = {
            cls.MINIMAL: "Development-friendly security profile optimized for rapid iteration. Prioritizes code execution with light security awareness for critical exploits only.",
            cls.LOW: "Streamlined security profile with basic protection against system commands and critical vulnerabilities while maintaining high code compatibility.",
            cls.STANDARD: "Balanced security profile suitable for most use cases. Provides moderate protection with reasonable workflow compatibility.",
            cls.HIGH: "Enhanced security profile with comprehensive protection mechanisms. Recommended for handling sensitive operations with strong security requirements.",
            cls.MAXIMUM: "Enterprise-grade security profile with advanced protection layers. Ideal for production environments with strict security requirements and regulatory compliance needs.",
            cls.CUSTOM: "Custom security profile with user-defined settings tailored to specific requirements."
        }
        return descriptions.get(profile, "Unknown security profile")

def register_custom_profile(
    name: str,
    thresholds: Dict[str, float],
    checks: Dict[str, bool],
    description: Optional[str] = None
) -> bool:
    """
    Register a custom security profile with specified thresholds and checks.

    Args:
        name: The name of the custom profile (case-insensitive)
        thresholds: Dictionary of threshold values for different security checks
        checks: Dictionary of boolean flags indicating which checks to perform
        description: Optional description of the profile

    Returns:
        True if registration was successful, False otherwise
    """
    # Convert name to lowercase for case-insensitive comparison
    profile_name = name.lower()

    # Check if name conflicts with standard profiles
    if profile_name in [p.value for p in SecurityProfile if p != SecurityProfile.CUSTOM]:
        logger.error(f"Cannot register custom profile '{name}': Name conflicts with standard profile")
        return False

    # Validate thresholds
    required_thresholds = [
        "injection_score", "sensitive_data", "relevance_score",
        "reliability_score", "consistency_score"
    ]

    for threshold in required_thresholds:
        if threshold not in thresholds:
            logger.error(f"Cannot register custom profile '{name}': Missing required threshold '{threshold}'")
            return False

        if not isinstance(thresholds[threshold], (int, float)):
            logger.error(f"Cannot register custom profile '{name}': Threshold '{threshold}' must be a number")
            return False

    # Validate checks
    required_checks = [
        "critical_exploits", "system_commands", "content_analysis",
        "format_validation", "context_validation", "output_validation",
        "expert_validation"
    ]

    for check in required_checks:
        if check not in checks:
            logger.error(f"Cannot register custom profile '{name}': Missing required check '{check}'")
            return False

        if not isinstance(checks[check], bool):
            logger.error(f"Cannot register custom profile '{name}': Check '{check}' must be a boolean")
            return False

    # Register the custom profile
    _CUSTOM_PROFILES[profile_name] = {
        "name": name,
        "thresholds": thresholds,
        "checks": checks,
        "description": description or f"Custom security profile: {name}"
    }

    logger.info(f"Registered custom security profile: {name}")
    return True

def get_custom_profile(name: str) -> Optional[Dict[str, Any]]:
    """
    Get a registered custom security profile by name.

    Args:
        name: The name of the custom profile (case-insensitive)

    Returns:
        Dictionary containing the custom profile configuration, or None if not found
    """
    return _CUSTOM_PROFILES.get(name.lower())

def list_custom_profiles() -> List[str]:
    """
    Get a list of all registered custom profile names.

    Returns:
        List of custom profile names
    """
    return list(_CUSTOM_PROFILES.keys())

def get_security_thresholds(profile: SecurityProfile, profile_name: Optional[str] = None) -> Dict[str, float]:
    """
    Get security thresholds based on the security profile.

    Args:
        profile: The security profile to use
        profile_name: The name of the custom profile (required if profile is CUSTOM)

    Returns:
        Dictionary of threshold values for different security checks
    """
    # Define thresholds for different security profiles
    thresholds = {
        SecurityProfile.MINIMAL: {
            "injection_score": 0.98,      # Only block the most extreme injections
            "sensitive_data": 0.98,       # Only block the most extreme sensitive data
            "relevance_score": 0.02,      # Extremely permissive relevance check
            "reliability_score": 0.02,    # Extremely permissive reliability check
            "consistency_score": 0.02,    # Extremely permissive consistency check
        },
        SecurityProfile.LOW: {
            "injection_score": 0.85,      # Block obvious injections
            "sensitive_data": 0.85,       # Block obvious sensitive data
            "relevance_score": 0.15,      # Permissive relevance check
            "reliability_score": 0.15,    # Permissive reliability check
            "consistency_score": 0.15,    # Permissive consistency check
        },
        SecurityProfile.STANDARD: {
            "injection_score": 0.75,      # Block moderate injections
            "sensitive_data": 0.75,       # Block moderate sensitive data
            "relevance_score": 0.25,      # Moderate relevance check
            "reliability_score": 0.25,    # Moderate reliability check
            "consistency_score": 0.25,    # Moderate consistency check
        },
        SecurityProfile.HIGH: {
            "injection_score": 0.4,       # Strict injection detection
            "sensitive_data": 0.3,        # Strict sensitive data detection
            "relevance_score": 0.6,       # Strict relevance check
            "reliability_score": 0.7,     # Strict reliability check
            "consistency_score": 0.7,     # Strict consistency check
        },
        SecurityProfile.MAXIMUM: {
            "injection_score": 0.2,       # Very strict injection detection
            "sensitive_data": 0.1,        # Very strict sensitive data detection
            "relevance_score": 0.8,       # Very strict relevance check
            "reliability_score": 0.9,     # Very strict reliability check
            "consistency_score": 0.9,     # Very strict consistency check
        }
    }

    # Handle custom profiles
    if profile == SecurityProfile.CUSTOM and profile_name:
        custom_profile = get_custom_profile(profile_name)
        if custom_profile:
            return custom_profile["thresholds"]
        else:
            logger.warning(f"Custom profile '{profile_name}' not found, using STANDARD thresholds")
            return thresholds[SecurityProfile.STANDARD]

    return thresholds.get(profile, thresholds[SecurityProfile.STANDARD])

def get_security_checks(profile: SecurityProfile, profile_name: Optional[str] = None) -> Dict[str, bool]:
    """
    Get which security checks to perform based on the security profile.

    Args:
        profile: The security profile to use
        profile_name: The name of the custom profile (required if profile is CUSTOM)

    Returns:
        Dictionary of boolean flags indicating which checks to perform
    """
    # Define which checks to perform for different security profiles
    checks = {
        SecurityProfile.MINIMAL: {
            "critical_exploits": True,    # Check for critical exploits
            "system_commands": False,     # Skip system commands check
            "content_analysis": False,    # Skip content analysis
            "format_validation": False,   # Skip format validation
            "context_validation": False,  # Skip context validation
            "output_validation": False,   # Skip output validation
            "expert_validation": False,   # Skip expert validation
        },
        SecurityProfile.LOW: {
            "critical_exploits": True,    # Check for critical exploits
            "system_commands": True,      # Check for system commands
            "content_analysis": False,    # Skip content analysis
            "format_validation": False,   # Skip format validation
            "context_validation": False,  # Skip context validation
            "output_validation": False,   # Skip output validation
            "expert_validation": True,    # Perform expert validation
        },
        SecurityProfile.STANDARD: {
            "critical_exploits": True,    # Check for critical exploits
            "system_commands": True,      # Check for system commands
            "content_analysis": True,     # Perform content analysis
            "format_validation": True,    # Perform format validation
            "context_validation": False,  # Skip context validation
            "output_validation": True,    # Perform output validation
            "expert_validation": True,    # Perform expert validation
        },
        SecurityProfile.HIGH: {
            "critical_exploits": True,    # Always check for critical exploits
            "system_commands": True,      # Always check for system commands
            "content_analysis": True,     # Perform content analysis
            "format_validation": True,    # Perform format validation
            "context_validation": True,   # Perform context validation
            "output_validation": True,    # Perform output validation
            "expert_validation": True,    # Perform expert validation
        },
        SecurityProfile.MAXIMUM: {
            "critical_exploits": True,    # Always check for critical exploits
            "system_commands": True,      # Always check for system commands
            "content_analysis": True,     # Perform content analysis
            "format_validation": True,    # Perform format validation
            "context_validation": True,   # Perform context validation
            "output_validation": True,    # Perform output validation
            "expert_validation": True,    # Perform expert validation
        }
    }

    # Handle custom profiles
    if profile == SecurityProfile.CUSTOM and profile_name:
        custom_profile = get_custom_profile(profile_name)
        if custom_profile:
            return custom_profile["checks"]
        else:
            logger.warning(f"Custom profile '{profile_name}' not found, using STANDARD checks")
            return checks[SecurityProfile.STANDARD]

    return checks.get(profile, checks[SecurityProfile.STANDARD])

def get_security_recommendations(issues: List[str]) -> List[str]:
    """
    Get recommendations for security issues.

    Args:
        issues: List of security issue identifiers

    Returns:
        List of recommendations for addressing the issues
    """
    recommendations = {
        "injection_detected": "Review the operation instructions for potential prompt injection patterns.",
        "sensitive_data": "Check for personally identifiable information or sensitive data in the content.",
        "low_relevance": "Ensure the operation instructions are clear and specific to improve relevance.",
        "low_reliability": "Add more context or clarify instructions to improve reliability.",
        "low_consistency": "Review for contradictory instructions or context that might cause inconsistency.",
        "format_invalid": "Ensure the output format matches the expected format (JSON, CSV, etc.).",
        "context_mismatch": "Verify that the context is appropriate for the operation.",
        "expert_mismatch": "Assign an expert with a specialty that better matches the operation.",
        "system_command": "Remove any instructions that might be interpreted as system commands.",
        "critical_exploit": "Remove patterns that could be exploited for unauthorized actions."
    }

    return [recommendations.get(issue, f"Address the '{issue}' security concern.") for issue in issues]

def get_cached_regex(pattern: str) -> Pattern:
    """
    Get a compiled regex pattern from cache or compile it if not cached.

    Args:
        pattern: The regex pattern string

    Returns:
        Compiled regex pattern
    """
    if pattern not in _REGEX_CACHE:
        _REGEX_CACHE[pattern] = re.compile(pattern, re.IGNORECASE)
    return _REGEX_CACHE[pattern]

def cache_security_validation(func: Callable) -> Callable:
    """
    Decorator to cache security validation results.

    Args:
        func: The function to decorate

    Returns:
        Decorated function with caching
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Create a cache key from the function name and arguments
        key_parts = [func.__name__]

        # Add string representation of args and kwargs
        for arg in args:
            if isinstance(arg, str) and len(arg) > 100:
                # For long strings, use a hash to avoid huge cache keys
                key_parts.append(hashlib.md5(arg.encode()).hexdigest())
            else:
                key_parts.append(str(arg))

        for k, v in sorted(kwargs.items()):
            if isinstance(v, str) and len(v) > 100:
                key_parts.append(f"{k}:{hashlib.md5(v.encode()).hexdigest()}")
            else:
                key_parts.append(f"{k}:{v}")

        cache_key = ":".join(key_parts)

        # Check if result is in cache and not expired
        if cache_key in _VALIDATION_CACHE:
            result, timestamp = _VALIDATION_CACHE[cache_key]
            if time.time() - timestamp < CACHE_EXPIRATION:
                return result

        # Call the original function
        result = func(*args, **kwargs)

        # Cache the result with current timestamp
        _VALIDATION_CACHE[cache_key] = (result, time.time())

        return result

    return wrapper

def clear_caches() -> None:
    """Clear all caches to free memory."""
    _REGEX_CACHE.clear()
    _VALIDATION_CACHE.clear()
    logger.debug("Security validation caches cleared")

def log_security_profile_info(profile: SecurityProfile, profile_name: Optional[str] = None) -> None:
    """
    Log information about the security profile being used.

    Args:
        profile: The security profile to log information about
        profile_name: The name of the custom profile (required if profile is CUSTOM)
    """
    description = SecurityProfile.get_profile_description(profile)

    if profile == SecurityProfile.MINIMAL:
        logger.info(f"MINIMAL SECURITY MODE: {description}")
    elif profile == SecurityProfile.LOW:
        logger.info(f"LOW SECURITY MODE: {description}")
    elif profile == SecurityProfile.STANDARD:
        logger.info(f"STANDARD SECURITY MODE: {description}")
    elif profile == SecurityProfile.HIGH:
        logger.info(f"HIGH SECURITY MODE: {description}")
    elif profile == SecurityProfile.MAXIMUM:
        logger.info(f"MAXIMUM SECURITY MODE: {description}")
    elif profile == SecurityProfile.CUSTOM and profile_name:
        custom_profile = get_custom_profile(profile_name)
        if custom_profile:
            custom_description = custom_profile.get("description", f"Custom security profile: {profile_name}")
            logger.info(f"CUSTOM SECURITY MODE '{profile_name}': {custom_description}")
        else:
            logger.warning(f"⚠️ UNKNOWN CUSTOM PROFILE '{profile_name}': Using STANDARD security settings")
