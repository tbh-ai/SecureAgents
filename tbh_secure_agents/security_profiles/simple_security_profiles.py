#!/usr/bin/env python3
"""
Simple Security Profiles

This script creates custom security profiles that are more usable than the built-in ones.
"""

import os
import logging
from tbh_secure_agents.security_profiles import register_custom_profile

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create an unrestricted security profile
unrestricted_profile = register_custom_profile(
    name="unrestricted",
    thresholds={
        "injection_score": 1.0,       # Never block injections
        "sensitive_data": 1.0,        # Never block sensitive data
        "relevance_score": 0.0,       # No relevance check
        "reliability_score": 0.0,     # No reliability check
        "consistency_score": 0.0,     # No consistency check
    },
    checks={
        "critical_exploits": False,   # Skip critical exploits check
        "system_commands": False,     # Skip system commands check
        "content_analysis": False,    # Skip content analysis
        "format_validation": False,   # Skip format validation
        "context_validation": False,  # Skip context validation
        "output_validation": False,   # Skip output validation
        "expert_validation": False,   # Skip expert validation
    },
    description="Unrestricted mode with no security checks. Use at your own risk."
)

# Create a minimal security profile
minimal_override = register_custom_profile(
    name="minimal_override",
    thresholds={
        "injection_score": 1.0,       # Never block injections
        "sensitive_data": 1.0,        # Never block sensitive data
        "relevance_score": 0.0,       # No relevance check
        "reliability_score": 0.0,     # No reliability check
        "consistency_score": 0.0,     # No consistency check
    },
    checks={
        "critical_exploits": True,    # Only check for critical exploits
        "system_commands": False,     # Skip system commands check
        "content_analysis": False,    # Skip content analysis
        "format_validation": False,   # Skip format validation
        "context_validation": False,  # Skip context validation
        "output_validation": False,   # Skip output validation
        "expert_validation": False,   # Skip expert validation
    },
    description="Minimal security with only critical exploit checks. Almost all code will run."
)

# Create a standard security profile
standard_override = register_custom_profile(
    name="standard_override",
    thresholds={
        "injection_score": 0.9,       # Only block very obvious injections
        "sensitive_data": 0.9,        # Only block very obvious sensitive data
        "relevance_score": 0.1,       # Very permissive relevance check
        "reliability_score": 0.1,     # Very permissive reliability check
        "consistency_score": 0.1,     # Very permissive consistency check
    },
    checks={
        "critical_exploits": True,    # Check for critical exploits
        "system_commands": True,      # Check for system commands
        "content_analysis": False,    # Skip content analysis
        "format_validation": False,   # Skip format validation
        "context_validation": False,  # Skip context validation
        "output_validation": False,   # Skip output validation
        "expert_validation": False,   # Skip expert validation
    },
    description="Standard security with minimal restrictions. Most code will run."
)

# Print success message
if unrestricted_profile and minimal_override and standard_override:
    logger.info("Successfully created custom security profiles:")
    logger.info("1. 'unrestricted': No security checks at all")
    logger.info("2. 'minimal_override': Only critical exploit checks")
    logger.info("3. 'standard_override': Similar to the old minimal profile")
    logger.info("\nTo use these profiles:")
    logger.info("expert = Expert(security_profile='unrestricted')")
    logger.info("expert = Expert(security_profile='minimal_override')")
    logger.info("expert = Expert(security_profile='standard_override')")
else:
    logger.error("Failed to create some custom security profiles")
