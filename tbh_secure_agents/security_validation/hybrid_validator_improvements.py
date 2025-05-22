#!/usr/bin/env python3
"""
Hybrid Validator Improvements

This module provides improvements to the hybrid security validator to make it
more robust against false positives and negatives, with better visualization
and framework-specific recommendations.
"""

import os
import logging
from typing import Dict, Any, Optional, List, Union, Tuple

from .validators.hybrid_validator import HybridValidator
from .recommendation.framework_specific_recommendation import FrameworkSpecificRecommendationGenerator
from .visualization.enhanced_visualizer import EnhancedVisualizer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ImprovedHybridValidator:
    """
    Improved hybrid security validator.

    This class enhances the existing hybrid validator with:
    1. Better handling of false positives/negatives
    2. Framework-specific recommendations
    3. Enhanced visualization
    4. Improved caching
    """

    def __init__(self,
                 api_key: Optional[str] = None,
                 use_parallel: bool = True,
                 enable_reports: bool = True,
                 auto_open_reports: bool = False,
                 reports_dir: Optional[str] = None,
                 recommendation_style: str = "detailed",
                 include_code_examples: bool = True):
        """
        Initialize the improved hybrid validator.

        Args:
            api_key (Optional[str]): API key for LLM services
            use_parallel (bool): Whether to use parallel validation
            enable_reports (bool): Whether to generate HTML reports
            auto_open_reports (bool): Whether to automatically open reports
            reports_dir (Optional[str]): Directory to save reports
            recommendation_style (str): Style of recommendations (detailed, concise, bullet)
            include_code_examples (bool): Whether to include code examples in recommendations
        """
        # Initialize the base hybrid validator
        self.hybrid_validator = HybridValidator(
            api_key=api_key,
            use_parallel=use_parallel
        )

        # Initialize the recommendation generator
        self.recommendation_generator = FrameworkSpecificRecommendationGenerator(
            api_key=api_key,
            recommendation_style=recommendation_style,
            include_code_examples=include_code_examples
        )

        # Initialize the visualizer
        self.enable_reports = enable_reports
        self.auto_open_reports = auto_open_reports
        self.reports_dir = reports_dir or os.path.join(os.getcwd(), "security_reports")

        if self.enable_reports:
            self.visualizer = EnhancedVisualizer(
                output_dir=self.reports_dir,
                auto_save=True,
                use_llm_recommendations=True,
                llm_api_key=api_key
            )

            # Create reports directory if it doesn't exist
            os.makedirs(self.reports_dir, exist_ok=True)

        logger.info(f"Initialized improved hybrid validator (reports={enable_reports})")

    def validate(self, text: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Validate text using the improved hybrid approach.

        Args:
            text (str): The text to validate
            context (Optional[Dict[str, Any]]): Additional context for validation

        Returns:
            Dict[str, Any]: Validation result
        """
        context = context or {}
        security_level = context.get("security_level", "standard")

        # Run the base hybrid validation
        result = self.hybrid_validator.validate(text, context)

        # Apply heuristics to reduce false positives and negatives
        result = self._reduce_false_positives(result, security_level)
        result = self._reduce_false_negatives(result, text, security_level)

        # Add framework-specific recommendations if insecure
        if not result.get("is_secure", True) and "threats" in result:
            recommendation = self.recommendation_generator.generate_recommendation(
                text, result["threats"]
            )
            result["recommendation"] = recommendation

        # Generate HTML report if enabled
        if self.enable_reports:
            report_path = self.visualizer.save_report(
                result, security_level, text, "html"
            )
            result["report_path"] = report_path

            # Open the report in the browser if auto_open_reports is enabled
            if self.auto_open_reports:
                try:
                    import webbrowser
                    webbrowser.open(f"file://{os.path.abspath(report_path)}")
                except Exception as e:
                    logger.error(f"Could not open browser: {e}")

        return result

    def _reduce_false_positives(self, result: Dict[str, Any], security_level: str) -> Dict[str, Any]:
        """
        Reduce false positives by applying additional heuristics.

        Args:
            result (Dict[str, Any]): Validation result
            security_level (str): Security level

        Returns:
            Dict[str, Any]: Updated validation result
        """
        # If already secure, no need to check
        if result.get("is_secure", True):
            return result

        # For minimal security level, be more permissive
        if security_level == "minimal":
            # Filter out low-confidence threats
            if "threats" in result:
                filtered_threats = []
                for threat in result["threats"]:
                    # Only keep high-confidence threats for minimal security
                    if threat.get("score", 0.0) > 0.8:
                        filtered_threats.append(threat)

                # If no threats remain after filtering, mark as secure
                if not filtered_threats:
                    result["is_secure"] = True
                    result["reason"] = "No high-confidence threats detected"
                    result["original_threats"] = result["threats"]
                    result["threats"] = []
                else:
                    result["threats"] = filtered_threats

        # For low security level, be somewhat permissive
        elif security_level == "low":
            # Filter out very low-confidence threats
            if "threats" in result:
                filtered_threats = []
                for threat in result["threats"]:
                    # Only keep moderate-confidence threats for low security
                    if threat.get("score", 0.0) > 0.6:
                        filtered_threats.append(threat)

                # If no threats remain after filtering, mark as secure
                if not filtered_threats:
                    result["is_secure"] = True
                    result["reason"] = "No moderate-confidence threats detected"
                    result["original_threats"] = result["threats"]
                    result["threats"] = []
                else:
                    result["threats"] = filtered_threats

        return result

    def _reduce_false_negatives(self, result: Dict[str, Any], text: str, security_level: str) -> Dict[str, Any]:
        """
        Reduce false negatives by applying additional heuristics.

        Args:
            result (Dict[str, Any]): Validation result
            text (str): The text that was validated
            security_level (str): Security level

        Returns:
            Dict[str, Any]: Updated validation result
        """
        # If already insecure, no need to check
        if not result.get("is_secure", True):
            return result

        # For high and maximum security levels, be more strict
        if security_level in ["high", "maximum"]:
            # Check for potentially dangerous patterns that might have been missed
            dangerous_patterns = [
                # System commands
                r"rm\s+-rf",
                r"sudo\s+",
                r"chmod\s+777",
                # Code execution
                r"eval\s*\(",
                r"exec\s*\(",
                r"system\s*\(",
                r"subprocess\.call",
                r"os\.system",
                # Dynamic imports
                r"__import__",
                r"importlib",
                # File operations
                r"open\s*\([^)]*,\s*['\"]w['\"]",
                r"with\s+open\s*\([^)]*,\s*['\"]w['\"]"
            ]

            import re
            for pattern in dangerous_patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    # Found a potentially dangerous pattern
                    result["is_secure"] = False
                    result["reason"] = f"Potentially dangerous pattern detected: {pattern}"

                    # Add a threat
                    if "threats" not in result:
                        result["threats"] = []

                    result["threats"].append({
                        "category": "potentially_dangerous_pattern",
                        "score": 0.7,
                        "description": f"Potentially dangerous pattern detected: {pattern}"
                    })

                    break

        return result

# Global instance of the improved hybrid validator
_improved_hybrid_validator = None

def enable_improved_hybrid_validation(
    api_key: Optional[str] = None,
    use_parallel: bool = True,
    enable_reports: bool = True,
    auto_open_reports: bool = False,
    reports_dir: Optional[str] = None,
    recommendation_style: str = "detailed",
    include_code_examples: bool = True
) -> ImprovedHybridValidator:
    """
    Enable the improved hybrid validation system.

    This function initializes the improved hybrid validator and sets it as the
    global validator for the framework.

    Args:
        api_key (Optional[str]): API key for LLM services
        use_parallel (bool): Whether to use parallel validation
        enable_reports (bool): Whether to generate HTML reports
        auto_open_reports (bool): Whether to automatically open reports
        reports_dir (Optional[str]): Directory to save reports
        recommendation_style (str): Style of recommendations (detailed, concise, bullet)
        include_code_examples (bool): Whether to include code examples in recommendations

    Returns:
        ImprovedHybridValidator: The initialized improved hybrid validator
    """
    global _improved_hybrid_validator

    # Initialize the improved hybrid validator
    _improved_hybrid_validator = ImprovedHybridValidator(
        api_key=api_key,
        use_parallel=use_parallel,
        enable_reports=enable_reports,
        auto_open_reports=auto_open_reports,
        reports_dir=reports_dir,
        recommendation_style=recommendation_style,
        include_code_examples=include_code_examples
    )

    # Import the security validation module to patch it
    from tbh_secure_agents.security_validation import security_validator

    # Patch the validate function to use the improved hybrid validator
    def improved_validate(text: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Improved validate function that uses the improved hybrid validator.

        Args:
            text (str): The text to validate
            context (Optional[Dict[str, Any]]): Additional context for validation

        Returns:
            Dict[str, Any]: Validation result
        """
        return _improved_hybrid_validator.validate(text, context)

    # Replace the validate function
    security_validator.validate = improved_validate

    logger.info("Enabled improved hybrid validation")

    return _improved_hybrid_validator
