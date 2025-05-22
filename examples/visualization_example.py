#!/usr/bin/env python3
"""
Visualization Example [BETA]

This example demonstrates the enhanced visualization for security validation results.
These features are currently in beta and may change in future releases.
"""

import os
import logging
import webbrowser
from tbh_secure_agents.security_validation import enable_improved_hybrid_validation
from tbh_secure_agents.security_validation.visualization.enhanced_visualizer import EnhancedVisualizer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set the API key (replace with your actual API key)
os.environ["GOOGLE_API_KEY"] = "YOUR_API_KEY_HERE"  # Replace with your actual API key

# Create output directory
os.makedirs("outputs/visualization", exist_ok=True)

def main():
    """Main function."""
    # Initialize the improved hybrid validator
    validator = enable_improved_hybrid_validation(
        api_key=os.environ.get("GOOGLE_API_KEY"),
        use_parallel=True,
        enable_reports=True,
        auto_open_reports=False,
        reports_dir="outputs/visualization",
        recommendation_style="detailed",
        include_code_examples=True
    )

    logger.info("Enabled improved hybrid validation system")

    # Test with different security profiles
    test_visualizations()

def test_visualizations():
    """Test the enhanced visualizations."""
    # Define a potentially risky operation
    risky_text = """
    import os
    import subprocess

    def delete_files(directory):
        # This is a dangerous command that could delete important files
        subprocess.run(f"rm -rf {directory}/*", shell=True)

    def backup_files(source, destination):
        # This uses system commands with shell=True which is risky
        os.system(f"cp -r {source} {destination}")

    def list_files(directory):
        # This is safer but still uses subprocess
        result = subprocess.check_output(["ls", "-la", directory])
        return result.decode("utf-8")

    # Main function
    if __name__ == "__main__":
        list_files("/tmp")
        backup_files("/home/user/important", "/backup")
        delete_files("/tmp/temp")
    """

    # Test with different security profiles
    security_profiles = ["minimal", "low", "standard", "high", "maximum"]

    for profile in security_profiles:
        logger.info(f"\n=== Testing {profile.upper()} security profile ===")

        # Validate the text
        result = validate_text(risky_text, profile)

        # Generate a report
        report_path = generate_report(risky_text, result, profile)

        # Open the report in the browser
        try:
            webbrowser.open(f"file://{os.path.abspath(report_path)}")
            logger.info(f"Opened report for {profile} profile in browser")
        except Exception as e:
            logger.error(f"Could not open browser: {e}")

def validate_text(text, security_level):
    """Validate text with the specified security level."""
    from tbh_secure_agents.security_validation.security_validator import validate

    # Create validation context
    context = {
        "security_level": security_level,
        "validation_type": "code",
        "operation_index": 0
    }

    # Validate the text
    result = validate(text, context)

    # Log the result
    is_secure = result.get("is_secure", False)
    logger.info(f"Validation result for {security_level} profile: {'Secure' if is_secure else 'Insecure'}")

    return result

def generate_report(text, result, security_level):
    """Generate a report for the validation result."""
    # Create a visualizer
    visualizer = EnhancedVisualizer(
        output_dir="outputs/visualization",
        auto_save=True,
        use_llm_recommendations=True,
        llm_api_key=os.environ.get("GOOGLE_API_KEY")
    )

    # Generate a report
    report_path = visualizer.save_report(result, security_level, text, "html")

    logger.info(f"Generated report for {security_level} profile: {report_path}")

    return report_path

if __name__ == "__main__":
    main()
