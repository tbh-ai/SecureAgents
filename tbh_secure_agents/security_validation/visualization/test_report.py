#!/usr/bin/env python3
"""
Test script to generate a sample professional report.
"""

import os
import sys
import json
from datetime import datetime

# Add the parent directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from security_validation.visualization.enhanced_visualizer import EnhancedVisualizer

def generate_sample_report():
    """Generate a sample report with the professional template."""
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
            "regex_time_ms": 0.01,
            "ml_time_ms": 3.04,
            "llm_time_ms": 6861.61
        },
        "threats": [
            {
                "category": "command_injection",
                "score": 0.92,
                "description": "The input contains a system command that could be used for command injection."
            },
            {
                "category": "privilege_escalation",
                "score": 0.85,
                "description": "The command attempts to access sensitive system files."
            },
            {
                "category": "data_exfiltration",
                "score": 0.78,
                "description": "The command could be used to extract sensitive data from the system."
            }
        ],
        "fix_suggestion": "Use secure file operations instead of system commands. For example, use Python's built-in file operations instead of 'rm -rf /tmp/data/*'."
    }

    # Sample input text
    sample_text = "rm -rf /tmp/data/*"

    # Create the visualizer
    output_dir = "framework_integration_results"
    os.makedirs(output_dir, exist_ok=True)
    
    visualizer = EnhancedVisualizer(output_dir=output_dir, auto_save=False)
    
    # Generate and save the report
    report_path = visualizer.save_report(sample_result, "standard", sample_text, "html")
    
    print(f"Generated sample report at: {report_path}")
    
    return report_path

if __name__ == "__main__":
    report_path = generate_sample_report()
    
    # Try to open the report in the default browser
    try:
        import webbrowser
        webbrowser.open(f"file://{os.path.abspath(report_path)}")
        print("Opened report in browser")
    except Exception as e:
        print(f"Could not open browser: {e}")
