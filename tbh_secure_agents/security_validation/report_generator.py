"""
HTML Report Generator for Security Validation.

This module provides functionality to generate HTML reports for security validation
results, including detailed threat analysis and recommendations.
"""

import os
import re
import logging
import webbrowser
from datetime import datetime
from typing import Dict, Any, List, Optional, Union, Tuple

# Get a logger for this module
logger = logging.getLogger(__name__)


def format_recommendation(recommendation_text: str) -> str:
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


class SecurityReportGenerator:
    """
    Generator for security validation HTML reports.
    
    This class provides functionality to generate detailed HTML reports for
    security validation results, including threat analysis and recommendations.
    """
    
    def __init__(self, output_dir: str = "security_reports"):
        """
        Initialize the security report generator.
        
        Args:
            output_dir (str): Directory to save reports
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_report(self, 
                        input_text: str, 
                        validation_result: Dict[str, Any],
                        recommendation: Optional[str] = None,
                        open_browser: bool = False) -> str:
        """
        Generate an HTML report for a security validation result.
        
        Args:
            input_text (str): The input text that was validated
            validation_result (Dict[str, Any]): The validation result
            recommendation (Optional[str]): LLM-generated recommendation
            open_browser (bool): Whether to open the report in a browser
            
        Returns:
            str: Path to the generated report
        """
        # Extract validation information
        is_secure = validation_result.get("is_secure", False)
        reason = validation_result.get("reason", "Unknown security issue")
        threats = validation_result.get("threats", [])
        
        # Create HTML report
        html = self._create_html_template(
            input_text=input_text,
            is_secure=is_secure,
            reason=reason,
            threats=threats,
            recommendation=recommendation
        )
        
        # Save the report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"security_validation_report_{timestamp}.html"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, "w") as f:
            f.write(html)
        
        logger.info(f"Generated security validation report at: {filepath}")
        
        # Open in browser if requested
        if open_browser:
            try:
                webbrowser.open(f"file://{os.path.abspath(filepath)}")
                logger.info("Opened report in browser")
            except Exception as e:
                logger.error(f"Could not open browser: {e}")
        
        return filepath
    
    def _create_html_template(self,
                             input_text: str,
                             is_secure: bool,
                             reason: str,
                             threats: List[Dict[str, Any]],
                             recommendation: Optional[str] = None) -> str:
        """
        Create the HTML template for the report.
        
        Args:
            input_text (str): The input text that was validated
            is_secure (bool): Whether the input is secure
            reason (str): Reason for validation result
            threats (List[Dict[str, Any]]): List of detected threats
            recommendation (Optional[str]): LLM-generated recommendation
            
        Returns:
            str: HTML template
        """
        # Generate threat items HTML
        threat_items_html = ""
        for threat in threats:
            category = threat.get("category", "unknown").replace("_", " ").title()
            score = threat.get("score", 0.0)
            description = threat.get("description", "")
            
            threat_items_html += f"""
                <div class="threat-item">
                    <h3>{category}</h3>
                    <div class="score">Score: {score:.2f}</div>
                    <div class="description">{description}</div>
                </div>
            """
        
        # Format recommendation if provided
        recommendation_html = ""
        if recommendation:
            recommendation_html = f"""
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
            """
        
        # Create the full HTML template
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
        
        .badge-success {{
            background-color: var(--success-light);
            color: var(--success-color);
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
                <span class="badge badge-{'success' if is_secure else 'danger'}">{('Secure' if is_secure else 'Insecure')}</span>
            </div>
            <div class="card-body">
                <div class="detail-item">
                    <div class="label">Reason</div>
                    <div class="value">{reason}</div>
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
                {threat_items_html if threats else "<p>No threats detected.</p>"}
            </div>
        </div>

        {recommendation_html}

        <div class="footer">
            <p>Generated by SecureAgents Security Validation Framework</p>
            <p>© 2025 tbh.ai - Secure AI Agent Framework</p>
        </div>
    </div>
</body>
</html>
"""
        
        return html
