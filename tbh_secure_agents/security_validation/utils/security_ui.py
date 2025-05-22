"""
Security UI utilities.

This module provides UI utilities for security validation, including
progress indicators, error messages, and interactive fix suggestions.
"""

import sys
import time
import threading
from typing import Dict, Any, Optional, List, Callable

# ANSI color codes for terminal output
class Color:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'


class SecurityUI:
    """
    User interface for security validation.
    
    This class provides methods for displaying security validation progress,
    results, and interactive fix suggestions.
    """
    
    def __init__(self, use_colors: bool = True, interactive: bool = True):
        """
        Initialize the security UI.
        
        Args:
            use_colors (bool): Whether to use colors in terminal output
            interactive (bool): Whether to use interactive features
        """
        self.use_colors = use_colors
        self.interactive = interactive
        self.spinner_active = False
        self.spinner_thread = None
        
    def _colorize(self, text: str, color: str) -> str:
        """
        Add color to text if colors are enabled.
        
        Args:
            text (str): The text to colorize
            color (str): The color to use
            
        Returns:
            str: The colorized text
        """
        if self.use_colors:
            return f"{color}{text}{Color.RESET}"
        return text
        
    def _spinner_worker(self, text: str):
        """
        Display a spinner with text.
        
        Args:
            text (str): The text to display with the spinner
        """
        spinner_chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        i = 0
        while self.spinner_active:
            spinner = spinner_chars[i % len(spinner_chars)]
            sys.stdout.write(f"\r{self._colorize(spinner, Color.BRIGHT_BLUE)} {text}")
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1
        sys.stdout.write("\r" + " " * (len(text) + 2) + "\r")
        sys.stdout.flush()
        
    def start_spinner(self, text: str):
        """
        Start a spinner with text.
        
        Args:
            text (str): The text to display with the spinner
        """
        if not self.interactive:
            return
            
        self.spinner_active = True
        self.spinner_thread = threading.Thread(target=self._spinner_worker, args=(text,))
        self.spinner_thread.daemon = True
        self.spinner_thread.start()
        
    def stop_spinner(self, success: bool = True, text: Optional[str] = None):
        """
        Stop the spinner and display a result.
        
        Args:
            success (bool): Whether the operation was successful
            text (Optional[str]): The text to display after stopping the spinner
        """
        if not self.interactive:
            return
            
        self.spinner_active = False
        if self.spinner_thread:
            self.spinner_thread.join()
            
        if text:
            icon = "✓" if success else "✗"
            color = Color.GREEN if success else Color.RED
            print(f"{self._colorize(icon, color)} {text}")
            
    def show_validation_progress(self, validator_name: str, security_level: str):
        """
        Show validation progress.
        
        Args:
            validator_name (str): The name of the validator
            security_level (str): The security level
        """
        if not self.interactive:
            return
            
        validator_colors = {
            "regex": Color.BRIGHT_GREEN,
            "ml": Color.BRIGHT_YELLOW,
            "llm": Color.BRIGHT_MAGENTA,
            "hybrid": Color.BRIGHT_BLUE
        }
        
        color = validator_colors.get(validator_name.lower(), Color.RESET)
        self.start_spinner(f"Running {self._colorize(validator_name, color)} validation ({security_level} security level)")
        
    def show_validation_result(self, result: Dict[str, Any]):
        """
        Show validation result.
        
        Args:
            result (Dict[str, Any]): The validation result
        """
        if not self.interactive:
            return
            
        is_secure = result.get("is_secure", False)
        method = result.get("method", "unknown")
        
        if is_secure:
            self.stop_spinner(True, f"Validation passed ({method})")
        else:
            reason = result.get("reason", "Unknown reason")
            self.stop_spinner(False, f"Validation failed: {reason}")
            
            # Show more details
            self.show_validation_details(result)
            
    def show_validation_details(self, result: Dict[str, Any]):
        """
        Show detailed validation results.
        
        Args:
            result (Dict[str, Any]): The validation result
        """
        if not self.interactive:
            return
            
        print("\n" + self._colorize("Security Validation Details:", Color.BOLD))
        print("-" * 50)
        
        # Show method
        method = result.get("method", "unknown")
        print(f"Validation method: {self._colorize(method, Color.BRIGHT_BLUE)}")
        
        # Show confidence if available
        if "confidence" in result:
            confidence = result["confidence"] * 100
            confidence_color = Color.GREEN if confidence > 80 else Color.YELLOW if confidence > 50 else Color.RED
            print(f"Confidence: {self._colorize(f'{confidence:.1f}%', confidence_color)}")
            
        # Show threshold if available
        if "threshold" in result:
            threshold = result["threshold"] * 100
            print(f"Threshold: {threshold:.1f}%")
            
        # Show reason
        reason = result.get("reason", "Unknown reason")
        print(f"Reason: {self._colorize(reason, Color.RED)}")
        
        # Show matched pattern for regex
        if "matched_pattern" in result:
            print(f"Matched pattern: {self._colorize(result['matched_pattern'], Color.YELLOW)}")
            
        # Show matched text
        if "matched_text" in result:
            print(f"Matched text: {self._colorize(result['matched_text'], Color.RED)}")
            
        # Show highlighted text
        if "highlighted_text" in result:
            print("\nHighlighted text:")
            highlighted = result["highlighted_text"].replace(">>>", self._colorize("", Color.BG_RED)).replace("<<<", self._colorize("", Color.RESET))
            print(highlighted)
            
        # Show threats for ML
        if "threats" in result and result["threats"]:
            print("\nDetected threats:")
            for threat in result["threats"]:
                category = threat.get("category", "unknown")
                severity = threat.get("severity", "unknown")
                severity_color = Color.RED if severity == "high" else Color.YELLOW if severity == "medium" else Color.GREEN
                description = threat.get("description", "")
                print(f"- {category} ({self._colorize(severity, severity_color)}): {description}")
                
        # Show fix suggestion
        if "fix_suggestion" in result and result["fix_suggestion"]:
            print("\n" + self._colorize("Suggested fix:", Color.BRIGHT_GREEN))
            print(result["fix_suggestion"])
            
        # Show validation metrics
        if "validation_metrics" in result:
            metrics = result["validation_metrics"]
            print("\nValidation performance:")
            total_time = metrics.get("total_time", 0) * 1000  # Convert to ms
            print(f"Total time: {total_time:.2f}ms")
            
            if "methods_used" in metrics:
                methods = ", ".join(metrics["methods_used"])
                print(f"Methods used: {methods}")
                
            if "regex_time" in metrics:
                regex_time = metrics["regex_time"] * 1000  # Convert to ms
                print(f"Regex time: {regex_time:.2f}ms")
                
            if "ml_time" in metrics:
                ml_time = metrics["ml_time"] * 1000  # Convert to ms
                print(f"ML time: {ml_time:.2f}ms")
                
            if "llm_time" in metrics:
                llm_time = metrics["llm_time"] * 1000  # Convert to ms
                print(f"LLM time: {llm_time:.2f}ms")
                
        print("-" * 50)
        
    def show_security_level_info(self, security_level: str):
        """
        Show information about a security level.
        
        Args:
            security_level (str): The security level
        """
        if not self.interactive:
            return
            
        print("\n" + self._colorize(f"Security Level: {security_level.upper()}", Color.BOLD))
        print("-" * 50)
        
        if security_level == "minimal":
            print("✓ Basic security checks only")
            print("✓ Allows most operations to run")
            print("✓ Logs warnings but doesn't block execution")
            print("✗ Not recommended for production")
        elif security_level == "standard":
            print("✓ Balanced security and usability")
            print("✓ Uses regex and ML validation")
            print("✓ Blocks common security threats")
            print("✓ Recommended for most use cases")
        elif security_level == "high":
            print("✓ Enhanced security checks")
            print("✓ Uses regex, ML, and LLM validation")
            print("✓ Stricter thresholds for security checks")
            print("✓ Recommended for sensitive applications")
        elif security_level == "maximum":
            print("✓ Maximum security protection")
            print("✓ Uses all available validation methods")
            print("✓ Very strict thresholds for security checks")
            print("✓ May impact performance")
            print("✓ Recommended for critical applications")
            
        print("-" * 50)
        
    def ask_for_fix(self, result: Dict[str, Any]) -> bool:
        """
        Ask the user if they want to apply a suggested fix.
        
        Args:
            result (Dict[str, Any]): The validation result
            
        Returns:
            bool: Whether the user wants to apply the fix
        """
        if not self.interactive or "fix_suggestion" not in result or not result["fix_suggestion"]:
            return False
            
        print("\n" + self._colorize("Would you like to apply the suggested fix?", Color.BRIGHT_YELLOW))
        print("1. Yes")
        print("2. No")
        print("3. Show me more details first")
        
        choice = input("Enter your choice (1-3): ")
        
        if choice == "1":
            return True
        elif choice == "3":
            self.show_validation_details(result)
            return self.ask_for_fix(result)
            
        return False
