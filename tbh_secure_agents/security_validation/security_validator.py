"""
Main security validator for the TBH Secure Agents framework.

This module provides the main security validator class that integrates with
the existing framework and provides a unified interface for security validation.
It also includes HTML report generation and LLM-based recommendations.
"""

import logging
import os
from typing import Dict, Any, Optional, List, Union, Tuple, Callable

from .validators import HybridValidator
from .utils import SecurityUI
from .report_generator import SecurityReportGenerator
from .recommendation_generator import LLMRecommendationGenerator, generate_basic_recommendation

# Get a logger for this module
logger = logging.getLogger(__name__)


class SecurityValidator:
    """
    Main security validator for the TBH Secure Agents framework.

    This class provides a unified interface for security validation that
    integrates with the existing framework. It uses the hybrid validator
    under the hood and provides UX-optimized feedback, HTML reports, and
    LLM-based recommendations.
    """

    def __init__(self,
                 api_key: Optional[str] = None,
                 interactive: bool = True,
                 enable_reports: bool = True,
                 reports_dir: str = "security_reports",
                 enable_recommendations: bool = True):
        """
        Initialize the security validator.

        Args:
            api_key (Optional[str]): API key for the LLM service
            interactive (bool): Whether to use interactive features
            enable_reports (bool): Whether to enable HTML report generation
            reports_dir (str): Directory to save reports
            enable_recommendations (bool): Whether to enable LLM recommendations
        """
        self.api_key = api_key or os.environ.get("GOOGLE_API_KEY")
        self.validator = HybridValidator(api_key=self.api_key)
        self.ui = SecurityUI(interactive=interactive)

        # HTML report generation
        self.enable_reports = enable_reports
        if self.enable_reports:
            self.report_generator = SecurityReportGenerator(output_dir=reports_dir)
        else:
            self.report_generator = None

        # LLM recommendation generation
        self.enable_recommendations = enable_recommendations
        if self.enable_recommendations:
            self.recommendation_generator = LLMRecommendationGenerator(api_key=self.api_key)
        else:
            self.recommendation_generator = None

    def validate_prompt(self, prompt: str, security_level: str = "standard",
                      generate_report: bool = False, open_report: bool = False) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        Validate a prompt for security issues.

        Args:
            prompt (str): The prompt to validate
            security_level (str): The security level to use
            generate_report (bool): Whether to generate an HTML report
            open_report (bool): Whether to open the report in a browser

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

        # Show validation progress
        self.ui.show_validation_progress("Hybrid", security_level)

        # Validate the prompt
        result = self.validator.validate(prompt, context)

        # Show validation result
        self.ui.show_validation_result(result)

        # Generate recommendation if enabled and needed
        recommendation = None
        if not result["is_secure"] and self.enable_recommendations:
            threats = result.get("threats", [])
            if threats:
                try:
                    if self.recommendation_generator:
                        recommendation = self.recommendation_generator.generate_recommendation(
                            prompt, threats
                        )
                    else:
                        recommendation = generate_basic_recommendation(prompt, threats)
                except Exception as e:
                    logger.error(f"Error generating recommendation: {e}")
                    recommendation = None

        # Generate HTML report if requested
        report_path = None
        if generate_report and self.enable_reports and self.report_generator:
            try:
                report_path = self.report_generator.generate_report(
                    input_text=prompt,
                    validation_result=result,
                    recommendation=recommendation,
                    open_browser=open_report
                )
                logger.info(f"Generated security validation report: {report_path}")
            except Exception as e:
                logger.error(f"Error generating report: {e}")

        # Return validation result
        if result["is_secure"]:
            return True, None
        else:
            # Create error details
            error_details = {
                "error_code": result.get("category", "security_violation"),
                "error_message": result.get("reason", "Security validation failed"),
                "suggestions": [result.get("fix_suggestion", "Review and modify the flagged content")],
                "details": result.get("highlighted_text", ""),
                "recommendation": recommendation,
                "report_path": report_path
            }

            return False, error_details

    def validate_output(self, output: str, security_level: str = "standard",
                       generate_report: bool = False, open_report: bool = False) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        Validate an output for security issues.

        Args:
            output (str): The output to validate
            security_level (str): The security level to use
            generate_report (bool): Whether to generate an HTML report
            open_report (bool): Whether to open the report in a browser

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

        # Show validation progress
        self.ui.show_validation_progress("Hybrid", security_level)

        # Validate the output
        result = self.validator.validate(output, context)

        # Show validation result
        self.ui.show_validation_result(result)

        # Generate recommendation if enabled and needed
        recommendation = None
        if not result["is_secure"] and self.enable_recommendations:
            threats = result.get("threats", [])
            if threats:
                try:
                    if self.recommendation_generator:
                        recommendation = self.recommendation_generator.generate_recommendation(
                            output, threats
                        )
                    else:
                        recommendation = generate_basic_recommendation(output, threats)
                except Exception as e:
                    logger.error(f"Error generating recommendation: {e}")
                    recommendation = None

        # Generate HTML report if requested
        report_path = None
        if generate_report and self.enable_reports and self.report_generator:
            try:
                report_path = self.report_generator.generate_report(
                    input_text=output,
                    validation_result=result,
                    recommendation=recommendation,
                    open_browser=open_report
                )
                logger.info(f"Generated security validation report: {report_path}")
            except Exception as e:
                logger.error(f"Error generating report: {e}")

        # Return validation result
        if result["is_secure"]:
            return True, None
        else:
            # Create error details
            error_details = {
                "error_code": result.get("category", "security_violation"),
                "error_message": result.get("reason", "Security validation failed"),
                "suggestions": [result.get("fix_suggestion", "Review and modify the flagged content")],
                "details": result.get("highlighted_text", ""),
                "recommendation": recommendation,
                "report_path": report_path
            }

            return False, error_details

    def validate_operation(self, operation: Any, security_level: str = "standard",
                         generate_report: bool = False, open_report: bool = False) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        Validate an operation for security issues.

        Args:
            operation (Any): The operation to validate
            security_level (str): The security level to use
            generate_report (bool): Whether to generate an HTML report
            open_report (bool): Whether to open the report in a browser

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

        # Show validation progress
        self.ui.show_validation_progress("Hybrid", security_level)

        # Validate the operation instructions
        result = self.validator.validate(instructions, context)

        # Show validation result
        self.ui.show_validation_result(result)

        # Generate recommendation if enabled and needed
        recommendation = None
        if not result["is_secure"] and self.enable_recommendations:
            threats = result.get("threats", [])
            if threats:
                try:
                    if self.recommendation_generator:
                        recommendation = self.recommendation_generator.generate_recommendation(
                            instructions, threats
                        )
                    else:
                        recommendation = generate_basic_recommendation(instructions, threats)
                except Exception as e:
                    logger.error(f"Error generating recommendation: {e}")
                    recommendation = None

        # Generate HTML report if requested
        report_path = None
        if generate_report and self.enable_reports and self.report_generator:
            try:
                report_path = self.report_generator.generate_report(
                    input_text=instructions,
                    validation_result=result,
                    recommendation=recommendation,
                    open_browser=open_report
                )
                logger.info(f"Generated security validation report: {report_path}")
            except Exception as e:
                logger.error(f"Error generating report: {e}")

        # Return validation result
        if result["is_secure"]:
            return True, None
        else:
            # Create error details
            error_details = {
                "error_code": result.get("category", "security_violation"),
                "error_message": result.get("reason", "Security validation failed"),
                "suggestions": [result.get("fix_suggestion", "Review and modify the flagged content")],
                "details": result.get("highlighted_text", ""),
                "recommendation": recommendation,
                "report_path": report_path
            }

            return False, error_details

    def show_security_level_info(self, security_level: str):
        """
        Show information about a security level.

        Args:
            security_level (str): The security level
        """
        self.ui.show_security_level_info(security_level)

    def clear_cache(self):
        """Clear the validation cache."""
        self.validator.clear_cache()

    def generate_report(self, input_text: str, validation_result: Dict[str, Any],
                       recommendation: Optional[str] = None, open_browser: bool = False) -> Optional[str]:
        """
        Generate a security validation report.

        Args:
            input_text (str): The input text that was validated
            validation_result (Dict[str, Any]): The validation result
            recommendation (Optional[str]): LLM-generated recommendation
            open_browser (bool): Whether to open the report in a browser

        Returns:
            Optional[str]: Path to the generated report, or None if report generation is disabled
        """
        if not self.enable_reports or not self.report_generator:
            logger.warning("Report generation is disabled")
            return None

        try:
            report_path = self.report_generator.generate_report(
                input_text=input_text,
                validation_result=validation_result,
                recommendation=recommendation,
                open_browser=open_browser
            )
            logger.info(f"Generated security validation report: {report_path}")
            return report_path
        except Exception as e:
            logger.error(f"Error generating report: {e}")
            return None

    def generate_recommendation(self, input_text: str, threats: List[Dict[str, Any]]) -> Optional[str]:
        """
        Generate a recommendation for security issues.

        Args:
            input_text (str): The input text that was validated
            threats (List[Dict[str, Any]]): List of detected threats

        Returns:
            Optional[str]: Generated recommendation, or None if recommendation generation is disabled
        """
        if not self.enable_recommendations:
            logger.warning("Recommendation generation is disabled")
            return None

        try:
            if self.recommendation_generator:
                return self.recommendation_generator.generate_recommendation(input_text, threats)
            else:
                return generate_basic_recommendation(input_text, threats)
        except Exception as e:
            logger.error(f"Error generating recommendation: {e}")
            return None
