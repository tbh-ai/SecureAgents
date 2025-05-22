# Utility Scripts

This directory contains utility scripts for the TBH Secure Agents framework. These scripts automate common development, build, and maintenance tasks.

## Documentation Scripts

- **generate_word_docs.py**: Generate Word documents from Markdown files
  ```bash
  python scripts/generate_word_docs.py
  ```

- **generate_word_docs.sh**: Shell script to generate Word documents (Unix/macOS)
  ```bash
  ./scripts/generate_word_docs.sh
  ```

- **generate_word_docs.bat**: Batch script to generate Word documents (Windows)
  ```bash
  scripts\generate_word_docs.bat
  ```

## Build and Publishing Scripts

- **build_package.py**: Build the package
  ```bash
  python scripts/build_package.py
  ```

- **build_and_publish.sh**: Build and publish the package to PyPI
  ```bash
  ./scripts/build_and_publish.sh
  ```

## Version Control Scripts

- **push_to_github.sh**: Push changes to GitHub
  ```bash
  ./scripts/push_to_github.sh "Commit message"
  ```

## Security Profile Management

- **update_security_profiles.py**: Update specific security profiles
  ```bash
  python scripts/update_security_profiles.py --profile minimal
  ```

- **update_all_security_profiles.py**: Update all security profiles
  ```bash
  python scripts/update_all_security_profiles.py
  ```

## Adding New Scripts

When adding new scripts to this directory:

1. Make sure the script has a clear, specific purpose
2. Add appropriate documentation and usage instructions
3. Include error handling and logging
4. Make the script executable if it's a shell script (`chmod +x script_name.sh`)
5. Update this README.md file with information about the new script

## Script Best Practices

1. **Documentation**: Include a docstring or header comment explaining the purpose and usage of the script
2. **Error Handling**: Include proper error handling and exit codes
3. **Logging**: Use appropriate logging for important events and errors
4. **Configuration**: Use command-line arguments or configuration files for customization
5. **Testing**: Test scripts thoroughly before committing them
