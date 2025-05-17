# tbh_secure_agents/terminal_ui.py
# Author: Saish (TBH.AI)

"""
Terminal UI module for TBH Secure Agents framework.

This module provides a polished, professional terminal output interface
for the framework, making the execution flow more visually appealing
and easier to follow.
"""

import sys
import time
import logging
import threading
from typing import Optional, Dict, Any, List, Tuple
from enum import Enum
import os

# Check if running in a terminal that supports colors
SUPPORTS_COLOR = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()

# ANSI color codes
class Color:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'

    # Foreground colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'

    # Bright foreground colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'

    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'

# Icons for different message types
class Icon:
    INFO = "•"
    SUCCESS = "✓"
    WARNING = "!"
    ERROR = "×"
    SECURITY = "•"
    EXPERT = "•"
    OPERATION = "•"
    SQUAD = "•"
    THINKING = "•"
    GUARDRAIL = "•"
    RESULT = "•"

class TerminalUI:
    """
    Terminal UI manager for TBH Secure Agents framework.

    This class provides methods for displaying polished, professional
    terminal output during framework execution.
    """

    def __init__(self, enable_animations: bool = True, color_mode: bool = True):
        """
        Initialize the Terminal UI manager.

        Args:
            enable_animations (bool): Whether to enable animated spinners and progress bars
            color_mode (bool): Whether to use colored output
        """
        self.enable_animations = enable_animations and SUPPORTS_COLOR
        self.color_mode = color_mode and SUPPORTS_COLOR
        self.spinner_active = False
        self.spinner_thread = None
        self.spinner_text = ""
        self.terminal_width = self._get_terminal_width()

        # Store active operations and experts for status tracking
        self.active_operations = {}
        self.active_experts = {}

    def _get_terminal_width(self) -> int:
        """Get the current terminal width."""
        try:
            return os.get_terminal_size().columns
        except (AttributeError, OSError):
            return 80

    def _apply_color(self, text: str, color: str) -> str:
        """Apply color to text if color mode is enabled."""
        if self.color_mode:
            return f"{color}{text}{Color.RESET}"
        return text

    def _format_time(self, seconds: float) -> str:
        """Format time in seconds to a human-readable string."""
        if seconds < 60:
            return f"{seconds:.1f}s"
        minutes, seconds = divmod(seconds, 60)
        if minutes < 60:
            return f"{int(minutes)}m {int(seconds)}s"
        hours, minutes = divmod(minutes, 60)
        return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"

    def _spinner_worker(self):
        """Worker thread for animated spinner."""
        spinner_chars = ["⠄", "⠆", "⠇", "⠋", "⠙", "⠸", "⠰", "⠠", "⠰", "⠸", "⠙", "⠋", "⠇", "⠆"]
        i = 0
        while self.spinner_active:
            spinner = spinner_chars[i % len(spinner_chars)]
            sys.stdout.write(f"\r{self._apply_color(spinner, Color.BRIGHT_BLUE)} {self.spinner_text}")
            sys.stdout.flush()
            time.sleep(0.08)
            i += 1
        sys.stdout.write("\r" + " " * (len(self.spinner_text) + 2) + "\r")
        sys.stdout.flush()

    def start_spinner(self, text: str):
        """Start an animated spinner with the given text."""
        if not self.enable_animations:
            print(f"{self._apply_color('•', Color.BRIGHT_BLUE)} {text}...")
            return

        self.spinner_text = text
        self.spinner_active = True
        self.spinner_thread = threading.Thread(target=self._spinner_worker)
        self.spinner_thread.daemon = True
        self.spinner_thread.start()

    def stop_spinner(self, success: bool = True, result_text: Optional[str] = None):
        """Stop the animated spinner and display result."""
        if not self.enable_animations:
            if result_text:
                icon = Icon.SUCCESS if success else Icon.ERROR
                color = Color.GREEN if success else Color.RED
                print(f"{self._apply_color(icon, color)} {result_text}")
            return

        self.spinner_active = False
        if self.spinner_thread:
            self.spinner_thread.join()

        if result_text:
            icon = Icon.SUCCESS if success else Icon.ERROR
            color = Color.GREEN if success else Color.RED
            print(f"{self._apply_color(icon, color)} {result_text}")

    def print_header(self, text: str):
        """Print a section header."""
        self.terminal_width = self._get_terminal_width()
        print()
        print(self._apply_color("┌" + "─" * (self.terminal_width - 2) + "┐", Color.BRIGHT_BLACK))
        padding = (self.terminal_width - len(text) - 4) // 2
        print(self._apply_color("│", Color.BRIGHT_BLACK) + " " * padding +
              self._apply_color(text, Color.BOLD + Color.BRIGHT_WHITE) +
              " " * (self.terminal_width - len(text) - padding - 4) +
              self._apply_color(" │", Color.BRIGHT_BLACK))
        print(self._apply_color("└" + "─" * (self.terminal_width - 2) + "┘", Color.BRIGHT_BLACK))

    def print_subheader(self, text: str):
        """Print a subsection header."""
        self.terminal_width = self._get_terminal_width()
        print()
        print(self._apply_color(text, Color.BOLD + Color.BRIGHT_WHITE))

    def print_expert_info(self, specialty: str, objective: str, security_profile: str):
        """Print information about an expert."""
        print(f"{self._apply_color(Icon.EXPERT, Color.CYAN)} {self._apply_color(specialty, Color.BOLD)}")
        print(f"  {self._apply_color('›', Color.BRIGHT_BLACK)} {objective}")
        print(f"  {self._apply_color('›', Color.BRIGHT_BLACK)} Security: {security_profile}")

    def print_operation_info(self, instructions: str, expert_specialty: str, result_destination: str = None):
        """Print information about an operation."""
        # Truncate and format instructions for better display
        formatted_instructions = instructions.replace('\n', ' ').strip()
        if len(formatted_instructions) > 80:
            formatted_instructions = formatted_instructions[:77] + "..."

        print(f"{self._apply_color(Icon.OPERATION, Color.MAGENTA)} {self._apply_color(formatted_instructions, Color.BOLD)}")
        print(f"  {self._apply_color('›', Color.BRIGHT_BLACK)} Expert: {expert_specialty}")

        if result_destination:
            # Get the file format from the extension
            file_format = os.path.splitext(result_destination)[1].upper().replace('.', '')
            if not file_format:
                file_format = "TXT"

            print(f"  {self._apply_color('›', Color.BRIGHT_BLACK)} Output: {os.path.basename(result_destination)} ({file_format})")

    def print_squad_info(self, expert_count: int, operation_count: int, process: str, security_level: str):
        """Print information about a squad."""
        print(f"{self._apply_color(Icon.SQUAD, Color.BLUE)} {self._apply_color('Squad Configuration', Color.BOLD)}")
        print(f"  {self._apply_color('›', Color.BRIGHT_BLACK)} {expert_count} experts, {operation_count} operations")
        print(f"  {self._apply_color('›', Color.BRIGHT_BLACK)} Process: {process}, Security: {security_level}")

    def print_guardrails_info(self, guardrails: Dict[str, Any]):
        """Print information about guardrails."""
        if not guardrails:
            return

        print(f"{self._apply_color(Icon.GUARDRAIL, Color.YELLOW)} {self._apply_color('Guardrails', Color.BOLD)}")

        # Format guardrails in a compact way
        guardrail_items = []
        for key, value in guardrails.items():
            # Format value for display
            if isinstance(value, str) and len(value) > 30:
                value_str = f"{value[:27]}..."
            elif isinstance(value, dict):
                value_str = f"<dict:{len(value)}>"
            elif isinstance(value, list):
                value_str = f"<list:{len(value)}>"
            else:
                value_str = str(value)

            guardrail_items.append(f"{key}={value_str}")

        # Print guardrails in a compact format
        items_per_line = 3
        for i in range(0, len(guardrail_items), items_per_line):
            line_items = guardrail_items[i:i+items_per_line]
            print(f"  {self._apply_color('›', Color.BRIGHT_BLACK)} {', '.join(line_items)}")

    def print_result(self, result: str, execution_time: float):
        """Print the final result of a squad execution."""
        # Format execution time
        time_str = self._format_time(execution_time)

        # Print a clean separator
        print("\n" + self._apply_color("─" * self.terminal_width, Color.BRIGHT_BLACK))

        # Print execution time in a subtle way
        print(f"{self._apply_color('Completed in', Color.BRIGHT_BLACK)} {self._apply_color(time_str, Color.BRIGHT_WHITE)}")

        # Print a clean separator
        print(self._apply_color("─" * self.terminal_width, Color.BRIGHT_BLACK) + "\n")

        # Print the result
        lines = result.split('\n')
        max_lines = 20  # Show at most 20 lines

        if len(lines) > max_lines:
            print('\n'.join(lines[:max_lines]))
            print(f"\n{self._apply_color(f'... {len(lines) - max_lines} more lines not shown', Color.BRIGHT_BLACK)}")
        else:
            print(result)

    def print_security_warning(self, message: str, suggestions: List[str] = None, details: str = None):
        """
        Print a security warning message with optional suggestions and details.

        Args:
            message (str): The security warning message to display
            suggestions (List[str], optional): A list of suggestions to help resolve the security issue
            details (str, optional): Additional details about the security issue
        """
        print(f"{self._apply_color('⚠️', Color.YELLOW)} {self._apply_color('SECURITY WARNING:', Color.YELLOW + Color.BOLD)} {message}")

        if details:
            # Print details with indentation
            print(f"  {self._apply_color('Details:', Color.BRIGHT_YELLOW)} {details}")

        if suggestions:
            # Print a separator before suggestions
            print(f"\n{self._apply_color('Recommended Actions:', Color.BRIGHT_YELLOW)}")

            # Print each suggestion with a bullet point
            for suggestion in suggestions:
                print(f"  {self._apply_color('•', Color.BRIGHT_YELLOW)} {suggestion}")

    def print_error(self, message: str, suggestions: List[str] = None):
        """
        Print an error message with optional suggestions.

        Args:
            message (str): The error message to display
            suggestions (List[str], optional): A list of suggestions to help resolve the error
        """
        print(f"{self._apply_color(Icon.ERROR, Color.RED)} {self._apply_color(message, Color.BOLD)}")

        if suggestions:
            # Print a separator before suggestions
            print(f"\n{self._apply_color('Suggestions:', Color.BRIGHT_YELLOW)}")

            # Print each suggestion with a bullet point
            for suggestion in suggestions:
                print(f"  {self._apply_color('•', Color.BRIGHT_YELLOW)} {suggestion}")

    def print_success(self, message: str):
        """Print a success message."""
        print(f"{self._apply_color(Icon.SUCCESS, Color.GREEN)} {message}")

    def print_info(self, message: str):
        """Print an informational message."""
        print(f"{self._apply_color(Icon.INFO, Color.BLUE)} {message}")

    def update_operation_status(self, operation_id: str, status: str, progress: float = 0.0):
        """Update the status of an operation."""
        self.active_operations[operation_id] = {
            'status': status,
            'progress': progress,
            'updated_at': time.time()
        }

    def update_expert_status(self, expert_id: str, status: str):
        """Update the status of an expert."""
        self.active_experts[expert_id] = {
            'status': status,
            'updated_at': time.time()
        }

# Create a global instance for use throughout the framework
terminal = TerminalUI()

# Custom logging handler that uses the TerminalUI
class TerminalUILogHandler(logging.Handler):
    """Custom logging handler that uses TerminalUI for output."""

    def emit(self, record):
        msg = self.format(record)

        # Skip certain verbose log messages to reduce clutter
        if "initialized with" in msg or "security components initialized" in msg:
            return

        if record.levelno >= logging.ERROR:
            # Check if this is a structured error message with suggestions
            if hasattr(record, 'suggestions') and record.suggestions:
                terminal.print_error(msg, record.suggestions)
            else:
                terminal.print_error(msg)
        elif record.levelno >= logging.WARNING:
            if "SECURITY WARNING" in msg:
                # Check if this is a structured security warning with suggestions and details
                if hasattr(record, 'suggestions') and record.suggestions:
                    details = record.details if hasattr(record, 'details') else None
                    terminal.print_security_warning(
                        msg.replace("⚠️ SECURITY WARNING: ", ""),
                        record.suggestions,
                        details
                    )
                else:
                    terminal.print_security_warning(msg.replace("⚠️ SECURITY WARNING: ", ""))
            else:
                print(f"{terminal._apply_color(Icon.WARNING, Color.YELLOW)} {msg}")
        elif record.levelno >= logging.INFO:
            # Only show important info messages
            if "starting" in msg or "finished" in msg or "completed" in msg:
                terminal.print_info(msg)
