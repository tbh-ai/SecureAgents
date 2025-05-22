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

## Project Structure

The TBH Secure Agents framework is organized into the following directories:

* **`tbh_secure_agents/`**: Core package code
  * **`security/`**: Security-related components
  * **`security_validation/`**: Security validation system
  * **`security_profiles/`**: Security profile definitions and management

* **`docs/`**: Comprehensive documentation

* **`examples/`**: Example code demonstrating framework usage

* **`tests/`**: Comprehensive test suite
  * Unit tests, integration tests, and security validation tests

* **`scripts/`**: Utility scripts for development and maintenance
  * Build scripts, update scripts, and other utilities

* **`outputs/`**: Directory for generated outputs (not included in repository)
  * Generated reports, visualizations, and test results

## Development Setup

Please refer to the [Installation Guide](./docs/installation.md) for instructions on setting up your development environment, including installing the package in editable mode and installing development dependencies (`pip install -e .[dev]`).

When adding new code:
1. Core functionality should be added to the appropriate module in `tbh_secure_agents/`
2. Tests should be added to the `tests/` directory
3. Examples should be added to the `examples/` directory
4. Documentation should be added to the `docs/` directory
5. Utility scripts should be added to the `scripts/` directory
6. Generated outputs should be saved to the `outputs/` directory (which is git-ignored)

## Code Style

We aim to follow standard Python style guidelines (PEP 8). Please ensure your code is well-formatted and readable. We use `flake8` for linting (configuration defined in the GitHub Actions workflow).

## Security Considerations

Given the focus of this project, security is paramount. When contributing code, please follow these security guidelines:

1. **Security-First Approach**: Always prioritize security over convenience or performance.

2. **Input Validation**: All user inputs must be properly validated and sanitized.

3. **Security Profiles**: Maintain the integrity of the security profile system. Any changes to security profiles should be thoroughly documented and tested.

4. **Security Validation**: The security validation system is a critical component. Changes to this system require extensive testing and review.

5. **Dependency Management**: Be cautious when adding new dependencies. Each new dependency increases the attack surface.

6. **Code Review**: All security-related code should undergo thorough peer review.

7. **Testing**: Write comprehensive tests for security features, including edge cases and potential attack vectors.

8. **Documentation**: Document security implications of new features and changes.

If you identify a potential security vulnerability, please report it responsibly by emailing saish.shinde.jb@gmail.com with the subject "TBH Secure Agents Security Vulnerability".

## Questions?

Feel free to open an issue if you have questions about contributing.

We appreciate your contributions!
