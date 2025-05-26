"""
Main security validator for the TBH Secure Agents framework.

This module provides the main security validator class that integrates with
the existing framework and provides a unified interface for security validation.
Focused purely on security - no visualization bloat, just hardcore protection.
"""

import logging
import os
from typing import Dict, Any, Optional, Tuple

from .validators import HybridValidator
from .validators.production_hybrid_validator import ProductionHybridValidator
from .utils import SecurityUI

# Get a logger for this module
logger = logging.getLogger(__name__)


class SecurityValidator:
    """
    Main security validator for the TBH Secure Agents framework.

    This class provides a unified interface for security validation that
    integrates with the existing framework. It uses the hybrid validator
    under the hood and provides security-focused validation with minimal UI.
    Pure security, maximum performance.
    """

    def __init__(self,
                 api_key: Optional[str] = None,
                 interactive: bool = True,
                 use_production_validator: bool = True):
        """
        Initialize the security validator.

        Args:
            api_key (Optional[str]): API key for the LLM service
            interactive (bool): Whether to use interactive features
            use_production_validator (bool): Whether to use the production-optimized validator
        """
        self.api_key = api_key or os.environ.get("GOOGLE_API_KEY")

        # Use production validator for better accuracy
        if use_production_validator:
            try:
                self.validator = ProductionHybridValidator(api_key=self.api_key)
                logger.info("Using ProductionHybridValidator for enhanced accuracy")
            except Exception as e:
                logger.warning(f"Failed to initialize ProductionHybridValidator: {e}")
                logger.info("Falling back to standard HybridValidator")
                self.validator = HybridValidator(api_key=self.api_key)
        else:
            self.validator = HybridValidator(api_key=self.api_key)
        # Initialize UI (minimal for security focus)
        self.ui = SecurityUI(interactive=interactive)

    def validate_prompt(self, prompt: str, security_level: str = "standard") -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        Validate a prompt for security issues.

        Args:
            prompt (str): The prompt to validate
            security_level (str): The security level to use

        Returns:
            Tuple[bool, Optional[Dict[str, Any]]]: A tuple containing:
                - A boolean indicating whether the prompt is secure
                - A dictionary with error details if validation fails, None otherwise
        """
        # Create validation context
        context = {
            "security_level": security_level,
            "validation_type": "prompt"
        }

        # Show validation progress (minimal UI)
        self.ui.show_validation_progress("Hybrid", security_level)

        # Validate the prompt
        result = self.validator.validate(prompt, context)

        # Show validation result (minimal UI)
        self.ui.show_validation_result(result)

        # Return validation result
        if result["is_secure"]:
            return True, None
        else:
            # Create error details
            error_details = {
                "error_code": result.get("category", "security_violation"),
                "error_message": result.get("reason", "Security validation failed"),
                "suggestions": [result.get("fix_suggestion", "Review and modify the flagged content")],
                "details": result.get("highlighted_text", "")
            }
            return False, error_details

    def validate_output(self, output: str, security_level: str = "standard") -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        Validate an output for security issues.

        Args:
            output (str): The output to validate
            security_level (str): The security level to use

        Returns:
            Tuple[bool, Optional[Dict[str, Any]]]: A tuple containing:
                - A boolean indicating whether the output is secure
                - A dictionary with error details if validation fails, None otherwise
        """
        # Create validation context
        context = {
            "security_level": security_level,
            "validation_type": "output"
        }

        # Show validation progress (minimal UI)
        self.ui.show_validation_progress("Hybrid", security_level)

        # Validate the output
        result = self.validator.validate(output, context)

        # Show validation result (minimal UI)
        self.ui.show_validation_result(result)

        # Return validation result
        if result["is_secure"]:
            return True, None
        else:
            # Create error details
            error_details = {
                "error_code": result.get("category", "security_violation"),
                "error_message": result.get("reason", "Security validation failed"),
                "suggestions": [result.get("fix_suggestion", "Review and modify the flagged content")],
                "details": result.get("highlighted_text", "")
            }
            return False, error_details

    def validate_operation(self, operation: Any, security_level: str = "standard") -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        Validate an operation for security issues.

        Args:
            operation (Any): The operation to validate
            security_level (str): The security level to use

        Returns:
            Tuple[bool, Optional[Dict[str, Any]]]: A tuple containing:
                - A boolean indicating whether the operation is secure
                - A dictionary with error details if validation fails, None otherwise
        """
        # Extract operation instructions
        if hasattr(operation, "instructions"):
            instructions = operation.instructions
        else:
            logger.warning("Operation does not have instructions attribute")
            return True, None

        # Create validation context
        context = {
            "security_level": security_level,
            "validation_type": "operation",
            "operation_type": type(operation).__name__
        }

        # Show validation progress (minimal UI)
        self.ui.show_validation_progress("Hybrid", security_level)

        # Validate the operation instructions
        result = self.validator.validate(instructions, context)

        # Show validation result (minimal UI)
        self.ui.show_validation_result(result)

        # Return validation result
        if result["is_secure"]:
            return True, None
        else:
            # Create error details
            error_details = {
                "error_code": result.get("category", "security_violation"),
                "error_message": result.get("reason", "Security validation failed"),
                "suggestions": [result.get("fix_suggestion", "Review and modify the flagged content")],
                "details": result.get("highlighted_text", "")
            }
            return False, error_details

    def show_security_level_info(self, security_level: str):
        """Show information about a security level."""
        self.ui.show_security_level_info(security_level)

    def clear_cache(self):
        """Clear the validation cache."""
        self.validator.clear_cache()
