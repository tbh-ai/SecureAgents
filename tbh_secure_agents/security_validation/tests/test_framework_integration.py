#!/usr/bin/env python3
"""
Test framework integration with security validation.

This script simulates how the framework would use the security validation system
and tests if the hybrid approach works correctly when integrated.
"""

import os
import sys
import time
import json
import logging
import argparse
from typing import Dict, Any, List, Optional, Union, Callable

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from SecureAgents.tbh_secure_agents.security_validation.validators.hybrid_validator import HybridValidator
from SecureAgents.tbh_secure_agents.security_validation.validators.parallel_validator import ParallelValidator
from SecureAgents.tbh_secure_agents.security_validation.visualization.enhanced_visualizer import EnhancedVisualizer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Get a logger for this module
logger = logging.getLogger(__name__)


# Simulated framework components
class SimulatedTool:
    """Simulated tool for testing."""

    def __init__(self, name: str, description: str, is_secure: bool = True):
        """
        Initialize the simulated tool.

        Args:
            name (str): Tool name
            description (str): Tool description
            is_secure (bool): Whether the tool is secure
        """
        self.name = name
        self.description = description
        self.is_secure = is_secure

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "is_secure": self.is_secure
        }


class SimulatedContext:
    """Simulated context for testing."""

    def __init__(self, name: str, data: Dict[str, Any], security_level: str = "standard"):
        """
        Initialize the simulated context.

        Args:
            name (str): Context name
            data (Dict[str, Any]): Context data
            security_level (str): Security level
        """
        self.name = name
        self.data = data
        self.security_level = security_level

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "data": self.data,
            "security_level": self.security_level
        }


class SimulatedMemory:
    """Simulated memory for testing."""

    def __init__(self, name: str, content: Dict[str, Any]):
        """
        Initialize the simulated memory.

        Args:
            name (str): Memory name
            content (Dict[str, Any]): Memory content
        """
        self.name = name
        self.content = content

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "content": self.content
        }


class SimulatedFramework:
    """Simulated framework for testing."""

    def __init__(self, validator_type: str = "parallel", api_key: Optional[str] = None):
        """
        Initialize the simulated framework.

        Args:
            validator_type (str): Type of validator to use (hybrid or parallel)
            api_key (Optional[str]): API key for the LLM service
        """
        # Use environment variables if not provided
        api_key = api_key or os.environ.get("OPENAI_API_KEY")

        # Initialize the validator
        if validator_type == "hybrid":
            self.validator = HybridValidator(api_key=api_key)
            logger.info("Using HybridValidator")
        else:
            self.validator = ParallelValidator(api_key=api_key)
            logger.info("Using ParallelValidator")

        # Initialize the visualizer
        self.visualizer = EnhancedVisualizer(
            output_dir="framework_integration_results",
            auto_save=False,  # Don't auto-save reports
            max_reports=100,  # Keep up to 100 reports in memory
            retention_days=7  # Keep reports for 7 days
        )

        # Initialize tools, contexts, and memories
        self.tools = {}
        self.contexts = {}
        self.memories = {}

        # Initialize security levels
        self.security_levels = ["minimal", "standard", "high", "maximum"]

        logger.info("Initialized simulated framework")

    def register_tool(self, tool: SimulatedTool) -> None:
        """
        Register a tool.

        Args:
            tool (SimulatedTool): Tool to register
        """
        self.tools[tool.name] = tool
        logger.info(f"Registered tool: {tool.name}")

    def register_context(self, context: SimulatedContext) -> None:
        """
        Register a context.

        Args:
            context (SimulatedContext): Context to register
        """
        self.contexts[context.name] = context
        logger.info(f"Registered context: {context.name}")

    def register_memory(self, memory: SimulatedMemory) -> None:
        """
        Register a memory.

        Args:
            memory (SimulatedMemory): Memory to register
        """
        self.memories[memory.name] = memory
        logger.info(f"Registered memory: {memory.name}")

    def validate_tool_call(self, tool_name: str, args: Dict[str, Any], context_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Validate a tool call.

        Args:
            tool_name (str): Tool name
            args (Dict[str, Any]): Tool arguments
            context_name (Optional[str]): Context name

        Returns:
            Dict[str, Any]: Validation result
        """
        # Check if the tool exists
        if tool_name not in self.tools:
            return {
                "is_secure": False,
                "method": "framework",
                "reason": f"Unknown tool: {tool_name}"
            }

        # Get the tool
        tool = self.tools[tool_name]

        # Get the context
        context = self.contexts.get(context_name) if context_name else None

        # Create the text to validate
        text = f"Tool call: {tool_name}\nArguments: {json.dumps(args, indent=2)}"

        # Create the validation context
        validation_context = {
            "security_level": context.security_level if context else "standard",
            "tool_info": tool.to_dict(),
            "context_info": context.to_dict() if context else {}
        }

        # Validate the tool call
        result = self.validator.validate(text, validation_context)

        # Store the validation result in memory
        report_metadata = self.visualizer.store_report(
            result,
            validation_context["security_level"],
            text
        )

        # Add report metadata to the result
        result["report_id"] = report_metadata["id"]

        return result

    def validate_memory_operation(self, memory_name: str, operation: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate a memory operation.

        Args:
            memory_name (str): Memory name
            operation (str): Operation (read, write, delete)
            data (Dict[str, Any]): Operation data

        Returns:
            Dict[str, Any]: Validation result
        """
        # Check if the memory exists
        if memory_name not in self.memories:
            return {
                "is_secure": False,
                "method": "framework",
                "reason": f"Unknown memory: {memory_name}"
            }

        # Get the memory
        memory = self.memories[memory_name]

        # Create the text to validate
        text = f"Memory operation: {operation}\nMemory: {memory_name}\nData: {json.dumps(data, indent=2)}"

        # Create the validation context
        validation_context = {
            "security_level": "high",  # Memory operations are sensitive
            "memory_info": memory.to_dict(),
            "operation": operation
        }

        # Validate the memory operation
        result = self.validator.validate(text, validation_context)

        # Store the validation result in memory
        report_metadata = self.visualizer.store_report(
            result,
            validation_context["security_level"],
            text
        )

        # Add report metadata to the result
        result["report_id"] = report_metadata["id"]

        return result

    def validate_context_operation(self, context_name: str, operation: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate a context operation.

        Args:
            context_name (str): Context name
            operation (str): Operation (read, write, delete)
            data (Dict[str, Any]): Operation data

        Returns:
            Dict[str, Any]: Validation result
        """
        # Check if the context exists
        if context_name not in self.contexts:
            return {
                "is_secure": False,
                "method": "framework",
                "reason": f"Unknown context: {context_name}"
            }

        # Get the context
        context = self.contexts[context_name]

        # Create the text to validate
        text = f"Context operation: {operation}\nContext: {context_name}\nData: {json.dumps(data, indent=2)}"

        # Create the validation context
        validation_context = {
            "security_level": context.security_level,
            "context_info": context.to_dict(),
            "operation": operation
        }

        # Validate the context operation
        result = self.validator.validate(text, validation_context)

        # Store the validation result in memory
        report_metadata = self.visualizer.store_report(
            result,
            validation_context["security_level"],
            text
        )

        # Add report metadata to the result
        result["report_id"] = report_metadata["id"]

        return result


# Test cases for framework integration
def test_framework_integration(validator_type: str = "parallel") -> None:
    """
    Test framework integration with security validation.

    Args:
        validator_type (str): Type of validator to use (hybrid or parallel)
    """
    # Initialize the framework
    framework = SimulatedFramework(validator_type=validator_type)

    # Register tools
    framework.register_tool(SimulatedTool(
        name="file_reader",
        description="Read a file from the filesystem",
        is_secure=True
    ))

    framework.register_tool(SimulatedTool(
        name="system_command",
        description="Execute a system command",
        is_secure=False
    ))

    framework.register_tool(SimulatedTool(
        name="data_processor",
        description="Process data",
        is_secure=True
    ))

    # Register contexts
    framework.register_context(SimulatedContext(
        name="user_context",
        data={"user_id": "123", "role": "user"},
        security_level="standard"
    ))

    framework.register_context(SimulatedContext(
        name="admin_context",
        data={"user_id": "456", "role": "admin"},
        security_level="high"
    ))

    framework.register_context(SimulatedContext(
        name="system_context",
        data={"system_id": "789", "role": "system"},
        security_level="maximum"
    ))

    # Register memories
    framework.register_memory(SimulatedMemory(
        name="user_memory",
        content={"preferences": {"theme": "dark"}}
    ))

    framework.register_memory(SimulatedMemory(
        name="system_memory",
        content={"settings": {"debug": False}}
    ))

    # Test tool calls
    logger.info("\n\nTesting tool calls")
    logger.info("=" * 80)

    # Test secure tool call
    logger.info("\nTesting secure tool call")
    logger.info("-" * 50)

    result = framework.validate_tool_call(
        tool_name="file_reader",
        args={"path": "/tmp/data.txt"},
        context_name="user_context"
    )

    logger.info(f"Result: {'✅ Secure' if result.get('is_secure', False) else '❌ Insecure'}")
    logger.info(f"Method: {result.get('method', 'unknown')}")
    if "reason" in result:
        logger.info(f"Reason: {result['reason']}")

    # Test insecure tool call
    logger.info("\nTesting insecure tool call")
    logger.info("-" * 50)

    result = framework.validate_tool_call(
        tool_name="system_command",
        args={"command": "rm -rf /tmp/data"},
        context_name="admin_context"
    )

    logger.info(f"Result: {'✅ Secure' if result.get('is_secure', False) else '❌ Insecure'}")
    logger.info(f"Method: {result.get('method', 'unknown')}")
    if "reason" in result:
        logger.info(f"Reason: {result['reason']}")

    # Test memory operations
    logger.info("\n\nTesting memory operations")
    logger.info("=" * 80)

    # Test secure memory operation
    logger.info("\nTesting secure memory operation")
    logger.info("-" * 50)

    result = framework.validate_memory_operation(
        memory_name="user_memory",
        operation="read",
        data={"key": "preferences"}
    )

    logger.info(f"Result: {'✅ Secure' if result.get('is_secure', False) else '❌ Insecure'}")
    logger.info(f"Method: {result.get('method', 'unknown')}")
    if "reason" in result:
        logger.info(f"Reason: {result['reason']}")

    # Test insecure memory operation
    logger.info("\nTesting insecure memory operation")
    logger.info("-" * 50)

    result = framework.validate_memory_operation(
        memory_name="system_memory",
        operation="write",
        data={"key": "settings", "value": {"debug": True, "admin_password": "password123"}}
    )

    logger.info(f"Result: {'✅ Secure' if result.get('is_secure', False) else '❌ Insecure'}")
    logger.info(f"Method: {result.get('method', 'unknown')}")
    if "reason" in result:
        logger.info(f"Reason: {result['reason']}")

    # Test context operations
    logger.info("\n\nTesting context operations")
    logger.info("=" * 80)

    # Test secure context operation
    logger.info("\nTesting secure context operation")
    logger.info("-" * 50)

    result = framework.validate_context_operation(
        context_name="user_context",
        operation="read",
        data={"key": "user_id"}
    )

    logger.info(f"Result: {'✅ Secure' if result.get('is_secure', False) else '❌ Insecure'}")
    logger.info(f"Method: {result.get('method', 'unknown')}")
    if "reason" in result:
        logger.info(f"Reason: {result['reason']}")

    # Test insecure context operation
    logger.info("\nTesting insecure context operation")
    logger.info("-" * 50)

    result = framework.validate_context_operation(
        context_name="system_context",
        operation="write",
        data={"key": "role", "value": "super_admin"}
    )

    logger.info(f"Result: {'✅ Secure' if result.get('is_secure', False) else '❌ Insecure'}")
    logger.info(f"Method: {result.get('method', 'unknown')}")
    if "reason" in result:
        logger.info(f"Reason: {result['reason']}")

    logger.info("\n\nAll tests completed")

    # Display report summary
    logger.info("\n\nValidation Report Summary")
    logger.info("=" * 80)

    recent_reports = framework.visualizer.get_recent_reports()

    for i, report in enumerate(recent_reports):
        logger.info(f"\nReport {i+1}: {report['id']}")
        logger.info(f"Security Level: {report['security_level']}")
        logger.info(f"Method: {report['method']}")
        logger.info(f"Result: {'✅ Secure' if report['is_secure'] else '❌ Insecure'}")

        # Save the report to disk for viewing
        path = framework.visualizer.save_report(
            report['result'],
            report['security_level'],
            report['text'],
            format="html"
        )

        logger.info(f"Report saved to: {path}")

    logger.info("\nTo view a report, open the HTML file in a web browser.")


def main():
    """Main function."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Test framework integration with security validation")
    parser.add_argument("--validator", choices=["hybrid", "parallel"], default="parallel",
                        help="Type of validator to use")
    args = parser.parse_args()

    # Test framework integration
    test_framework_integration(args.validator)


if __name__ == "__main__":
    main()
