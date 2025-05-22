#!/usr/bin/env python3
"""
Generate a sample HTML report with LLM recommendations.

This script demonstrates how the LLM recommendations would look in an HTML report.
"""

import os
import re
import logging
from datetime import datetime

# Import the basic recommendation function
from test_recommendation import _generate_basic_recommendation

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

def format_recommendation(recommendation_text):
    """
    Format the recommendation text for HTML display.

    Args:
        recommendation_text (str): The recommendation text in markdown format

    Returns:
        str: HTML formatted recommendation
    """
    # Process section headers (## headers)
    recommendation_text = re.sub(
        r'^## (.+)$',
        r'<h4>\1</h4>',
        recommendation_text,
        flags=re.MULTILINE
    )

    # Process bullet points
    lines = recommendation_text.split('\n')
    in_list = False
    result = []

    for line in lines:
        if line.strip().startswith('- '):
            if not in_list:
                result.append('<ul>')
                in_list = True
            # Convert the bullet point to an HTML list item
            item_content = line.strip()[2:]  # Remove the "- " prefix
            result.append(f'<li>{item_content}</li>')
        else:
            if in_list:
                result.append('</ul>')
                in_list = False
            result.append(line)

    if in_list:
        result.append('</ul>')

    # Process inline code
    formatted_text = '\n'.join(result)
    formatted_text = re.sub(
        r'`([^`]+)`',
        r'<code>\1</code>',
        formatted_text
    )

    # Wrap each section in a div
    formatted_text = re.sub(
        r'(<h4>.+?</h4>.*?)(?=<h4>|$)',
        r'<div class="recommendation-section">\1</div>',
        formatted_text,
        flags=re.DOTALL
    )

    return formatted_text

def generate_html_report():
    """Generate a sample HTML report with LLM recommendations."""
    # Sample input text
    input_text = "rm -rf /tmp/data/*"

    # Sample threats
    threats = [
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
    ]

    # Generate recommendation
    recommendation = _generate_basic_recommendation(input_text, threats)

    # Create HTML report
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Security Validation Report</title>
    <style>
        :root {{
            --primary-color: #2563eb;
            --primary-light: #dbeafe;
            --success-color: #10b981;
            --success-light: #d1fae5;
            --danger-color: #ef4444;
            --danger-light: #fee2e2;
            --warning-color: #f59e0b;
            --warning-light: #fef3c7;
            --text-color: #1e293b;
            --text-light: #64748b;
            --bg-color: #f8fafc;
            --card-bg: #ffffff;
            --border-color: #e2e8f0;
            --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            --logo-blue: #0052CC;
            --logo-text: #172B4D;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            line-height: 1.6;
            color: var(--text-color);
            background-color: var(--bg-color);
            padding: 0;
            margin: 0;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }}

        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid var(--border-color);
        }}

        .header-left {{
            display: flex;
            align-items: center;
            gap: 1rem;
        }}

        .logo-container {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .logo-box {{
            background-color: var(--logo-blue);
            width: 40px;
            height: 40px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 18px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}

        .logo-code {{
            font-family: monospace;
        }}

        .logo-text {{
            font-weight: bold;
            font-size: 20px;
            color: var(--logo-text);
            letter-spacing: -0.5px;
        }}

        .header h1 {{
            font-size: 1.8rem;
            font-weight: 600;
            color: var(--primary-color);
        }}

        .header .timestamp {{
            font-size: 0.9rem;
            color: var(--text-light);
        }}

        .card {{
            background-color: var(--card-bg);
            border-radius: 0.5rem;
            box-shadow: var(--shadow);
            margin-bottom: 1.5rem;
            overflow: hidden;
        }}

        .card-header {{
            padding: 1rem 1.5rem;
            border-bottom: 1px solid var(--border-color);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .card-header h2 {{
            font-size: 1.2rem;
            font-weight: 600;
        }}

        .card-body {{
            padding: 1.5rem;
        }}

        .badge {{
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
        }}

        .badge-danger {{
            background-color: var(--danger-light);
            color: var(--danger-color);
        }}

        .code-block {{
            background-color: #1e293b;
            color: #f8fafc;
            padding: 1rem;
            border-radius: 0.5rem;
            overflow-x: auto;
            font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
            font-size: 0.9rem;
            line-height: 1.5;
            margin-bottom: 1.5rem;
            max-height: 300px;
            overflow-y: auto;
        }}

        .threat-item {{
            padding: 1rem;
            border-radius: 0.5rem;
            margin-bottom: 1rem;
            border-left: 4px solid var(--danger-color);
            background-color: var(--danger-light);
        }}

        .threat-item h3 {{
            font-size: 1rem;
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
        }}

        .threat-item .score {{
            font-size: 0.8rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }}

        .threat-item .description {{
            font-size: 0.9rem;
        }}

        .llm-recommendation {{
            background-color: #f0f7ff;
            border-radius: 0.5rem;
            padding: 1.5rem;
            margin-top: 1.5rem;
            border: 1px solid #cce5ff;
        }}

        .llm-recommendation h3 {{
            font-size: 1.1rem;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            color: var(--primary-color);
            border-bottom: 1px solid #cce5ff;
            padding-bottom: 0.5rem;
        }}

        .recommendation-content {{
            font-size: 0.95rem;
            line-height: 1.6;
        }}

        .recommendation-section {{
            margin-bottom: 1.5rem;
        }}

        .recommendation-section:last-child {{
            margin-bottom: 0;
        }}

        .recommendation-section h4 {{
            font-size: 1rem;
            margin-bottom: 0.75rem;
            color: #2c5282;
            font-weight: 600;
        }}

        .recommendation-section ul {{
            margin-left: 1.5rem;
            margin-bottom: 0.5rem;
            list-style-type: disc;
        }}

        .recommendation-section li {{
            margin-bottom: 0.5rem;
        }}

        .recommendation-content code {{
            background-color: rgba(0, 0, 0, 0.05);
            padding: 0.2rem 0.4rem;
            border-radius: 0.25rem;
            font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
            font-size: 0.85em;
        }}

        .footer {{
            text-align: center;
            margin-top: 2rem;
            padding-top: 1rem;
            border-top: 1px solid var(--border-color);
            font-size: 0.8rem;
            color: var(--text-light);
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="header-left">
                <div class="logo-container">
                    <div class="logo-box">
                        <span class="logo-code">&lt;/&gt;</span>
                    </div>
                    <span class="logo-text">tbh.ai</span>
                </div>
                <h1>Security Validation Report</h1>
            </div>
            <div class="timestamp">{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</div>
        </div>

        <div class="card">
            <div class="card-header">
                <h2>Validation Result</h2>
                <span class="badge badge-danger">Insecure</span>
            </div>
            <div class="card-body">
                <div class="detail-item">
                    <div class="label">Reason</div>
                    <div class="value">Critical system command that could harm the system</div>
                </div>
            </div>
        </div>

        <div class="card">
            <div class="card-header">
                <h2>Input Text</h2>
            </div>
            <div class="card-body">
                <div class="code-block">{input_text}</div>
            </div>
        </div>

        <div class="card">
            <div class="card-header">
                <h2>Threat Analysis</h2>
            </div>
            <div class="card-body">
                <div class="threat-item">
                    <h3>Privilege Escalation</h3>
                    <div class="score">Score: 0.85</div>
                    <div class="description">The command attempts to delete files with elevated privileges</div>
                </div>
                <div class="threat-item">
                    <h3>Data Exfiltration</h3>
                    <div class="score">Score: 0.78</div>
                    <div class="description">The command could potentially leak sensitive data</div>
                </div>
            </div>
        </div>

        <div class="card">
            <div class="card-header">
                <h2>Detailed Recommendation</h2>
            </div>
            <div class="card-body">
                <div class="llm-recommendation">
                    <h3>AI-Generated Recommendation</h3>
                    <div class="recommendation-content">
                        {format_recommendation(recommendation)}
                    </div>
                </div>
            </div>
        </div>

        <div class="footer">
            <p>Generated by SecureAgents Security Validation Framework</p>
            <p>© 2025 tbh.ai - Secure AI Agent Framework</p>
        </div>
    </div>
</body>
</html>
"""

    # Save HTML report
    output_dir = "framework_integration_results"
    os.makedirs(output_dir, exist_ok=True)

    # No need to handle external assets as we're using inline styling

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"sample_report_with_llm_recommendation_{timestamp}.html"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w") as f:
        f.write(html)

    logger.info(f"Generated sample HTML report at: {filepath}")

    return filepath

if __name__ == "__main__":
    report_path = generate_html_report()

    # Try to open the report in the default browser
    try:
        import webbrowser
        webbrowser.open(f"file://{os.path.abspath(report_path)}")
        logger.info("Opened report in browser")
    except Exception as e:
        logger.error(f"Could not open browser: {e}")
