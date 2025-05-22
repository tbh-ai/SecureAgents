"""
Visualization utilities for security validation.

This module provides utilities for visualizing the security validation process,
including validation flow diagrams and performance metrics.
"""

import os
import time
import logging
from typing import Dict, Any, List, Optional, Tuple, Union
import json

# Get a logger for this module
logger = logging.getLogger(__name__)


class ValidationVisualizer:
    """
    Visualizer for security validation.
    
    This class provides methods for visualizing the security validation process,
    including validation flow diagrams and performance metrics.
    """
    
    def __init__(self, output_dir: str = "validation_visualizations"):
        """
        Initialize the visualizer.
        
        Args:
            output_dir (str): Directory to save visualizations
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
    def visualize_validation_flow(self, result: Dict[str, Any], filename: Optional[str] = None) -> str:
        """
        Visualize the validation flow for a result.
        
        This method generates a Mermaid diagram of the validation flow and saves
        it to a file. The diagram shows the path taken through the validation
        process, including which validators were used and their results.
        
        Args:
            result (Dict[str, Any]): The validation result
            filename (Optional[str]): The filename to save the diagram to
            
        Returns:
            str: The path to the generated diagram
        """
        # Extract validation flow from result
        validation_flow = result.get("validation_flow", [])
        
        # If no validation flow, return early
        if not validation_flow:
            logger.warning("No validation flow found in result")
            return ""
            
        # Create a unique filename if none provided
        if filename is None:
            timestamp = int(time.time())
            filename = f"validation_flow_{timestamp}.md"
            
        # Ensure filename has .md extension
        if not filename.endswith(".md"):
            filename += ".md"
            
        # Create the full path
        filepath = os.path.join(self.output_dir, filename)
        
        # Create the Mermaid diagram
        mermaid_diagram = self._create_mermaid_flow_diagram(result)
        
        # Save the diagram to a file
        with open(filepath, "w") as f:
            f.write("# Validation Flow Diagram\n\n")
            f.write("```mermaid\n")
            f.write(mermaid_diagram)
            f.write("\n```\n\n")
            
            # Add validation details
            f.write("## Validation Details\n\n")
            f.write(f"- Security Level: {result.get('security_level', 'unknown')}\n")
            f.write(f"- Validation Method: {result.get('method', 'unknown')}\n")
            f.write(f"- Is Secure: {result.get('is_secure', False)}\n")
            
            # Add metrics if available
            if "validation_metrics" in result:
                metrics = result["validation_metrics"]
                f.write("\n## Validation Metrics\n\n")
                f.write(f"- Total Time: {metrics.get('total_time', 0) * 1000:.2f} ms\n")
                f.write(f"- Methods Used: {', '.join(metrics.get('methods_used', []))}\n")
                f.write(f"- Regex Time: {metrics.get('regex_time', 0) * 1000:.2f} ms\n")
                f.write(f"- ML Time: {metrics.get('ml_time', 0) * 1000:.2f} ms\n")
                f.write(f"- LLM Time: {metrics.get('llm_time', 0) * 1000:.2f} ms\n")
                
                # Add complexity info if available
                if "complexity_info" in metrics:
                    complexity = metrics["complexity_info"]
                    f.write("\n## Complexity Analysis\n\n")
                    f.write(f"- Is Complex: {complexity.get('is_complex', False)}\n")
                    f.write(f"- Complexity Score: {complexity.get('complexity_score', 0):.2f}\n")
                    f.write(f"- Patterns Detected: {', '.join(complexity.get('patterns_detected', []))}\n")
            
            # Add validation result
            if not result.get("is_secure", True):
                f.write("\n## Security Issues\n\n")
                f.write(f"- Reason: {result.get('reason', 'Unknown reason')}\n")
                
                # Add risks if available
                if "risks" in result:
                    f.write("\n### Detected Risks\n\n")
                    for i, risk in enumerate(result["risks"]):
                        f.write(f"#### Risk {i+1}: {risk.get('category', 'unknown')}\n\n")
                        f.write(f"- Severity: {risk.get('severity', 'unknown')}\n")
                        f.write(f"- Text: `{risk.get('text', 'unknown')}`\n")
                        f.write(f"- Explanation: {risk.get('explanation', 'unknown')}\n")
                        f.write(f"- Recommendation: {risk.get('recommendation', 'unknown')}\n")
                        
                # Add fix suggestion if available
                if "fix_suggestion" in result:
                    f.write("\n### Fix Suggestion\n\n")
                    f.write(f"```\n{result['fix_suggestion']}\n```\n")
        
        logger.info(f"Validation flow diagram saved to {filepath}")
        return filepath
        
    def _create_mermaid_flow_diagram(self, result: Dict[str, Any]) -> str:
        """
        Create a Mermaid flow diagram for the validation result.
        
        Args:
            result (Dict[str, Any]): The validation result
            
        Returns:
            str: The Mermaid diagram as a string
        """
        # Extract validation flow and metrics
        validation_flow = result.get("validation_flow", [])
        metrics = result.get("validation_metrics", {})
        is_secure = result.get("is_secure", True)
        
        # Create the diagram header
        diagram = "graph TD\n"
        
        # Add the input node
        diagram += "    Input[\"Input Text\"] --> Regex\n"
        
        # Add the regex node
        if "regex" in metrics.get("methods_used", []):
            regex_time = metrics.get("regex_time", 0) * 1000
            if "regex" == result.get("method", ""):
                if is_secure:
                    diagram += f"    Regex[\"Regex Validator<br>({regex_time:.2f} ms)\"] --> RegexPass[\"✅ Passed\"]\n"
                else:
                    diagram += f"    Regex[\"Regex Validator<br>({regex_time:.2f} ms)\"] --> RegexFail[\"❌ Failed\"]\n"
            else:
                diagram += f"    Regex[\"Regex Validator<br>({regex_time:.2f} ms)\"] --> ML\n"
        
        # Add the ML node
        if "ml" in metrics.get("methods_used", []):
            ml_time = metrics.get("ml_time", 0) * 1000
            if "ml" == result.get("method", ""):
                if is_secure:
                    diagram += f"    ML[\"ML Validator<br>({ml_time:.2f} ms)\"] --> MLPass[\"✅ Passed\"]\n"
                else:
                    diagram += f"    ML[\"ML Validator<br>({ml_time:.2f} ms)\"] --> MLFail[\"❌ Failed\"]\n"
            else:
                diagram += f"    ML[\"ML Validator<br>({ml_time:.2f} ms)\"] --> LLM\n"
        
        # Add the LLM node
        if "llm" in metrics.get("methods_used", []):
            llm_time = metrics.get("llm_time", 0) * 1000
            if is_secure:
                diagram += f"    LLM[\"LLM Validator<br>({llm_time:.2f} ms)\"] --> LLMPass[\"✅ Passed\"]\n"
            else:
                diagram += f"    LLM[\"LLM Validator<br>({llm_time:.2f} ms)\"] --> LLMFail[\"❌ Failed\"]\n"
        
        # Add styling
        diagram += "\n    %% Styling\n"
        diagram += "    classDef input fill:#f9f9f9,stroke:#333,stroke-width:2px;\n"
        diagram += "    classDef validator fill:#e1f5fe,stroke:#0288d1,stroke-width:2px;\n"
        diagram += "    classDef pass fill:#e8f5e9,stroke:#4caf50,stroke-width:2px;\n"
        diagram += "    classDef fail fill:#ffebee,stroke:#f44336,stroke-width:2px;\n"
        diagram += "    class Input input;\n"
        diagram += "    class Regex,ML,LLM validator;\n"
        diagram += "    class RegexPass,MLPass,LLMPass pass;\n"
        diagram += "    class RegexFail,MLFail,LLMFail fail;\n"
        
        return diagram
        
    def visualize_performance_metrics(self, results: List[Dict[str, Any]], filename: Optional[str] = None) -> str:
        """
        Visualize performance metrics for multiple validation results.
        
        This method generates a Markdown report with performance metrics for
        multiple validation results, including average times and method usage.
        
        Args:
            results (List[Dict[str, Any]]): The validation results
            filename (Optional[str]): The filename to save the report to
            
        Returns:
            str: The path to the generated report
        """
        # If no results, return early
        if not results:
            logger.warning("No results provided for performance visualization")
            return ""
            
        # Create a unique filename if none provided
        if filename is None:
            timestamp = int(time.time())
            filename = f"performance_metrics_{timestamp}.md"
            
        # Ensure filename has .md extension
        if not filename.endswith(".md"):
            filename += ".md"
            
        # Create the full path
        filepath = os.path.join(self.output_dir, filename)
        
        # Extract metrics from results
        total_times = []
        regex_times = []
        ml_times = []
        llm_times = []
        methods_used = {"regex": 0, "ml": 0, "llm": 0}
        security_levels = {"minimal": 0, "standard": 0, "high": 0, "maximum": 0}
        is_secure_count = 0
        
        for result in results:
            metrics = result.get("validation_metrics", {})
            
            # Add times
            if "total_time" in metrics:
                total_times.append(metrics["total_time"])
            if "regex_time" in metrics:
                regex_times.append(metrics["regex_time"])
            if "ml_time" in metrics:
                ml_times.append(metrics["ml_time"])
            if "llm_time" in metrics:
                llm_times.append(metrics["llm_time"])
                
            # Count methods used
            for method in metrics.get("methods_used", []):
                if method in methods_used:
                    methods_used[method] += 1
                    
            # Count security levels
            security_level = result.get("security_level", "standard")
            if security_level in security_levels:
                security_levels[security_level] += 1
                
            # Count secure results
            if result.get("is_secure", False):
                is_secure_count += 1
        
        # Calculate averages
        avg_total_time = sum(total_times) / len(total_times) if total_times else 0
        avg_regex_time = sum(regex_times) / len(regex_times) if regex_times else 0
        avg_ml_time = sum(ml_times) / len(ml_times) if ml_times else 0
        avg_llm_time = sum(llm_times) / len(llm_times) if llm_times else 0
        
        # Create the report
        with open(filepath, "w") as f:
            f.write("# Security Validation Performance Metrics\n\n")
            
            # Summary
            f.write("## Summary\n\n")
            f.write(f"- Total Validations: {len(results)}\n")
            f.write(f"- Secure Results: {is_secure_count} ({is_secure_count / len(results) * 100:.1f}%)\n")
            f.write(f"- Insecure Results: {len(results) - is_secure_count} ({(len(results) - is_secure_count) / len(results) * 100:.1f}%)\n")
            
            # Performance metrics
            f.write("\n## Performance Metrics\n\n")
            f.write(f"- Average Total Time: {avg_total_time * 1000:.2f} ms\n")
            f.write(f"- Average Regex Time: {avg_regex_time * 1000:.2f} ms\n")
            f.write(f"- Average ML Time: {avg_ml_time * 1000:.2f} ms\n")
            f.write(f"- Average LLM Time: {avg_llm_time * 1000:.2f} ms\n")
            
            # Methods used
            f.write("\n## Methods Used\n\n")
            f.write(f"- Regex: {methods_used['regex']} ({methods_used['regex'] / len(results) * 100:.1f}%)\n")
            f.write(f"- ML: {methods_used['ml']} ({methods_used['ml'] / len(results) * 100:.1f}%)\n")
            f.write(f"- LLM: {methods_used['llm']} ({methods_used['llm'] / len(results) * 100:.1f}%)\n")
            
            # Security levels
            f.write("\n## Security Levels\n\n")
            f.write(f"- Minimal: {security_levels['minimal']} ({security_levels['minimal'] / len(results) * 100:.1f}%)\n")
            f.write(f"- Standard: {security_levels['standard']} ({security_levels['standard'] / len(results) * 100:.1f}%)\n")
            f.write(f"- High: {security_levels['high']} ({security_levels['high'] / len(results) * 100:.1f}%)\n")
            f.write(f"- Maximum: {security_levels['maximum']} ({security_levels['maximum'] / len(results) * 100:.1f}%)\n")
            
            # Add Mermaid chart for methods used
            f.write("\n## Methods Used Chart\n\n")
            f.write("```mermaid\n")
            f.write("pie\n")
            f.write("    title Methods Used\n")
            f.write(f"    \"Regex\" : {methods_used['regex']}\n")
            f.write(f"    \"ML\" : {methods_used['ml']}\n")
            f.write(f"    \"LLM\" : {methods_used['llm']}\n")
            f.write("```\n")
            
            # Add Mermaid chart for security levels
            f.write("\n## Security Levels Chart\n\n")
            f.write("```mermaid\n")
            f.write("pie\n")
            f.write("    title Security Levels\n")
            f.write(f"    \"Minimal\" : {security_levels['minimal']}\n")
            f.write(f"    \"Standard\" : {security_levels['standard']}\n")
            f.write(f"    \"High\" : {security_levels['high']}\n")
            f.write(f"    \"Maximum\" : {security_levels['maximum']}\n")
            f.write("```\n")
            
            # Add Mermaid chart for secure vs. insecure
            f.write("\n## Secure vs. Insecure Chart\n\n")
            f.write("```mermaid\n")
            f.write("pie\n")
            f.write("    title Secure vs. Insecure\n")
            f.write(f"    \"Secure\" : {is_secure_count}\n")
            f.write(f"    \"Insecure\" : {len(results) - is_secure_count}\n")
            f.write("```\n")
        
        logger.info(f"Performance metrics report saved to {filepath}")
        return filepath
        
    def export_results_to_json(self, results: List[Dict[str, Any]], filename: Optional[str] = None) -> str:
        """
        Export validation results to a JSON file.
        
        Args:
            results (List[Dict[str, Any]]): The validation results
            filename (Optional[str]): The filename to save the results to
            
        Returns:
            str: The path to the generated file
        """
        # Create a unique filename if none provided
        if filename is None:
            timestamp = int(time.time())
            filename = f"validation_results_{timestamp}.json"
            
        # Ensure filename has .json extension
        if not filename.endswith(".json"):
            filename += ".json"
            
        # Create the full path
        filepath = os.path.join(self.output_dir, filename)
        
        # Save the results to a file
        with open(filepath, "w") as f:
            json.dump(results, f, indent=2)
            
        logger.info(f"Validation results saved to {filepath}")
        return filepath
