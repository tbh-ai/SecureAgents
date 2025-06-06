# Installation

<img width="618" alt="Main" src="https://github.com/user-attachments/assets/dbbf5a4f-7b0b-4f43-9b37-ef77dc761ff1" />

This guide explains how to install the `tbh_secure_agents` package.

## Prerequisites

*   **Python:** Ensure you have Python installed (version 3.8 or higher is recommended). You can download it from [python.org](https://www.python.org/).
*   **pip:** The Python package installer (`pip`) is usually included with Python installations. Ensure it's up-to-date:
    ```bash
    python -m pip install --upgrade pip
    ```

## Installation from PyPI (Recommended)

The package is published to the Python Package Index (PyPI) and can be installed directly using pip:

```bash
pip install tbh-secure-agents
```

Note that the package name uses hyphens (`tbh-secure-agents`) rather than underscores when installing with pip.

This is a open-source package with proprietary security implementations. The installation provides you with the necessary interfaces to build secure multi-agent systems without exposing the internal security mechanisms.

## Source Code Access

This package is distributed as a open-source solution to protect the proprietary security mechanisms and intellectual property. The source code is not publicly available for direct installation or modification.

If you're interested in contributing to the project or need access to the source code for specific use cases, please contact the maintainers at saish.shinde.jb@gmail.com for more information about partnership opportunities.

## Verifying Installation

After installation, you can verify it by trying to import the package in a Python interpreter:

```python
import tbh_secure_agents
print(tbh_secure_agents.__version__)
```

If this runs without errors and prints the version number, the installation was successful.

## API Key Configuration

`tbh_secure_agents` uses Google Gemini as its default LLM, which requires an API key.

### Getting a Google API Key

1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Click "Get API Key"
4. Create a new API key or use an existing one
5. Copy the API key for use in your application

### Setting Up the API Key

**Recommended Method:** Set the `GOOGLE_API_KEY` environment variable:

```bash
# Linux/macOS
export GOOGLE_API_KEY='your_actual_api_key_here'

# Windows CMD
set GOOGLE_API_KEY=your_actual_api_key_here

# Windows PowerShell
$env:GOOGLE_API_KEY='your_actual_api_key_here'
```

**In Python (for testing only):**
```python
import os
os.environ["GOOGLE_API_KEY"] = "your_actual_api_key_here"
```

**⚠️ Security Warning:** Never hardcode API keys in your source code or commit them to version control.

## Quick Test

Test your installation with this simple example:

```python
from tbh_secure_agents import Expert, Operation

# Create a simple AI expert
expert = Expert(
    specialty="Assistant",
    objective="Help with simple tasks",
    security_profile="minimal"
)

# Create a simple task
task = Operation(
    instructions="Say hello and introduce yourself",
    expert=expert
)

# Execute the task
result = task.execute()
print(result)
```

If this runs successfully, you're ready to start building AI agents!
