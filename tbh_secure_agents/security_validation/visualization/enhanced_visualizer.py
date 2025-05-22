#!/usr/bin/env python3
"""
Enhanced security validation visualizer.

This module provides enhanced visualization tools for security validation
results, including interactive HTML reports and detailed performance metrics.
"""

import os
import json
import time
import logging
import re
import base64
from typing import Dict, Any, List, Optional, Union
from datetime import datetime

# Import the LLM recommendation generator
from ..recommendation.llm_recommendation import LLMRecommendationGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Get a logger for this module
logger = logging.getLogger(__name__)


class EnhancedVisualizer:
    """
    Enhanced security validation visualizer.

    This class provides enhanced visualization tools for security validation
    results, including interactive HTML reports and detailed performance metrics.
    """

    def __init__(self, output_dir: Optional[str] = None, auto_save: bool = False,
                 max_reports: int = 100, retention_days: int = 7,
                 use_llm_recommendations: bool = True,
                 llm_api_key: Optional[str] = None,
                 llm_model_name: str = "gemini-2.0-flash-lite",
                 logo_path: Optional[str] = None):
        """
        Initialize the enhanced visualizer.

        Args:
            output_dir (Optional[str]): Directory to save visualizations
            auto_save (bool): Whether to automatically save reports for every validation
            max_reports (int): Maximum number of reports to keep
            retention_days (int): Number of days to keep reports
            use_llm_recommendations (bool): Whether to use LLM for generating recommendations
            llm_api_key (Optional[str]): API key for Google Generative AI
            llm_model_name (str): Model to use for recommendations
            logo_path (Optional[str]): Path to the company logo file
        """
        self.output_dir = output_dir or "validation_visualizations"
        self.auto_save = auto_save
        self.max_reports = max_reports
        self.retention_days = retention_days
        self.use_llm_recommendations = use_llm_recommendations
        self.logo_base64 = None

        # Initialize LLM recommendation generator if enabled
        self.llm_recommendation_generator = None
        if use_llm_recommendations:
            try:
                self.llm_recommendation_generator = LLMRecommendationGenerator(
                    api_key=llm_api_key,
                    model_name=llm_model_name
                )
                logger.info(f"Initialized LLM recommendation generator with model: {llm_model_name}")
            except Exception as e:
                logger.warning(f"Failed to initialize LLM recommendation generator: {e}")
                logger.warning("Falling back to basic recommendations")

        # In-memory storage for recent reports
        self.recent_reports = []

        # Create the output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)

        # Create templates directory if it doesn't exist
        templates_dir = os.path.join(os.path.dirname(__file__), "templates")
        os.makedirs(templates_dir, exist_ok=True)

        # Load the company logo
        self._load_logo(logo_path)

        # Log initialization
        logger.info(f"Initialized enhanced visualizer with output directory: {self.output_dir}")
        logger.info(f"Auto-save: {self.auto_save}, Max reports: {self.max_reports}, Retention days: {self.retention_days}")

        # Clean up old reports if needed
        if self.auto_save:
            self._cleanup_old_reports()

    def _load_logo(self, logo_path: Optional[str] = None):
        """
        Load the company logo and convert it to base64.

        Args:
            logo_path (Optional[str]): Path to the logo file
        """
        try:
            # If a specific logo path is provided, use it
            if logo_path and os.path.exists(logo_path):
                with open(logo_path, "rb") as f:
                    logo_data = f.read()
                    self.logo_base64 = base64.b64encode(logo_data).decode("utf-8")
                logger.info(f"Loaded custom logo from {logo_path}")
                return

            # Try to find the logo in the templates directory
            templates_dir = os.path.join(os.path.dirname(__file__), "templates")
            logo_paths = [
                os.path.join(templates_dir, "tbh_logo.png"),
                os.path.join(templates_dir, "logo.png"),
                os.path.join(templates_dir, "company_logo.png")
            ]

            for path in logo_paths:
                if os.path.exists(path):
                    with open(path, "rb") as f:
                        logo_data = f.read()
                        self.logo_base64 = base64.b64encode(logo_data).decode("utf-8")
                    logger.info(f"Loaded logo from {path}")
                    return

            # If no logo file is found, create a simple, professional logo
            logger.warning("No logo file found, creating a simple professional logo")
            from PIL import Image, ImageDraw, ImageFont
            import io

            # Create a blank image with transparent background
            width, height = 200, 50
            img = Image.new('RGBA', (width, height), color=(255, 255, 255, 0))
            d = ImageDraw.Draw(img)

            # Use a default font
            try:
                # Try to use a system font
                font = ImageFont.truetype("Arial Bold", 28)
            except:
                # Fall back to default font
                font = ImageFont.load_default()

            # Draw solid background
            d.rectangle([(0, 0), (width, height)], fill=(0, 51, 102, 255))

            # Draw the text
            d.text((20, 10), "TBH.AI", fill=(255, 255, 255, 255), font=font)

            # Save to a bytes buffer
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")

            # Convert to base64
            self.logo_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
            logger.info("Created professional logo")

        except Exception as e:
            logger.warning(f"Error loading logo: {e}")
            self.logo_base64 = ""

    def _cleanup_old_reports(self):
        """Clean up old reports based on retention policy."""
        try:
            # Get all report files
            report_files = []
            for filename in os.listdir(self.output_dir):
                if filename.startswith("validation_report_") and (filename.endswith(".html") or filename.endswith(".md")):
                    file_path = os.path.join(self.output_dir, filename)
                    report_files.append((file_path, os.path.getmtime(file_path)))

            # Sort by modification time (oldest first)
            report_files.sort(key=lambda x: x[1])

            # Delete old files based on max_reports
            if len(report_files) > self.max_reports:
                for file_path, _ in report_files[:-self.max_reports]:
                    os.remove(file_path)
                    logger.debug(f"Deleted old report: {file_path}")

            # Delete files older than retention_days
            cutoff_time = time.time() - (self.retention_days * 86400)
            for file_path, mtime in report_files:
                if mtime < cutoff_time:
                    os.remove(file_path)
                    logger.debug(f"Deleted expired report: {file_path}")

        except Exception as e:
            logger.warning(f"Error cleaning up old reports: {e}")

    def generate_mermaid_flow(self, result: Dict[str, Any], security_level: str) -> str:
        """
        Generate a Mermaid flow diagram for the validation result.

        Args:
            result (Dict[str, Any]): Validation result
            security_level (str): Security level used for validation

        Returns:
            str: Mermaid flow diagram
        """
        # Extract performance metrics
        performance = result.get("validation_performance", {})
        methods_used = performance.get("methods_used", [])

        # Extract times
        regex_time = performance.get("regex_time_ms", 0)
        ml_time = performance.get("ml_time_ms", 0)
        llm_time = performance.get("llm_time_ms", 0)

        # Determine the final method
        final_method = result.get("method", "unknown")

        # Determine if the validation passed or failed
        is_secure = result.get("is_secure", False)

        # Create the Mermaid diagram
        mermaid = [
            "```mermaid",
            "graph TD",
            "    Input[\"Input Text\"] --> Regex"
        ]

        # Add nodes for each method used
        if "regex" in methods_used:
            mermaid.append(f"    Regex[\"Regex Validator<br>({regex_time:.2f} ms)\"]")

            if len(methods_used) == 1 or final_method == "regex":
                if is_secure:
                    mermaid.append("    Regex --> RegexPass[\"✅ Passed\"]")
                else:
                    mermaid.append("    Regex --> RegexFail[\"❌ Failed\"]")
            else:
                mermaid.append("    Regex --> ML")

        if "ml" in methods_used:
            mermaid.append(f"    ML[\"ML Validator<br>({ml_time:.2f} ms)\"]")

            if len(methods_used) == 2 or final_method == "ml":
                if is_secure:
                    mermaid.append("    ML --> MLPass[\"✅ Passed\"]")
                else:
                    mermaid.append("    ML --> MLFail[\"❌ Failed\"]")
            else:
                mermaid.append("    ML --> LLM")

        if "llm" in methods_used:
            mermaid.append(f"    LLM[\"LLM Validator<br>({llm_time:.2f} ms)\"]")

            if is_secure:
                mermaid.append("    LLM --> LLMPass[\"✅ Passed\"]")
            else:
                mermaid.append("    LLM --> LLMFail[\"❌ Failed\"]")

        # Add styling
        mermaid.extend([
            "",
            "    %% Styling",
            "    classDef input fill:#f9f9f9,stroke:#333,stroke-width:2px;",
            "    classDef validator fill:#e1f5fe,stroke:#0288d1,stroke-width:2px;",
            "    classDef pass fill:#e8f5e9,stroke:#4caf50,stroke-width:2px;",
            "    classDef fail fill:#ffebee,stroke:#f44336,stroke-width:2px;",
            "    class Input input;",
            "    class Regex,ML,LLM validator;",
            "    class RegexPass,MLPass,LLMPass pass;",
            "    class RegexFail,MLFail,LLMFail fail;",
            ""
        ])

        mermaid.append("```")

        return "\n".join(mermaid)

    def generate_performance_chart(self, result: Dict[str, Any]) -> str:
        """
        Generate a performance chart for the validation result.

        Args:
            result (Dict[str, Any]): Validation result

        Returns:
            str: Performance chart in Mermaid format
        """
        # Extract performance metrics
        performance = result.get("validation_performance", {})
        methods_used = performance.get("methods_used", [])

        # Extract times
        regex_time = performance.get("regex_time_ms", 0)
        ml_time = performance.get("ml_time_ms", 0)
        llm_time = performance.get("llm_time_ms", 0)
        total_time = performance.get("total_time_ms", 0)

        # Calculate percentages
        regex_percent = (regex_time / total_time) * 100 if total_time > 0 else 0
        ml_percent = (ml_time / total_time) * 100 if total_time > 0 else 0
        llm_percent = (llm_time / total_time) * 100 if total_time > 0 else 0

        # Create the Mermaid chart
        mermaid = [
            "```mermaid",
            "pie",
            "    title Validation Time Distribution",
        ]

        # Add slices for each method used
        if "regex" in methods_used:
            mermaid.append(f"    \"Regex: {regex_time:.2f}ms\" : {regex_percent:.1f}")

        if "ml" in methods_used:
            mermaid.append(f"    \"ML: {ml_time:.2f}ms\" : {ml_percent:.1f}")

        if "llm" in methods_used:
            mermaid.append(f"    \"LLM: {llm_time:.2f}ms\" : {llm_percent:.1f}")

        mermaid.append("```")

        return "\n".join(mermaid)

    def generate_threat_chart(self, result: Dict[str, Any]) -> str:
        """
        Generate a threat chart for the validation result.

        Args:
            result (Dict[str, Any]): Validation result

        Returns:
            str: Threat chart in Mermaid format
        """
        # Extract threats
        threats = result.get("threats", [])

        if not threats:
            return "No threats detected."

        # Create the Mermaid chart
        mermaid = [
            "```mermaid",
            "graph LR",
        ]

        # Add nodes for each threat
        for i, threat in enumerate(threats):
            category = threat.get("category", "unknown")
            score = threat.get("score", 0.0)

            # Determine color based on score
            if score >= 0.8:
                color = "red"
            elif score >= 0.5:
                color = "orange"
            else:
                color = "yellow"

            mermaid.append(f"    T{i}[\"{category}<br>Score: {score:.2f}\"]")

            # Add styling
            mermaid.append(f"    style T{i} fill:{color},stroke:#333,stroke-width:2px;")

        mermaid.append("```")

        return "\n".join(mermaid)

    def generate_llm_recommendation(self, text: str, result: Dict[str, Any]) -> str:
        """
        Generate an LLM-based recommendation for security issues.

        Args:
            text (str): The text that was validated
            result (Dict[str, Any]): Validation result

        Returns:
            str: Generated recommendation
        """
        # If LLM recommendations are disabled or generator is not initialized, return basic recommendation
        if not self.use_llm_recommendations or self.llm_recommendation_generator is None:
            return self._generate_basic_recommendation(text, result)

        try:
            # Extract threats
            threats = result.get("threats", [])

            # Generate recommendation using LLM
            recommendation = self.llm_recommendation_generator.generate_recommendation(text, threats)

            return recommendation

        except Exception as e:
            logger.warning(f"Error generating LLM recommendation: {e}")
            return self._generate_basic_recommendation(text, result)

    def _generate_basic_recommendation(self, text: str, result: Dict[str, Any]) -> str:
        """
        Generate a basic recommendation for security issues.

        Args:
            text (str): The text that was validated
            result (Dict[str, Any]): Validation result

        Returns:
            str: Basic recommendation
        """
        # Extract threats
        threats = result.get("threats", [])

        if not threats:
            return """
<div class="recommendation-section">
    <h3>✅ Security Assessment</h3>
    <p>No security issues detected. The input appears to be secure.</p>

    <h3>🔄 Recommended Security Profile</h3>
    <p>Current code meets security requirements. You may continue using the <strong>Minimal</strong> security profile for development.</p>

    <h3>🛡️ TBH.AI Secure Agents Framework</h3>
    <ul>
        <li><strong>Multi-layered Security:</strong> Rule-based, ML, and LLM validation</li>
        <li><strong>Customizable Profiles:</strong> Minimal to Maximum security levels</li>
        <li><strong>Real-time Protection:</strong> Immediate threat detection</li>
        <li><strong>Performance Optimized:</strong> Minimal validation overhead</li>
    </ul>
</div>
"""

        # Get the highest scoring threat
        highest_threat = max(threats, key=lambda x: x.get("score", 0.0))
        category = highest_threat.get("category", "unknown").replace("_", " ").title()
        score = highest_threat.get("score", 0.0)

        # Determine recommended security profile based on threat score
        if score > 0.8:
            recommended_profile = "High or Maximum"
        elif score > 0.5:
            recommended_profile = "Medium"
        else:
            recommended_profile = "Low or Standard"

        # Common framework features section
        framework_features = """
<h3>🛡️ TBH.AI Secure Agents Framework</h3>
<ul>
    <li><strong>Multi-layered Security:</strong> Rule-based, ML, and LLM validation</li>
    <li><strong>Customizable Profiles:</strong> Minimal to Maximum security levels</li>
    <li><strong>Real-time Protection:</strong> Immediate threat detection</li>
    <li><strong>Performance Optimized:</strong> Minimal validation overhead</li>
</ul>
"""

        # Generate a basic recommendation based on the threat category
        if "privilege_escalation" in category.lower():
            return f"""
<div class="recommendation-section">
    <h3>⚠️ Security Assessment</h3>
    <p>Potential <strong>{category}</strong> risk detected with confidence score: {score:.2f}</p>

    <h3>🔄 Recommended Security Profile</h3>
    <p>Consider using the <strong>{recommended_profile}</strong> security profile for this code.</p>

    <h3>🔍 Code Modifications</h3>
    <ul>
        <li>Replace system commands with secure file operations</li>
        <li>Add permission validation before executing privileged operations</li>
        <li>Implement strict input validation for all parameters</li>
        <li>Use Python's built-in file handling instead of shell commands</li>
        <li>Apply least privilege principle throughout the code</li>
    </ul>

    {framework_features}
</div>
"""

        elif "data_exfiltration" in category.lower():
            return f"""
<div class="recommendation-section">
    <h3>⚠️ Security Assessment</h3>
    <p>Potential <strong>{category}</strong> risk detected with confidence score: {score:.2f}</p>

    <h3>🔄 Recommended Security Profile</h3>
    <p>Consider using the <strong>{recommended_profile}</strong> security profile for this code.</p>

    <h3>🔍 Code Modifications</h3>
    <ul>
        <li>Restrict external data transmission to authorized endpoints only</li>
        <li>Implement proper encryption for all data transfers</li>
        <li>Add comprehensive logging for all network operations</li>
        <li>Apply data minimization principles to limit exposure</li>
        <li>Use secure API authentication for all external communications</li>
    </ul>

    {framework_features}
</div>
"""

        elif "code_injection" in category.lower():
            return f"""
<div class="recommendation-section">
    <h3>⚠️ Security Assessment</h3>
    <p>Potential <strong>{category}</strong> risk detected with confidence score: {score:.2f}</p>

    <h3>🔄 Recommended Security Profile</h3>
    <p>Consider using the <strong>{recommended_profile}</strong> security profile for this code.</p>

    <h3>🔍 Code Modifications</h3>
    <ul>
        <li>Replace eval() or exec() with safer alternatives</li>
        <li>Implement strict input validation and sanitization</li>
        <li>Use JSON or other structured parsers instead of code execution</li>
        <li>Consider sandboxed execution environments if dynamic code is required</li>
        <li>Add runtime monitoring for unexpected code execution</li>
    </ul>

    {framework_features}
</div>
"""

        elif "command_injection" in category.lower():
            return f"""
<div class="recommendation-section">
    <h3>⚠️ Security Assessment</h3>
    <p>Potential <strong>{category}</strong> risk detected with confidence score: {score:.2f}</p>

    <h3>🔄 Recommended Security Profile</h3>
    <p>Consider using the <strong>{recommended_profile}</strong> security profile for this code.</p>

    <h3>🔍 Code Modifications</h3>
    <ul>
        <li>Use subprocess with argument lists instead of shell=True</li>
        <li>Implement strict input validation for all command parameters</li>
        <li>Replace shell commands with native Python libraries where possible</li>
        <li>Add proper escaping for any user-provided command arguments</li>
        <li>Consider using restricted execution environments</li>
    </ul>

    {framework_features}
</div>
"""

        else:
            return f"""
<div class="recommendation-section">
    <h3>⚠️ Security Assessment</h3>
    <p>Potential <strong>{category}</strong> risk detected with confidence score: {score:.2f}</p>

    <h3>🔄 Recommended Security Profile</h3>
    <p>Consider using the <strong>{recommended_profile}</strong> security profile for this code.</p>

    <h3>🔍 Code Modifications</h3>
    <ul>
        <li>Implement comprehensive input validation and sanitization</li>
        <li>Add appropriate security controls specific to this threat category</li>
        <li>Follow secure coding practices throughout the implementation</li>
        <li>Consider using the framework's built-in security features</li>
        <li>Add additional logging and monitoring for suspicious activities</li>
    </ul>

    {framework_features}
</div>
"""

    def generate_markdown_report(self, result: Dict[str, Any], security_level: str, text: str) -> str:
        """
        Generate a Markdown report for the validation result.

        Args:
            result (Dict[str, Any]): Validation result
            security_level (str): Security level used for validation
            text (str): The text that was validated

        Returns:
            str: Markdown report
        """
        # Extract basic information
        is_secure = result.get("is_secure", False)
        method = result.get("method", "unknown")
        confidence = result.get("confidence", 0.0)
        threshold = result.get("threshold", 0.0)
        reason = result.get("reason", "")

        # Extract performance metrics
        performance = result.get("validation_performance", {})
        total_time = performance.get("total_time_ms", 0)
        methods_used = performance.get("methods_used", [])
        regex_time = performance.get("regex_time_ms", 0)
        ml_time = performance.get("ml_time_ms", 0)
        llm_time = performance.get("llm_time_ms", 0)

        # Extract complexity information
        complexity_info = result.get("complexity_info", {})
        is_complex = complexity_info.get("is_complex", False)
        complexity_score = complexity_info.get("complexity_score", 0.0)
        patterns = complexity_info.get("patterns", [])

        # Extract threats
        threats = result.get("threats", [])

        # Create the Markdown report
        report = [
            "# Validation Report",
            "",
            f"## Input Text",
            "",
            f"```",
            text[:500] + ("..." if len(text) > 500 else ""),
            f"```",
            "",
            "## Validation Flow",
            "",
            self.generate_mermaid_flow(result, security_level),
            "",
            "## Validation Details",
            "",
            f"- Security Level: {security_level}",
            f"- Validation Method: {method}",
            f"- Is Secure: {'Yes' if is_secure else 'No'}",
        ]

        if "confidence" in result:
            report.append(f"- Confidence: {confidence:.2f}")

        if "threshold" in result:
            report.append(f"- Threshold: {threshold:.2f}")

        if reason:
            report.append(f"- Reason: {reason}")

        report.extend([
            "",
            "## Validation Performance",
            "",
            self.generate_performance_chart(result),
            "",
            f"- Total Time: {total_time:.2f} ms",
            f"- Methods Used: {', '.join(methods_used)}",
            f"- Regex Time: {regex_time:.2f} ms",
            f"- ML Time: {ml_time:.2f} ms",
            f"- LLM Time: {llm_time:.2f} ms",
        ])

        if complexity_info:
            report.extend([
                "",
                "## Complexity Analysis",
                "",
                f"- Is Complex: {'Yes' if is_complex else 'No'}",
                f"- Complexity Score: {complexity_score:.2f}",
            ])

            if patterns:
                report.append(f"- Patterns Detected: {', '.join(patterns)}")

        if threats:
            report.extend([
                "",
                "## Threat Analysis",
                "",
                self.generate_threat_chart(result),
                "",
                "### Detected Threats",
                "",
            ])

            for threat in threats:
                category = threat.get("category", "unknown")
                score = threat.get("score", 0.0)
                description = threat.get("description", "")

                report.extend([
                    f"#### {category.replace('_', ' ').title()}",
                    "",
                    f"- Score: {score:.2f}",
                    f"- Description: {description}",
                    "",
                ])

        if "fix_suggestion" in result:
            report.extend([
                "## Fix Suggestion",
                "",
                "```",
                result["fix_suggestion"],
                "```",
                "",
            ])

        # Add LLM recommendation
        llm_recommendation = self.generate_llm_recommendation(text, result)
        if llm_recommendation:
            report.extend([
                "## Detailed Recommendation",
                "",
                llm_recommendation,
                "",
            ])

        # Add timestamp
        report.extend([
            "---",
            "",
            f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        ])

        return "\n".join(report)

    def generate_html_report(self, result: Dict[str, Any], security_level: str, text: str) -> str:
        """
        Generate an HTML report for the validation result.

        Args:
            result (Dict[str, Any]): Validation result
            security_level (str): Security level used for validation
            text (str): The text that was validated

        Returns:
            str: HTML report
        """
        # Load the professional template
        template_path = os.path.join(os.path.dirname(__file__), "templates", "professional_report.html")
        try:
            with open(template_path, "r") as f:
                template_content = f.read()
        except FileNotFoundError:
            logger.warning(f"Professional template not found at {template_path}, falling back to basic template")
            return self._generate_basic_html_report(result, security_level, text)

        # Extract basic information
        is_secure = result.get("is_secure", False)
        method = result.get("method", "unknown")
        confidence = result.get("confidence", 0.0)
        threshold = result.get("threshold", 0.0)
        reason = result.get("reason", "")

        # Extract performance metrics
        performance = result.get("validation_performance", {})
        total_time = performance.get("total_time_ms", 0)
        regex_time = performance.get("regex_time_ms", 0)
        ml_time = performance.get("ml_time_ms", 0)
        llm_time = performance.get("llm_time_ms", 0)

        # Extract threats
        threats = result.get("threats", [])

        # Prepare threat data for charts
        threat_labels = []
        threat_data = []

        for threat in threats:
            category = threat.get("category", "unknown").replace("_", " ").title()
            score = threat.get("score", 0.0)
            threat_labels.append(f'"{category}"')
            threat_data.append(str(score))

        # Extract fix suggestion
        fix_suggestion = result.get("fix_suggestion", "")

        # Generate LLM recommendation
        llm_recommendation = self.generate_llm_recommendation(text, result)

        # Generate mermaid diagrams
        validation_flow = self.generate_mermaid_flow(result, security_level).replace("```mermaid", "").replace("```", "").strip()
        performance_chart = self.generate_performance_chart(result).replace("```mermaid", "").replace("```", "").strip()
        threat_chart = self.generate_threat_chart(result).replace("```mermaid", "").replace("```", "").strip() if threats else ""

        # Format timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Replace template placeholders
        html = template_content

        # Basic replacements
        replacements = {
            "{{timestamp}}": timestamp,
            "{{security_level}}": security_level,
            "{{method}}": method,
            "{{input_text}}": text[:500] + ("..." if len(text) > 500 else ""),
            "{{reason}}": reason,
            "{{total_time}}": f"{total_time:.2f}",
            "{{regex_time}}": f"{regex_time:.2f}",
            "{{ml_time}}": f"{ml_time:.2f}",
            "{{llm_time}}": f"{llm_time:.2f}",
            "{{validation_flow}}": validation_flow,
            "{{performance_chart}}": performance_chart,
            "{{threat_chart}}": threat_chart,
            "{{fix_suggestion}}": fix_suggestion,
            "{{llm_recommendation}}": llm_recommendation,
            "{{logo_base64}}": self.logo_base64 or "",
            "{{threat_labels}}": "[" + ", ".join(threat_labels) + "]" if threat_labels else "[]",
            "{{threat_data}}": "[" + ", ".join(threat_data) + "]" if threat_data else "[]"
        }

        for placeholder, value in replacements.items():
            html = html.replace(placeholder, str(value))

        # Conditional sections
        if is_secure:
            html = html.replace("{{#if is_secure}}", "").replace("{{else}}", "<!--").replace("{{/if}}", "-->")
        else:
            html = html.replace("{{#if is_secure}}", "<!--").replace("{{else}}", "-->").replace("{{/if}}", "")

        # Handle confidence and threshold
        if "confidence" in result:
            html = html.replace("{{#if confidence}}", "").replace("{{/if confidence}}", "")
            html = html.replace("{{confidence}}", f"{confidence:.2f}")
        else:
            html = re.sub(r'{{#if confidence}}.*?{{/if confidence}}', '', html, flags=re.DOTALL)

        if "threshold" in result:
            html = html.replace("{{#if threshold}}", "").replace("{{/if threshold}}", "")
            html = html.replace("{{threshold}}", f"{threshold:.2f}")
        else:
            html = re.sub(r'{{#if threshold}}.*?{{/if threshold}}', '', html, flags=re.DOTALL)

        # Handle regex, ml, llm times
        if regex_time > 0:
            html = html.replace("{{#if regex_time}}", "").replace("{{/if regex_time}}", "")
        else:
            html = re.sub(r'{{#if regex_time}}.*?{{/if regex_time}}', '', html, flags=re.DOTALL)

        if ml_time > 0:
            html = html.replace("{{#if ml_time}}", "").replace("{{/if ml_time}}", "")
        else:
            html = re.sub(r'{{#if ml_time}}.*?{{/if ml_time}}', '', html, flags=re.DOTALL)

        if llm_time > 0:
            html = html.replace("{{#if llm_time}}", "").replace("{{/if llm_time}}", "")
        else:
            html = re.sub(r'{{#if llm_time}}.*?{{/if llm_time}}', '', html, flags=re.DOTALL)

        # Handle threats
        if threats:
            html = html.replace("{{#if threats}}", "").replace("{{/if threats}}", "")

            # Generate threat items
            threat_items_html = ""
            for threat in threats:
                category = threat.get("category", "unknown")
                score = threat.get("score", 0.0)
                description = threat.get("description", "")

                threat_item = f"""
                <div class="threat-item">
                    <h3><i class="fas fa-shield-alt"></i> {category}</h3>
                    <div class="score">Score: {score:.2f}</div>
                    <div class="description">{description}</div>
                </div>
                """
                threat_items_html += threat_item

            html = html.replace("{{#each threats}}", "").replace("{{/each}}", "")
            html = html.replace("{{category}}", "").replace("{{score}}", "").replace("{{description}}", "")

            # Insert all threat items
            html = html.replace('<div class="threat-item">', threat_items_html + '<div class="threat-item" style="display:none;">')
        else:
            html = re.sub(r'{{#if threats}}.*?{{/if threats}}', '', html, flags=re.DOTALL)

        # Handle fix suggestion
        if fix_suggestion:
            html = html.replace("{{#if fix_suggestion}}", "").replace("{{/if fix_suggestion}}", "")
        else:
            html = re.sub(r'{{#if fix_suggestion}}.*?{{/if fix_suggestion}}', '', html, flags=re.DOTALL)

        # Handle LLM recommendation
        if llm_recommendation:
            html = html.replace("{{#if llm_recommendation}}", "").replace("{{/if llm_recommendation}}", "")
        else:
            html = re.sub(r'{{#if llm_recommendation}}.*?{{/if llm_recommendation}}', '', html, flags=re.DOTALL)

        # Clean up any remaining template tags
        html = re.sub(r'{{.*?}}', '', html)

        return html

    def _generate_basic_html_report(self, result: Dict[str, Any], security_level: str, text: str) -> str:
        """
        Generate a basic HTML report as fallback if the professional template is not available.

        Args:
            result (Dict[str, Any]): Validation result
            security_level (str): Security level used for validation
            text (str): The text that was validated

        Returns:
            str: HTML report
        """
        # Generate the Markdown report
        markdown = self.generate_markdown_report(result, security_level, text)

        # Create the HTML report
        html = [
            "<!DOCTYPE html>",
            "<html>",
            "<head>",
            "    <meta charset=\"UTF-8\">",
            "    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">",
            "    <title>Security Validation Report</title>",
            "    <script src=\"https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js\"></script>",
            "    <link rel=\"stylesheet\" href=\"https://cdn.jsdelivr.net/npm/github-markdown-css/github-markdown.min.css\">",
            "    <style>",
            "        body {",
            "            font-family: -apple-system, BlinkMacSystemFont, \"Segoe UI\", Helvetica, Arial, sans-serif;",
            "            line-height: 1.6;",
            "            color: #24292e;",
            "            max-width: 800px;",
            "            margin: 0 auto;",
            "            padding: 20px;",
            "        }",
            "        .markdown-body {",
            "            box-sizing: border-box;",
            "            min-width: 200px;",
            "            max-width: 980px;",
            "            margin: 0 auto;",
            "            padding: 45px;",
            "        }",
            "        @media (max-width: 767px) {",
            "            .markdown-body {",
            "                padding: 15px;",
            "            }",
            "        }",
            "    </style>",
            "</head>",
            "<body>",
            "    <div class=\"markdown-body\">",
            f"        {markdown}",
            "    </div>",
            "    <script>",
            "        mermaid.initialize({startOnLoad:true});",
            "    </script>",
            "</body>",
            "</html>",
        ]

        return "\n".join(html)

    def store_report(self, result: Dict[str, Any], security_level: str, text: str) -> Dict[str, Any]:
        """
        Store a report in memory.

        Args:
            result (Dict[str, Any]): Validation result
            security_level (str): Security level used for validation
            text (str): The text that was validated

        Returns:
            Dict[str, Any]: Report metadata
        """
        # Generate a report ID
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        method = result.get("method", "unknown")
        is_secure = "secure" if result.get("is_secure", False) else "insecure"
        report_id = f"{security_level}_{method}_{is_secure}_{timestamp}"

        # Generate report content
        markdown_content = self.generate_markdown_report(result, security_level, text)
        html_content = self.generate_html_report(result, security_level, text)

        # Create report metadata
        report_metadata = {
            "id": report_id,
            "timestamp": datetime.now().isoformat(),
            "security_level": security_level,
            "method": method,
            "is_secure": result.get("is_secure", False),
            "text": text,
            "result": result,
            "markdown_content": markdown_content,
            "html_content": html_content
        }

        # Store the report in memory
        self.recent_reports.append(report_metadata)

        # Limit the number of in-memory reports
        if len(self.recent_reports) > self.max_reports:
            self.recent_reports.pop(0)

        # Auto-save if enabled
        if self.auto_save:
            self.save_report(result, security_level, text, "html")

        return report_metadata

    def get_recent_reports(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent reports.

        Args:
            limit (int): Maximum number of reports to return

        Returns:
            List[Dict[str, Any]]: List of report metadata
        """
        # Return the most recent reports (limited by limit)
        return self.recent_reports[-limit:]

    def get_report_by_id(self, report_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a report by ID.

        Args:
            report_id (str): Report ID

        Returns:
            Optional[Dict[str, Any]]: Report metadata or None if not found
        """
        # Find the report with the given ID
        for report in self.recent_reports:
            if report["id"] == report_id:
                return report

        return None

    def save_report(self, result: Dict[str, Any], security_level: str, text: str, format: str = "markdown") -> str:
        """
        Save a report to disk.

        Args:
            result (Dict[str, Any]): Validation result
            security_level (str): Security level used for validation
            text (str): The text that was validated
            format (str): Report format (markdown or html)

        Returns:
            str: Path to the saved report
        """
        # Generate a filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        method = result.get("method", "unknown")
        is_secure = "secure" if result.get("is_secure", False) else "insecure"

        if format == "html":
            filename = f"validation_report_{security_level}_{method}_{is_secure}_{timestamp}.html"
            content = self.generate_html_report(result, security_level, text)
        else:
            filename = f"validation_report_{security_level}_{method}_{is_secure}_{timestamp}.md"
            content = self.generate_markdown_report(result, security_level, text)

        # Save the report
        path = os.path.join(self.output_dir, filename)
        with open(path, "w") as f:
            f.write(content)

        logger.info(f"Saved report to {path}")

        return path

    def save_json(self, result: Dict[str, Any], security_level: str, text: str) -> str:
        """
        Save the validation result as JSON.

        Args:
            result (Dict[str, Any]): Validation result
            security_level (str): Security level used for validation
            text (str): The text that was validated

        Returns:
            str: Path to the saved JSON file
        """
        # Generate a filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        method = result.get("method", "unknown")
        is_secure = "secure" if result.get("is_secure", False) else "insecure"

        filename = f"validation_result_{security_level}_{method}_{is_secure}_{timestamp}.json"

        # Create the JSON data
        data = {
            "result": result,
            "security_level": security_level,
            "text": text,
            "timestamp": datetime.now().isoformat()
        }

        # Save the JSON
        path = os.path.join(self.output_dir, filename)
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

        logger.info(f"Saved JSON to {path}")

        return path
