#!/usr/bin/env python3
"""
Test script for the enhanced security validation visualization.

This script generates a sample security validation report with the enhanced
visualization features, including the company logo and improved charts.
"""

import os
import base64
import logging
from datetime import datetime

from tbh_secure_agents.security_validation.visualization.enhanced_visualizer import EnhancedVisualizer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Get a logger for this module
logger = logging.getLogger(__name__)

def generate_sample_report():
    """Generate a sample report with the enhanced visualization features."""
    # Create a sample validation result
    sample_result = {
        "is_secure": False,
        "method": "hybrid",
        "confidence": 0.95,
        "threshold": 0.8,
        "reason": "Critical system command that could harm the system",
        "validation_performance": {
            "total_time_ms": 6862.76,
            "methods_used": ["regex", "ml", "llm"],
            "regex_time_ms": 0.51,
            "ml_time_ms": 3.04,
            "llm_time_ms": 6861.61
        },
        "threats": [
            {
                "category": "command_injection",
                "score": 0.92,
                "description": "The input contains a system command that could be used to delete files."
            },
            {
                "category": "privilege_escalation",
                "score": 0.78,
                "description": "The command attempts to access system directories which may require elevated privileges."
            },
            {
                "category": "data_destruction",
                "score": 0.85,
                "description": "The command could potentially delete important data."
            }
        ],
        "fix_suggestion": "Use secure file operations instead of system commands. For example, use Python's built-in file operations instead of 'rm -rf /tmp/data/*'.",
        "llm_recommendation": """
<div class="recommendation-section">
    <h4>⚠️ Security Assessment</h4>
    <p>The input contains potential security risks related to <strong>Command Injection</strong>.</p>

    <h4>🔍 Recommended Actions</h4>
    <ul>
        <li>Avoid using shell=True with subprocess functions</li>
        <li>Use a list of arguments instead of a string for subprocess calls</li>
        <li>Validate and sanitize all user inputs before using in commands</li>
        <li>Implement proper input escaping for shell arguments</li>
        <li>Consider using library functions instead of shell commands</li>
    </ul>

    <h4>🛡️ TBH.AI Secure Agents Framework Features</h4>
    <ul>
        <li><strong>Multi-layered Security Validation:</strong> Combines rule-based, ML, and LLM approaches</li>
        <li><strong>Customizable Security Profiles:</strong> Minimal, Low, Medium, High, and Maximum security levels</li>
        <li><strong>Real-time Threat Detection:</strong> Identifies potential security risks as code is written</li>
        <li><strong>Comprehensive Visualization:</strong> Detailed reports with actionable insights</li>
        <li><strong>Performance Optimization:</strong> Fast validation with minimal overhead</li>
    </ul>
</div>
"""
    }

    # Sample input text
    sample_text = "rm -rf /tmp/data/*"

    # Create the visualizer
    output_dir = "visualization_examples"
    os.makedirs(output_dir, exist_ok=True)

    # Create the logo directory if it doesn't exist
    templates_dir = os.path.join("tbh_secure_agents", "security_validation", "visualization", "templates")
    os.makedirs(templates_dir, exist_ok=True)

    # Convert the base64 logo to a PNG file if it doesn't exist
    logo_path = os.path.join(templates_dir, "tbh_logo.png")
    if not os.path.exists(logo_path):
        try:
            # Read the base64 logo from the text file
            logo_txt_path = os.path.join(templates_dir, "tbh_logo.txt")
            if os.path.exists(logo_txt_path):
                with open(logo_txt_path, "r") as f:
                    base64_data = f.read().strip()

                # Convert base64 to binary and save as PNG
                with open(logo_path, "wb") as f:
                    f.write(base64.b64decode(base64_data))

                logger.info(f"Created logo file at {logo_path}")
            else:
                logger.warning(f"Logo text file not found at {logo_txt_path}")
        except Exception as e:
            logger.error(f"Error creating logo file: {e}")

    # Initialize the visualizer with the logo path
    visualizer = EnhancedVisualizer(
        output_dir=output_dir,
        auto_save=False,
        use_llm_recommendations=False,  # Disable LLM recommendations since we don't have an API key
        logo_path=logo_path
    )

    # Verify the logo was loaded
    if visualizer.logo_base64:
        logger.info("Logo loaded successfully")
    else:
        logger.warning("Logo not loaded properly")

    # Generate and save the report
    report_path = visualizer.save_report(sample_result, "standard", sample_text, "html")

    logger.info(f"Generated sample report at: {report_path}")

    return report_path

if __name__ == "__main__":
    report_path = generate_sample_report()

    # Try to open the report in the default browser
    try:
        import webbrowser
        webbrowser.open(f"file://{os.path.abspath(report_path)}")
        logger.info("Opened report in browser")
    except Exception as e:
        logger.error(f"Could not open browser: {e}")
