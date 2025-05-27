"""
Integration module for the hybrid security validation approach.

This module provides functions for integrating the hybrid security validation
approach with the existing TBH Secure Agents framework.
"""

import logging
import re
from typing import Dict, Any, Optional, Tuple, Union

from .security_validator import SecurityValidator

# Get a logger for this module
logger = logging.getLogger(__name__)


def integrate_with_expert(expert_class: type) -> type:
    """
    Integrate the hybrid security validation with the Expert class.

    This function monkey-patches the _is_prompt_secure and _is_output_secure
    methods of the Expert class to use the hybrid security validation approach.

    Args:
        expert_class (type): The Expert class to patch

    Returns:
        type: The patched Expert class
    """
    # Store the original methods
    original_is_prompt_secure = expert_class._is_prompt_secure
    original_is_output_secure = expert_class._is_output_secure

    # Create a security validator
    validator = SecurityValidator(interactive=False)

    # Define the new methods
    def new_is_prompt_secure(self, prompt: str, generate_report: bool = False, open_report: bool = False) -> bool:
        """
        Enhanced security checks on prompts using the hybrid approach.

        Args:
            prompt (str): The prompt to be checked
            generate_report (bool): Whether to generate an HTML report
            open_report (bool): Whether to open the report in a browser

        Returns:
            bool: True if the prompt passes all security checks, False otherwise
        """
        logger.debug(f"Performing hybrid prompt security check for Expert '{self.specialty}', Profile '{self.security_profile}'")

        # For minimal security profile, use extremely permissive validation
        if hasattr(self, 'security_profile') and self.security_profile == "minimal":
            logger.debug(f"Minimal security profile - using permissive validation for prompt of length {len(prompt)}")

            # Only check for the most critical exploits (like system destruction commands)
            critical_patterns = [
                r'rm\s+-rf\s+/',  # System destruction
                r'format\s+c:',   # Windows format
                r'del\s+/s\s+/q', # Windows delete all
            ]

            for pattern in critical_patterns:
                if re.search(pattern, prompt, re.IGNORECASE):
                    logger.warning(f"Minimal security: Blocked critical system destruction pattern")
                    return False

            # Allow everything else for minimal profile
            return True

        # For backward compatibility, use the original method for certain cases
        if not hasattr(self, 'use_hybrid_validation') or not self.use_hybrid_validation:
            return original_is_prompt_secure(self, prompt)

        # Check if report generation is enabled
        should_generate_report = generate_report
        if hasattr(self, 'generate_security_reports'):
            should_generate_report = should_generate_report or self.generate_security_reports

        # Check if report opening is enabled
        should_open_report = open_report
        if hasattr(self, 'open_security_reports'):
            should_open_report = should_open_report or self.open_security_reports

        # Validate the prompt
        is_secure, error_details = validator.validate_prompt(
            prompt,
            security_level=self.security_profile
        )

        # Log the result
        if not is_secure:
            logger.warning(f"⚠️ SECURITY WARNING: Prompt security check FAILED: {error_details.get('error_message', 'Unknown reason')}")
            return False

        logger.debug(f"Prompt security check PASSED for Expert '{self.specialty}'")
        return True

    def new_is_output_secure(self, output: str, generate_report: bool = False, open_report: bool = False) -> bool:
        """
        Enhanced security checks on LLM outputs using the hybrid approach.

        Args:
            output (str): The LLM-generated output to be checked
            generate_report (bool): Whether to generate an HTML report
            open_report (bool): Whether to open the report in a browser

        Returns:
            bool: True if the output passes all security checks, False otherwise
        """
        logger.debug(f"Performing hybrid output security check for Expert '{self.specialty}', Profile '{self.security_profile}'")

        # For backward compatibility, use the original method for certain cases
        if not hasattr(self, 'use_hybrid_validation') or not self.use_hybrid_validation:
            return original_is_output_secure(self, output)

        # Check if report generation is enabled
        should_generate_report = generate_report
        if hasattr(self, 'generate_security_reports'):
            should_generate_report = should_generate_report or self.generate_security_reports

        # Check if report opening is enabled
        should_open_report = open_report
        if hasattr(self, 'open_security_reports'):
            should_open_report = should_open_report or self.open_security_reports

        # Validate the output
        is_secure, error_details = validator.validate_output(
            output,
            security_level=self.security_profile
        )

        # Log the result
        if not is_secure:
            logger.warning(f"⚠️ SECURITY WARNING: Output security check FAILED: {error_details.get('error_message', 'Unknown reason')}")

            # For minimal security profile, log but don't block
            if self.security_profile == "minimal":
                logger.info("Allowing output despite security warning due to minimal security profile")
                return True

            return False

        logger.debug(f"Output security check PASSED for Expert '{self.specialty}'")
        return True

    # Patch the methods
    expert_class._is_prompt_secure = new_is_prompt_secure
    expert_class._is_output_secure = new_is_output_secure

    # Add a flag to enable/disable hybrid validation
    setattr(expert_class, 'use_hybrid_validation', True)

    return expert_class


def integrate_with_squad(squad_class: type) -> type:
    """
    Integrate the hybrid security validation with the Squad class.

    This function monkey-patches the _validate_operation_security method
    of the Squad class to use the hybrid security validation approach.

    Args:
        squad_class (type): The Squad class to patch

    Returns:
        type: The patched Squad class
    """
    # Store the original method
    original_validate_operation_security = squad_class._validate_operation_security

    # Create a security validator
    validator = SecurityValidator(interactive=False)

    # Define the new method
    def new_validate_operation_security(self, operation: Any, index: int,
                                       generate_report: bool = False,
                                       open_report: bool = False) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        Enhanced security validation of an operation using the hybrid approach.

        Args:
            operation (Any): The operation to validate
            index (int): The index of the operation in the task list
            generate_report (bool): Whether to generate an HTML report
            open_report (bool): Whether to open the report in a browser

        Returns:
            Tuple[bool, Optional[Dict[str, Any]]]:
                - Boolean indicating if the operation passes all security checks
                - Dictionary with error details and suggestions if validation fails, None otherwise
        """
        # For backward compatibility, use the original method for certain cases
        if not hasattr(self, 'use_hybrid_validation') or not self.use_hybrid_validation:
            return original_validate_operation_security(self, operation, index)

        # Check if report generation is enabled
        should_generate_report = generate_report
        if hasattr(self, 'generate_security_reports'):
            should_generate_report = should_generate_report or self.generate_security_reports

        # Check if report opening is enabled
        should_open_report = open_report
        if hasattr(self, 'open_security_reports'):
            should_open_report = should_open_report or self.open_security_reports

        # Validate the operation
        is_secure, error_details = validator.validate_operation(
            operation,
            security_level=self.security_profile
        )

        # Return the result
        return is_secure, error_details

    # Patch the method
    squad_class._validate_operation_security = new_validate_operation_security

    # Add a flag to enable/disable hybrid validation
    setattr(squad_class, 'use_hybrid_validation', True)

    return squad_class


def enable_hybrid_validation(expert_class: Optional[type] = None,
                       squad_class: Optional[type] = None,
                       enable_reports: bool = True,
                       auto_open_reports: bool = False) -> None:
    """
    Enable hybrid security validation for the TBH Secure Agents framework.

    This function integrates the hybrid security validation approach with
    the Expert and Squad classes.

    Args:
        expert_class (Optional[type]): The Expert class to patch
        squad_class (Optional[type]): The Squad class to patch
        enable_reports (bool): Whether to enable HTML report generation
        auto_open_reports (bool): Whether to automatically open reports in a browser
    """
    # Import the classes if not provided
    if expert_class is None:
        from tbh_secure_agents.agent import Expert
        expert_class = Expert

    if squad_class is None:
        from tbh_secure_agents.crew import Squad
        squad_class = Squad

    # Integrate with the classes
    integrate_with_expert(expert_class)
    integrate_with_squad(squad_class)

    # Add report generation flags
    setattr(expert_class, 'generate_security_reports', enable_reports)
    setattr(expert_class, 'open_security_reports', auto_open_reports)
    setattr(squad_class, 'generate_security_reports', enable_reports)
    setattr(squad_class, 'open_security_reports', auto_open_reports)

    logger.info(f"Hybrid security validation enabled for the TBH Secure Agents framework (Reports: {enable_reports}, Auto-open: {auto_open_reports})")
