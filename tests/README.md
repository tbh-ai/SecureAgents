# Tests for TBH Secure Agents

This directory contains comprehensive tests for the TBH Secure Agents framework. A robust test suite is essential for maintaining the security and reliability of the framework.

## Running Tests

### Running All Tests

To run all tests:

```bash
cd SecureAgents
python -m unittest discover tests
```

### Running Specific Test Categories

To run tests in a specific category:

```bash
cd SecureAgents
python -m unittest discover tests "*security_profiles*"
python -m unittest discover tests "*security_validation*"
python -m unittest discover tests "*visualization*"
python -m unittest discover tests "*integration*"
```

### Running Individual Tests

To run a specific test file:

```bash
cd SecureAgents
python -m unittest tests/test_security_profiles.py
```

To run a specific test case or method:

```bash
cd SecureAgents
python -m unittest tests.test_security_profiles.TestSecurityProfiles
python -m unittest tests.test_security_profiles.TestSecurityProfiles.test_minimal_profile
```

## Test Output

Test results are saved to the `outputs/test_results` directory. This directory is not included in the repository.

## Test Categories

- **Security Profiles**: Tests for security profile functionality
  - Validation of security profile parameters
  - Profile inheritance and overrides
  - Custom profile registration and retrieval

- **Security Validation**: Tests for security validation components
  - Regex validation tests
  - ML validation tests
  - LLM validation tests
  - Hybrid validation tests
  - Parallel validation tests

- **Visualization**: Tests for report generation and visualization
  - HTML report generation
  - Markdown report generation
  - Chart generation
  - Logo integration

- **Integration**: Tests for framework integration
  - Expert integration tests
  - Squad integration tests
  - Operation integration tests
  - End-to-end workflow tests

## Writing Tests

When writing tests, follow these guidelines:

1. **Test Organization**: Place tests in the appropriate category
2. **Test Naming**: Use descriptive names for test methods (e.g., `test_minimal_profile_blocks_dangerous_commands`)
3. **Test Coverage**: Aim for high test coverage, especially for security-critical components
4. **Test Independence**: Tests should be independent and not rely on the state from other tests
5. **Test Documentation**: Document the purpose and expected behavior of each test
6. **Test Edge Cases**: Include tests for edge cases and potential failure modes
7. **Test Security**: Include tests that verify security properties and constraints

## Test Dependencies

Tests may require additional dependencies that are not needed for normal operation. These dependencies are specified in the `dev` extra in `setup.py`.
