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
        stripped_line = line.strip()
        if stripped_line.startswith('- ') or stripped_line.startswith('• '):
            if not in_list:
                result.append('<ul>')
                in_list = True
            # Convert the bullet point to an HTML list item
            if stripped_line.startswith('- '):
                item_content = stripped_line[2:]  # Remove the "- " prefix
            else:
                item_content = stripped_line[2:]  # Remove the "• " prefix
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
        # Extract validation information with proper defaults
        is_secure = validation_result.get("is_secure", False)
        reason = validation_result.get("reason", "Expert task execution completed successfully" if is_secure else "Security validation failed")
        threats = validation_result.get("threats", [])
        method = validation_result.get("method", "expert_validation")

        # Extract metrics if available
        metrics = validation_result.get("validation_metrics", {})
        validation_flow = validation_result.get("validation_flow", ["Input", "Regex"])

        # Extract security level and confidence with proper defaults
        security_level = "high"  # Default to high
        confidence = "High"      # Default to High
        threshold = "Standard"   # Default to Standard

        # Create HTML report
        html = self._create_html_template(
            input_text=input_text,
            is_secure=is_secure,
            reason=reason,
            threats=threats,
            recommendation=recommendation,
            method=method,
            metrics=metrics,
            validation_flow=validation_flow,
            security_level=security_level,
            confidence=confidence,
            threshold=threshold
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
                             recommendation: Optional[str] = None,
                             method: str = "expert_validation",
                             metrics: Dict[str, Any] = None,
                             validation_flow: List[str] = None,
                             security_level: str = "high",
                             confidence: str = "N/A",
                             threshold: str = "N/A") -> str:
        """
        Create the HTML template for the report.

        Args:
            input_text (str): The input text that was validated
            is_secure (bool): Whether the input is secure
            reason (str): Reason for validation result
            threats (List[Dict[str, Any]]): List of detected threats
            recommendation (Optional[str]): LLM-generated recommendation
            method (str): Validation method used
            metrics (Dict[str, Any]): Performance metrics
            validation_flow (List[str]): Validation flow steps
            security_level (str): Security level used
            confidence (str): Confidence score
            threshold (str): Threshold value

        Returns:
            str: HTML template
        """
        # Set defaults for mutable arguments
        if metrics is None:
            metrics = {}
        if validation_flow is None:
            validation_flow = []
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
                <table style="width: 100%; border-collapse: collapse;">
                    <tr style="border-bottom: 1px solid var(--border-color);">
                        <td style="padding: 0.5rem; font-weight: 600; width: 150px;">Security Level</td>
                        <td style="padding: 0.5rem;">{security_level}</td>
                    </tr>
                    <tr style="border-bottom: 1px solid var(--border-color);">
                        <td style="padding: 0.5rem; font-weight: 600;">Validation Method</td>
                        <td style="padding: 0.5rem;">{method}</td>
                    </tr>
                    <tr style="border-bottom: 1px solid var(--border-color);">
                        <td style="padding: 0.5rem; font-weight: 600;">Confidence</td>
                        <td style="padding: 0.5rem;">{confidence}</td>
                    </tr>
                    <tr style="border-bottom: 1px solid var(--border-color);">
                        <td style="padding: 0.5rem; font-weight: 600;">Threshold</td>
                        <td style="padding: 0.5rem;">{threshold}</td>
                    </tr>
                    <tr>
                        <td style="padding: 0.5rem; font-weight: 600;">Reason</td>
                        <td style="padding: 0.5rem;">{reason}</td>
                    </tr>
                </table>
            </div>
        </div>

        <!-- Validation Flow -->
        <div class="card">
            <div class="card-header">
                <h2>Validation Flow</h2>
            </div>
            <div class="card-body">
                <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                    {' → '.join(validation_flow) if validation_flow else 'Input → Regex'}
                </div>
                <div style="text-align: center; margin: 1rem 0;">
                    <svg width="400" height="100" viewBox="0 0 400 100" style="border: 1px solid var(--border-color); border-radius: 0.5rem; background: #f8fafc;">
                        <rect x="20" y="30" width="80" height="40" rx="5" fill="#dbeafe" stroke="#2563eb"/>
                        <text x="60" y="52" text-anchor="middle" font-size="12" fill="#2563eb">Input Text</text>
                        <rect x="160" y="30" width="80" height="40" rx="5" fill="#dcfce7" stroke="#10b981"/>
                        <text x="200" y="52" text-anchor="middle" font-size="12" fill="#10b981">Regex</text>
                        <path d="M 100 50 L 160 50" stroke="#64748b" stroke-width="2" marker-end="url(#arrowhead)"/>
                        <defs>
                            <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
                                <polygon points="0 0, 10 3.5, 0 7" fill="#64748b"/>
                            </marker>
                        </defs>
                    </svg>
                </div>
            </div>
        </div>

        <!-- Performance Metrics -->
        <div class="card">
            <div class="card-header">
                <h2>Performance Metrics</h2>
            </div>
            <div class="card-body">
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
                    <div style="text-align: center; padding: 1rem; background: #f8fafc; border-radius: 0.5rem;">
                        <div style="font-size: 1.5rem; font-weight: 600; color: var(--primary-color);">
                            {(metrics.get('total_time', 0.00) * 1000):.2f}
                        </div>
                        <div style="font-size: 0.9rem; color: var(--text-light);">Total Time</div>
                        <div style="font-size: 0.8rem; color: var(--text-light);">ms</div>
                    </div>
                    <div style="text-align: center; padding: 1rem; background: #f8fafc; border-radius: 0.5rem;">
                        <div style="font-size: 1.5rem; font-weight: 600; color: var(--primary-color);">
                            {(metrics.get('regex_time', 0.00) * 1000):.2f}
                        </div>
                        <div style="font-size: 0.9rem; color: var(--text-light);">Regex Time</div>
                        <div style="font-size: 0.8rem; color: var(--text-light);">ms</div>
                    </div>
                    <div style="text-align: center; padding: 1rem; background: #f8fafc; border-radius: 0.5rem;">
                        <div style="font-size: 1.5rem; font-weight: 600; color: var(--primary-color);">
                            {(metrics.get('ml_time', 0.00) * 1000):.2f}
                        </div>
                        <div style="font-size: 0.9rem; color: var(--text-light);">ML Time</div>
                        <div style="font-size: 0.8rem; color: var(--text-light);">ms</div>
                    </div>
                    <div style="text-align: center; padding: 1rem; background: #f8fafc; border-radius: 0.5rem;">
                        <div style="font-size: 1.5rem; font-weight: 600; color: var(--primary-color);">
                            {(metrics.get('llm_time', 0.00) * 1000):.2f}
                        </div>
                        <div style="font-size: 0.9rem; color: var(--text-light);">LLM Time</div>
                        <div style="font-size: 0.8rem; color: var(--text-light);">ms</div>
                    </div>
                </div>

                <!-- Validation Performance Chart -->
                <div style="margin-top: 2rem;">
                    <h3 style="margin-bottom: 1rem;">Validation Performance</h3>
                    <div style="background: white; padding: 1rem; border-radius: 0.5rem; border: 1px solid var(--border-color);">
                        <svg width="100%" height="200" viewBox="0 0 600 200">
                            <rect x="50" y="20" width="500" height="150" fill="none" stroke="#e2e8f0"/>
                            <!-- Y-axis labels -->
                            <text x="40" y="30" text-anchor="end" font-size="10" fill="#64748b">1.0</text>
                            <text x="40" y="60" text-anchor="end" font-size="10" fill="#64748b">0.8</text>
                            <text x="40" y="90" text-anchor="end" font-size="10" fill="#64748b">0.6</text>
                            <text x="40" y="120" text-anchor="end" font-size="10" fill="#64748b">0.4</text>
                            <text x="40" y="150" text-anchor="end" font-size="10" fill="#64748b">0.2</text>
                            <text x="40" y="180" text-anchor="end" font-size="10" fill="#64748b">0.0</text>
                            <!-- X-axis -->
                            <line x1="50" y1="170" x2="550" y2="170" stroke="#e2e8f0"/>
                            <!-- Bars -->
                            <rect x="100" y="150" width="80" height="20" fill="#3b82f6" opacity="0.8"/>
                            <text x="140" y="190" text-anchor="middle" font-size="10" fill="#64748b">Validation Time (ms)</text>
                            <!-- Legend -->
                            <rect x="450" y="30" width="15" height="15" fill="#3b82f6"/>
                            <text x="470" y="42" font-size="10" fill="#64748b">Validation Time (ms)</text>
                        </svg>
                    </div>
                </div>
            </div>
        </div>

        <!-- Threat Analysis -->
        <div class="card">
            <div class="card-header">
                <h2>Threat Analysis</h2>
            </div>
            <div class="card-body">
                <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                    <div style="display: flex; align-items: center; gap: 0.5rem;">
                        <div style="width: 12px; height: 12px; background: #ef4444; border-radius: 50%;"></div>
                        <span style="font-size: 0.9rem; color: var(--text-light);">Threat Score</span>
                    </div>
                </div>
                <div style="background: white; padding: 1rem; border-radius: 0.5rem; border: 1px solid var(--border-color); margin-bottom: 1rem;">
                    <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                        <div style="width: 24px; height: 24px; background: #ef4444; border-radius: 50%; display: flex; align-items: center; justify-content: center;">
                            <span style="color: white; font-size: 12px; font-weight: bold;">⚠</span>
                        </div>
                        <div>
                            <div style="font-weight: 600;">Score:</div>
                            <div style="color: var(--text-light); font-size: 0.9rem;">N/A</div>
                        </div>
                    </div>
                    <div style="background: white; padding: 1rem; border-radius: 0.5rem; border: 1px solid var(--border-color);">
                        <svg width="100%" height="150" viewBox="0 0 600 150">
                            <rect x="50" y="20" width="500" height="100" fill="none" stroke="#e2e8f0"/>
                            <!-- Y-axis labels -->
                            <text x="40" y="30" text-anchor="end" font-size="10" fill="#64748b">1.0</text>
                            <text x="40" y="50" text-anchor="end" font-size="10" fill="#64748b">0.8</text>
                            <text x="40" y="70" text-anchor="end" font-size="10" fill="#64748b">0.6</text>
                            <text x="40" y="90" text-anchor="end" font-size="10" fill="#64748b">0.4</text>
                            <text x="40" y="110" text-anchor="end" font-size="10" fill="#64748b">0.2</text>
                            <text x="40" y="130" text-anchor="end" font-size="10" fill="#64748b">0.0</text>
                            <!-- X-axis -->
                            <line x1="50" y1="120" x2="550" y2="120" stroke="#e2e8f0"/>
                            <!-- Threat score line (flat at 0 for secure content) -->
                            <line x1="50" y1="120" x2="550" y2="120" stroke="#ef4444" stroke-width="2"/>
                            <!-- Legend -->
                            <rect x="450" y="30" width="15" height="15" fill="#ef4444"/>
                            <text x="470" y="42" font-size="10" fill="#64748b">Threat Score</text>
                        </svg>
                    </div>
                </div>
                {threat_items_html if threats else "<p>No threats detected. The input appears to be secure.</p>"}
            </div>
        </div>

        <!-- Fix Suggestion -->
        <div class="card">
            <div class="card-header">
                <h2>Fix Suggestion</h2>
            </div>
            <div class="card-body">
                <div style="background: #d1fae5; padding: 1rem; border-radius: 0.5rem; border: 1px solid #10b981;">
                    <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                        <span style="color: #10b981; font-size: 1.2rem;">✓</span>
                        <span style="font-weight: 600; color: #10b981;">Recommended Fix</span>
                    </div>
                    <div style="color: #065f46;">N/A</div>
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



        {recommendation_html}

        <div class="footer">
            <p><strong>TBH.AI</strong></p>
            <p>Generated by TBH.AI Secure Agents Security Validation Framework</p>
            <p>© 2025 TBH.AI</p>
        </div>
    </div>
</body>
</html>"""

        return html
