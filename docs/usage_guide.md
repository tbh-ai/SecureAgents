# Usage Guide

![TBH Secure Agents Logo](./assets/logo.png)

This guide explains the core concepts of `tbh_secure_agents` and how to use them to build your multi-agent system.

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
        result_destination='research_findings.md' # Save result to a markdown file
    )

    operation2 = Operation(
        instructions='Based on the research findings, write a concise 2-paragraph summary for a non-technical audience.',
        output_format='A short summary explaining the vulnerabilities simply.',
        expert=writer, # Assign expert
        result_destination='executive_summary.html' # Save result to an HTML file
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
            "file_path": "output/squad_result.json"
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

Refer to the example scripts provided in the repository (e.g., `example_usage.py`, `example_usage_2.py`) for practical demonstrations of these concepts. The first example (`example_usage.py`) implements the Researcher/Writer scenario described above.

## Advanced Features

### Guardrails

Guardrails provide a way to pass dynamic inputs to your Squad during deployment. These inputs can be used to guide the experts' responses, enforce constraints, and provide additional context without modifying your core operations.

```python
# Define guardrail inputs
guardrails = {
    "topic": "AI ethics",
    "tone": "balanced",
    "include_examples": True,
    "max_length": 1000
}

# Deploy with guardrails
result = squad.deploy(guardrails=guardrails)
```

For more details on using guardrails, see the [Guardrails Guide](./guardrails_guide.md).

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
    result_destination="reports/renewable_energy_report.md"
)

# Create an operation that saves its result as JSON data
data_operation = Operation(
    instructions="Analyze the energy consumption data and provide key metrics.",
    output_format="A JSON object with analysis results",
    expert=data_analyst,
    result_destination="data/energy_analysis.json"
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
        "file_path": "output/energy_analysis_result.json"
    }
)

# Create a squad that saves its final result to a PDF file
report_squad = Squad(
    experts=[researcher, writer],
    operations=[research_operation, writing_operation],
    process="sequential",
    result_destination={
        "format": "pdf",
        "file_path": "reports/final_report.pdf"
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

*   Explore implementing custom security profiles.
*   Investigate adding tools to experts.
*   Experiment with different expert roles and operation sequences.
*   Try using guardrails to dynamically control expert behavior.
*   Use the result_destination parameter to save operation and squad results to files.
*   Refer to the `security_features_comprehensive.md` document for details on the framework's security approach.
