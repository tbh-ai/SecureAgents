#!/usr/bin/env python3
"""
Test script for LLM recommendation feature.

This script demonstrates the LLM recommendation feature by generating
a sample report with LLM-based recommendations.
"""

import os
import sys
import logging
from typing import Dict, Any, Optional

# Add the current directory to the path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import the enhanced visualizer directly
from enhanced_visualizer import EnhancedVisualizer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def generate_sample_report_with_llm_recommendation(api_key: Optional[str] = None) -> str:
    """
    Generate a sample report with LLM-based recommendations.

    Args:
        api_key (Optional[str]): API key for Google Generative AI

    Returns:
        str: Path to the generated report
    """
    # Create a sample validation result with threats
    sample_result = {
        "is_secure": False,
        "method": "hybrid",
        "confidence": 0.95,
        "threshold": 0.8,
        "reason": "Critical system command that could harm the system",
        "validation_performance": {
            "total_time_ms": 6862.76,
            "methods_used": ["regex", "ml", "llm"],
            "regex_time_ms": 0.01,
            "ml_time_ms": 3.04,
            "llm_time_ms": 6861.61
        },
        "threats": [
            {
                "category": "privilege_escalation",
                "score": 0.85,
                "description": "The command attempts to delete files with elevated privileges"
            },
            {
                "category": "data_exfiltration",
                "score": 0.78,
                "description": "The command could potentially leak sensitive data"
            }
        ],
        "fix_suggestion": "Use secure file operations instead of system commands. For example, use Python's built-in file operations instead of 'rm -rf /tmp/data/*'."
    }

    # Sample input text
    sample_text = "rm -rf /tmp/data/*"

    # Create the visualizer with LLM recommendations enabled
    output_dir = "framework_integration_results"
    os.makedirs(output_dir, exist_ok=True)

    visualizer = EnhancedVisualizer(
        output_dir=output_dir,
        auto_save=False,
        use_llm_recommendations=True,
        llm_api_key=api_key,
        llm_model_name="gemini-2.0-flash-lite"
    )

    # Generate and save the report
    report_path = visualizer.save_report(sample_result, "standard", sample_text, "html")

    logger.info(f"Generated sample report with LLM recommendations at: {report_path}")

    return report_path


def generate_sample_report_without_llm() -> str:
    """
    Generate a sample report without LLM-based recommendations.

    Returns:
        str: Path to the generated report
    """
    # Create a sample validation result with threats
    sample_result = {
        "is_secure": False,
        "method": "hybrid",
        "confidence": 0.95,
        "threshold": 0.8,
        "reason": "Critical system command that could harm the system",
        "validation_performance": {
            "total_time_ms": 6862.76,
            "methods_used": ["regex", "ml", "llm"],
            "regex_time_ms": 0.01,
            "ml_time_ms": 3.04,
            "llm_time_ms": 6861.61
        },
        "threats": [
            {
                "category": "privilege_escalation",
                "score": 0.85,
                "description": "The command attempts to delete files with elevated privileges"
            },
            {
                "category": "data_exfiltration",
                "score": 0.78,
                "description": "The command could potentially leak sensitive data"
            }
        ],
        "fix_suggestion": "Use secure file operations instead of system commands. For example, use Python's built-in file operations instead of 'rm -rf /tmp/data/*'."
    }

    # Sample input text
    sample_text = "rm -rf /tmp/data/*"

    # Create the visualizer with LLM recommendations disabled
    output_dir = "framework_integration_results"
    os.makedirs(output_dir, exist_ok=True)

    visualizer = EnhancedVisualizer(
        output_dir=output_dir,
        auto_save=False,
        use_llm_recommendations=False
    )

    # Generate and save the report
    report_path = visualizer.save_report(sample_result, "standard", sample_text, "html")

    logger.info(f"Generated sample report without LLM recommendations at: {report_path}")

    return report_path


if __name__ == "__main__":
    # Check if API key is provided as an environment variable
    api_key = os.environ.get("GOOGLE_API_KEY")

    if api_key:
        # Generate report with LLM recommendations
        report_path = generate_sample_report_with_llm_recommendation(api_key)
    else:
        logger.warning("No Google API key found in environment variables. Generating report without LLM recommendations.")
        report_path = generate_sample_report_without_llm()

    # Try to open the report in the default browser
    try:
        import webbrowser
        webbrowser.open(f"file://{os.path.abspath(report_path)}")
        logger.info("Opened report in browser")
    except Exception as e:
        logger.error(f"Could not open browser: {e}")
