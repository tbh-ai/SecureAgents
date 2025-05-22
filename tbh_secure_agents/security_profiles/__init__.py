"""
Security profiles for the TBH Secure Agents framework.

This package contains security profiles that define the security rules and
validation criteria for different security levels.
"""

from .simple_security_profiles import (
    get_security_profile,
    get_minimal_security_profile,
    get_low_security_profile,
    get_standard_security_profile,
    get_high_security_profile,
    get_maximum_security_profile,
    SECURITY_LEVELS
)

__all__ = [
    'get_security_profile',
    'get_minimal_security_profile',
    'get_low_security_profile',
    'get_standard_security_profile',
    'get_high_security_profile',
    'get_maximum_security_profile',
    'SECURITY_LEVELS'
]
