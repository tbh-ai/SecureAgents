# Result Destination

The TBH Secure Agents framework provides a powerful feature to save operation and squad results to files in various formats. This document explains how to use the `result_destination` parameter to save results to files.

## Overview

The `result_destination` parameter allows you to specify where and how to save the results of operations and squads. This is useful for:

- Saving results for later analysis
- Creating reports in various formats
- Integrating with other systems
- Archiving results for compliance purposes

## Operation Result Destination

For individual operations, the `result_destination` parameter is a simple string specifying the file path where the result should be saved.

### Example

```python
from tbh_secure_agents import Expert, Operation

# Create an expert
expert = Expert(
    specialty="Content Creator",
    objective="Create high-quality content",
    api_key="your_api_key"
)

# Create an operation with result_destination
operation = Operation(
    instructions="Write a short paragraph about artificial intelligence.",
    expert=expert,
    result_destination="outputs/ai_paragraph.txt"
)

# Execute the operation
result = operation.execute()
```

### Supported File Extensions

The file extension determines the format of the saved file:

- `.txt`: Plain text format
- `.md` or `.markdown`: Markdown format
- `.html`: HTML format
- `.json`: JSON format
- `.csv`: CSV format
- `.pdf`: PDF format (requires the `reportlab` package)

## Squad Result Destination

For squads, the `result_destination` parameter is a dictionary that specifies the format and file path for the result.

### Example

```python
from tbh_secure_agents import Expert, Operation, Squad

# Create an expert
expert = Expert(
    specialty="Content Creator",
    objective="Create high-quality content",
    api_key="your_api_key"
)

# Create an operation
operation = Operation(
    instructions="Write a short paragraph about machine learning.",
    expert=expert
)

# Create a squad with result_destination
squad = Squad(
    experts=[expert],
    operations=[operation],
    process="sequential",
    security_level="standard",
    result_destination={
        "format": "md",
        "file_path": "outputs/squad_result.md"
    }
)

# Deploy the squad
result = squad.deploy()
```

### Result Destination Dictionary

The `result_destination` dictionary for squads has the following keys:

- `format`: The format of the output file. Supported values are:
  - `txt`: Plain text format
  - `md` or `markdown`: Markdown format
  - `html`: HTML format
  - `json`: JSON format
  - `csv`: CSV format
  - `pdf`: PDF format 
- `file_path`: The path where the file should be saved

## Output Format Details

### Text Format (`.txt`)

The text format includes:
- A header with operation/squad details
- Guardrail inputs (if any)
- The result

### Markdown Format (`.md` or `.markdown`)

The Markdown format includes:
- Formatted headers for operation/squad details
- Guardrail inputs as a list (if any)
- The result

### HTML Format (`.html`)

The HTML format includes:
- A styled HTML page with operation/squad details
- Guardrail inputs as a list (if any)
- The result with proper formatting

### JSON Format (`.json`)

The JSON format includes:
- Operation/squad details as JSON properties
- Execution metrics
- Guardrail inputs (if any)
- The result

### CSV Format (`.csv`)

The CSV format includes:
- A header row with column names
- A data row with operation/squad details and the result

### PDF Format (`.pdf`)

The PDF format includes:
- A professionally formatted PDF document with operation/squad details
- Guardrail inputs as a table (if any)
- The result with proper formatting

> Note: PDF format requires the `reportlab` package. If not installed, the result will be saved as a text file.

## Security Considerations

The `result_destination` parameter is subject to security checks to prevent potential security issues:

- File paths are validated to prevent path traversal attacks
- Suspicious file extensions (e.g., `.exe`, `.bat`, `.sh`, `.py`, `.js`, `.php`) are not allowed
- Directory creation is handled securely

## Example: Saving Results in Multiple Formats

```python
from tbh_secure_agents import Expert, Operation, Squad

# Create an expert
expert = Expert(
    specialty="Content Creator",
    objective="Create high-quality content",
    api_key="your_api_key"
)

# Create operations with different formats
txt_operation = Operation(
    instructions="Create content about renewable energy in TXT format.",
    expert=expert,
    result_destination="outputs/energy.txt"
)

md_operation = Operation(
    instructions="Create content about renewable energy in MD format.",
    expert=expert,
    result_destination="outputs/energy.md"
)

json_operation = Operation(
    instructions="Create content about renewable energy in JSON format.",
    expert=expert,
    result_destination="outputs/energy.json"
)

html_operation = Operation(
    instructions="Create content about renewable energy in HTML format.",
    expert=expert,
    result_destination="outputs/energy.html"
)

# Create a squad with all operations
squad = Squad(
    experts=[expert],
    operations=[txt_operation, md_operation, json_operation, html_operation],
    process="sequential",
    security_level="standard"
)

# Deploy the squad
result = squad.deploy()
```

## Best Practices

1. **Use the outputs Directory**: Store all generated files in the `outputs` directory or its subdirectories to keep your project organized.
   ```python
   # Create the outputs directory if it doesn't exist
   import os
   os.makedirs("outputs", exist_ok=True)

   # Use subdirectories for different types of outputs
   os.makedirs("outputs/reports", exist_ok=True)
   os.makedirs("outputs/data", exist_ok=True)
   ```

2. **Use Absolute Paths**: To avoid path resolution issues, use absolute paths for the `file_path` parameter.
   ```python
   import os

   # Get the absolute path to the outputs directory
   outputs_dir = os.path.abspath("outputs")

   # Create a file path using the absolute path
   file_path = os.path.join(outputs_dir, "report.md")
   ```

3. **Choose Appropriate Formats**: Select the format that best suits your needs:
   - Use `.txt` or `.md` for simple text output
   - Use `.html` for formatted output that can be viewed in a browser
   - Use `.json` for structured data that can be processed by other systems
   - Use `.pdf` for professional reports

4. **Handle Errors**: Check the return value of the operation or squad execution to ensure the result was saved successfully.
   ```python
   try:
       result = operation.execute()
       print(f"Result saved to {operation.result_destination}")
   except Exception as e:
       print(f"Error saving result: {e}")
   ```

5. **Use Meaningful File Names**: Use descriptive file names that include relevant information such as date, content type, or purpose.
   ```python
   import datetime

   # Generate a file name with the current date
   today = datetime.datetime.now().strftime("%Y-%m-%d")
   file_name = f"outputs/reports/energy_report_{today}.md"
   ```
