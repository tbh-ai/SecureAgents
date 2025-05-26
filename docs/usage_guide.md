# TBH Secure Agents Usage Guide

![TBH Secure Agents Logo](./assets/logo.png)

This guide explains the core concepts of `tbh_secure_agents` and how to use them to build secure multi-agent systems.

## Table of Contents

1. [Core Concepts](#core-concepts)
2. [Basic Workflow](#basic-workflow)
3. [Example](#example)
4. [Advanced Features](#advanced-features)
   - [Guardrails](#guardrails)
   - [Result Destination](#result-destination)
   - [Security Profiles](#security-profiles)
5. [Next Steps](#next-steps)

## Quick Start

```bash
# Install the package
pip install tbh-secure-agents

# Set your API key as an environment variable (recommended)
export GOOGLE_API_KEY="your-api-key"
```

## Core Concepts

The framework revolves around three main components:

1.  **`Expert`**: Represents an autonomous entity designed to perform specific operations. Each expert has:
    *   A `specialty` (e.g., 'Researcher', 'Writer').
    *   An `objective` defining its primary purpose.
    *   A `background` providing context (optional).
    *   An underlying Large Language Model (LLM), defaulting to Google Gemini (`gemini-2.0-flash-lite`).
    *   A `security_profile` (placeholder for future security configurations).
    *   Optionally, a list of `tools` it can use (feature planned).

2.  **`Operation`**: Defines a unit of work to be performed by an expert. Each operation has:
    *   `instructions` clearly stating what needs to be done.
    *   An `output_format` describing the desired result format (optional).
    *   An assigned `expert` responsible for executing it.
    *   Optional `context` providing necessary background information.
    *   Optional `result_destination` specifying a file path where the operation result should be saved (supports various formats including .txt, .md, .csv, .json, .html, and .pdf).

3.  **`Squad`**: Manages a group of experts and orchestrates the execution of a list of operations. Key aspects include:
    *   A list of `experts`.
    *   A list of `operations`.
    *   A `process` defining the execution flow (currently supports 'sequential', where operations run one after another, passing results as context).
    *   Optional `result_destination` dictionary specifying the format and file path where the squad's final result should be saved (supports various formats including txt, md, csv, json, html, and pdf).

## Basic Workflow

Building an application with `tbh_secure_agents` typically involves these steps:

1.  **Import necessary classes:**
    ```python
    from tbh_secure_agents import Expert, Operation, Squad
    ```

2.  **Define your Experts:** Create instances of the `Expert` class, specifying their specialty, objective, and any other relevant parameters. Remember to handle API key configuration securely (preferably via the `GOOGLE_API_KEY` environment variable).
    ```python
    # Ensure GOOGLE_API_KEY is set in your environment
    # OR pass api_key='YOUR_KEY' for testing only (insecure)

    researcher = Expert(
        specialty='Senior Security Researcher',
        objective='Find the latest information on AI security vulnerabilities',
        background='An expert in cybersecurity with a focus on AI systems.'
        # api_key=YOUR_API_KEY # Testing only
    )

    writer = Expert(
        specialty='Technical Writer',
        objective='Summarize complex security information into concise reports',
        background='Skilled in communicating technical details clearly.'
        # api_key=YOUR_API_KEY # Testing only
    )
    ```

3.  **Define your Operations:** Create instances of the `Operation` class, providing clear instructions and assigning the appropriate expert. Optionally, specify a `result_destination` to automatically save the operation result to a file.
    ```python
    operation1 = Operation(
        instructions='Research and identify the top 3 AI security vulnerabilities reported in the last month.',
        output_format='A list of the top 3 vulnerabilities with brief descriptions.',
        expert=researcher, # Assign expert
        result_destination='outputs/research_findings.md' # Save result to a markdown file
    )

    operation2 = Operation(
        instructions='Based on the research findings, write a concise 2-paragraph summary for a non-technical audience.',
        output_format='A short summary explaining the vulnerabilities simply.',
        expert=writer, # Assign expert
        result_destination='outputs/executive_summary.html' # Save result to an HTML file
        # Context will be passed automatically by the Squad in sequential mode
    )
    ```

4.  **Assemble the Squad:** Create an instance of the `Squad` class, passing in the list of experts and operations. Specify the execution process (e.g., 'sequential') and optionally a result_destination.
    ```python
    security_squad = Squad(
        experts=[researcher, writer],
        operations=[operation1, operation2],
        process='sequential',
        result_destination={
            "format": "json",
            "file_path": "outputs/squad_result.json"
        }
    )
    ```

5.  **Define Guardrails (Optional):** Create a dictionary of guardrail inputs to guide the experts' behavior during execution.
    ```python
    guardrails = {
        "time_period": "last 30 days",
        "focus_area": "large language models",
        "audience": "executive leadership",
        "max_length": 500
    }
    ```

6.  **Deploy the Squad:** Call the `deploy()` method on your `Squad` instance, optionally passing guardrails, to start the execution.
    ```python
    try:
        # Deploy with guardrails
        result = security_squad.deploy(guardrails=guardrails)

        # Or deploy without guardrails
        # result = security_squad.deploy()

        print("Squad finished successfully!")
        print("\nFinal Result:")
        print(result)
    except Exception as e:
        print(f"An error occurred during squad execution: {e}")
    ```

## Example

The TBH Secure Agents framework includes a variety of examples in the `examples/` directory. Here's a simple example that demonstrates the core concepts:

```python
from tbh_secure_agents import Expert, Operation, Squad
import os

# Create outputs directory
os.makedirs("outputs/examples", exist_ok=True)

# Define experts with specific specialties
researcher = Expert(
    specialty="Security Researcher",
    objective="Research security vulnerabilities",
    security_profile="standard"
)

writer = Expert(
    specialty="Technical Writer",
    objective="Create clear documentation",
    security_profile="standard"
)

# Define operations with clear instructions
research_operation = Operation(
    instructions="Identify the top 3 security vulnerabilities in LLM applications",
    output_format="A numbered list with brief descriptions",
    expert=researcher,
    result_destination="outputs/examples/vulnerabilities.md"
)

summary_operation = Operation(
    instructions="Create a non-technical summary of the security vulnerabilities",
    output_format="A concise summary for executives",
    expert=writer,
    result_destination="outputs/examples/executive_summary.html"
)

# Create a squad to orchestrate the operations
security_squad = Squad(
    experts=[researcher, writer],
    operations=[research_operation, summary_operation],
    process="sequential",
    result_destination={
        "format": "json",
        "file_path": "outputs/examples/security_report.json"
    }
)

# Deploy the squad
result = security_squad.deploy()
print(f"Squad execution complete. Results saved to outputs/examples directory.")
```

For more examples, check the `examples/` directory in the repository:
- `examples/user_friendly/` - **NEW!** 5 simple, diverse AI agent examples (Researcher, Developer, Analyst, Strategist, Advisor)
- `examples/basic/` - Simple examples demonstrating core functionality
- `examples/advanced/` - More complex examples showcasing advanced features
- `examples/security/` - Examples focused on security features

### User-Friendly Examples

The `examples/user_friendly/` directory contains 5 ready-to-run examples that demonstrate different types of AI agents:

1. **AI Researcher** - Research any topic and save to markdown
2. **AI Code Developer** - Write code with specific requirements
3. **AI Business Analyst** - Analyze business problems and strategies
4. **AI Marketing Strategist** - Create marketing campaigns and strategies
5. **AI Financial Advisor** - Provide investment and financial advice

Each example demonstrates:
- Proper use of guardrails with template variables
- Different file formats (.md, .py, .json, .html, .pdf)
- Minimal security settings for easy learning
- Clean, simple code without fancy output

To run any example:
```bash
cd examples/user_friendly/
python3 1_ai_researcher.py
```

## Advanced Features

### Security Profiles

Security profiles are a key feature of the TBH Secure Agents framework, providing different levels of security validation for different use cases:

```python
# Create an expert with minimal security for development
dev_expert = Expert(
    specialty="Developer",
    objective="Write code",
    security_profile="minimal"  # For development and testing
)

# Create an expert with standard security (default)
standard_expert = Expert(
    specialty="Research Assistant",
    objective="Gather information"
    # security_profile defaults to "standard" if not specified
)

# Create an expert with high security for sensitive tasks
secure_expert = Expert(
    specialty="Financial Analyst",
    objective="Process financial data",
    security_profile="high"  # For sensitive applications
)
```

Available security profiles:

| Profile | Value | Description | Use Case |
|---------|-------|-------------|----------|
| **Minimal** | `"minimal"` | Only critical security checks | Development and testing |
| **Standard** | `"standard"` | Balanced security (default) | General purpose applications |
| **High** | `"high"` | Strict security validation | Sensitive applications |
| **Maximum** | `"maximum"` | Most stringent security | Highly sensitive applications |

For more details on security profiles, see the [Security Profiles Guide](./security_profiles_guide.md).

### Guardrails

Guardrails provide a powerful way to pass dynamic inputs to your operations using template variables. These inputs can be used to guide the experts' responses, enforce constraints, and provide additional context without modifying your core operations.

#### Template Variables in Expert Profiles

```python
# Expert with template variables
researcher = Expert(
    specialty="AI Researcher specializing in {research_topic}",
    objective="Research {research_topic} and provide {research_depth} information",
    security_profile="minimal"
)
```

#### Template Variables in Operation Instructions

```python
# Operation with template variables
research_operation = Operation(
    instructions="Research the latest developments in {research_topic}. Focus on {focus_areas}. Use a {tone} tone and provide {research_depth} analysis.",
    output_format="A {research_depth} research report with clear sections and bullet points",
    expert=researcher,
    result_destination="outputs/research_report.md"
)
```

#### Guardrails Dictionary

```python
# Define guardrail inputs that fill the template variables
guardrails = {
    "research_topic": "renewable energy technology",
    "research_depth": "comprehensive",
    "focus_areas": "innovations, market trends, future outlook",
    "tone": "professional"
}

# Execute with guardrails (for individual operations)
result = research_operation.execute(guardrails=guardrails)

# Or deploy with guardrails (for squads)
result = squad.deploy(guardrails=guardrails)
```

For more details on using guardrails, see the [Guardrails Guide](./guardrails_comprehensive.md).

### Result Destination

The `result_destination` parameter allows you to automatically save operation and squad results to files in various formats. This eliminates the need for separate file-saving code after deployment.

#### Operation Result Destination

For individual operations, the `result_destination` parameter is a simple string specifying the file path where the result should be saved:

```python
# Create an operation that saves its result to a markdown file
report_operation = Operation(
    instructions="Create a comprehensive report on renewable energy technologies.",
    output_format="A detailed report with sections and subsections",
    expert=energy_expert,
    result_destination="outputs/reports/renewable_energy_report.md"
)

# Create an operation that saves its result as JSON data
data_operation = Operation(
    instructions="Analyze the energy consumption data and provide key metrics.",
    output_format="A JSON object with analysis results",
    expert=data_analyst,
    result_destination="outputs/data/energy_analysis.json"
)
```

#### Squad Result Destination

For squads, the `result_destination` parameter is a dictionary that specifies the format and file path for the result:

```python
# Create a squad that saves its final result to a JSON file
analysis_squad = Squad(
    experts=[energy_expert, data_analyst],
    operations=[report_operation, data_operation],
    process="sequential",
    result_destination={
        "format": "json",
        "file_path": "outputs/energy_analysis_result.json"
    }
)

# Create a squad that saves its final result to a PDF file
report_squad = Squad(
    experts=[researcher, writer],
    operations=[research_operation, writing_operation],
    process="sequential",
    result_destination={
        "format": "pdf",
        "file_path": "outputs/reports/final_report.pdf"
    }
)
```

#### Supported File Formats

Both operations and squads support the following file formats:

- Text files (.txt)
- Markdown files (.md, .markdown)
- CSV files (.csv)
- JSON files (.json)
- HTML files (.html)
- PDF files (.pdf) - requires the reportlab package

The saved files include metadata such as operation/squad details, execution time, and guardrail inputs used during execution.

For more details on using the result destination feature, see the [Result Destination Guide](./result_destination.md).

## Next Steps

Now that you understand the basics of the TBH Secure Agents framework, here are some next steps to explore:

### Explore Advanced Security Features

* Read the [Security Profiles Guide](./security_profiles_guide.md) to learn about different security levels
* Check the [Security Guide](./security_guide.md) for best practices and advanced security configuration
* Explore the [Hybrid Security Validation](./hybrid_security_validation.md) system for enhanced security [BETA]
* Try the security visualization features for beautiful HTML reports [BETA]
* Implement custom security profiles for your specific security requirements

### Experiment with Different Configurations

* Try different expert roles and specialties
* Experiment with various operation sequences
* Test different security profiles to find the right balance for your use case

### Explore Example Code

* Check the `examples/` directory for complete working examples:
  * `examples/basic/` - Simple examples demonstrating core functionality
  * `examples/advanced/` - More complex examples showcasing advanced features
  * `examples/security/` - Examples focused on security features

### Integrate with Your Projects

* Use the framework in your own projects
* Implement custom tools for your experts
* Create domain-specific experts for your use cases

For more detailed information on specific topics, refer to the other documentation files in the `docs/` directory.
