# Contributing to TBH Secure Agents

Thank you for your interest in contributing to TBH Secure Agents! We welcome contributions from the community to help make this framework more robust, secure, and feature-rich.

## How to Contribute

There are several ways you can contribute:

*   **Reporting Bugs:** If you find a bug, please open an issue on the [GitHub Issues page](https://github.com/saishshinde15/TBH.AI_SecureAgents/issues), providing as much detail as possible, including steps to reproduce the bug.
*   **Suggesting Enhancements:** Have an idea for a new feature or an improvement to an existing one? Open an issue to discuss it. We're particularly interested in ideas related to enhancing the security aspects of the framework.
*   **Pull Requests:** If you'd like to contribute code (bug fixes, new features, documentation improvements), please follow these steps:
    1.  **Fork the repository.**
    2.  **Create a new branch** for your feature or fix: `git checkout -b feature/your-feature-name` or `fix/your-fix-name`.
    3.  **Make your changes.** Ensure your code adheres to the project's style and quality standards.
    4.  **Add tests** for any new functionality. (Testing framework TBD).
    5.  **Ensure code passes linting:** Run `flake8 .` locally. The GitHub Actions workflow will also check this.
    6.  **Update documentation** if necessary.
    7.  **Commit your changes** with clear and concise commit messages.
    8.  **Push your branch** to your fork.
    9.  **Open a Pull Request** against the `main` branch of the original repository. Provide a clear description of your changes.

## Development Setup

Please refer to the [Installation Guide](./docs/installation.md) for instructions on setting up your development environment, including installing the package in editable mode and installing development dependencies (`pip install -e .[dev]`).

## Code Style

We aim to follow standard Python style guidelines (PEP 8). Please ensure your code is well-formatted and readable. We use `flake8` for linting (configuration defined in the GitHub Actions workflow).

## Security Considerations

Given the focus of this project, security is paramount. When contributing code, please consider potential security implications. If you identify a potential security vulnerability, please report it responsibly (details TBD - consider adding a SECURITY.md file later).

## Questions?

Feel free to open an issue if you have questions about contributing.

We appreciate your contributions!
