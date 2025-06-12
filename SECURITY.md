# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.5.x   | :white_check_mark: |
| < 0.5   | :x:                |

## Reporting a Vulnerability

**DO NOT** create a public GitHub issue for security vulnerabilities.

If you discover a security vulnerability, please report it to security@tbh.ai. 
You should receive a response within 48 hours. If you don't hear back, please follow up via email.

Please include:
- A description of the vulnerability
- Steps to reproduce the issue
- Any potential impact
- Suggested mitigation or fix (if known)

## Security Updates

Security updates will be released as patch versions (e.g., 0.5.4 -> 0.5.5).

## Secure Development

- All code changes require code review by at least one other team member
- Security-sensitive changes require review by the security team
- Dependencies are regularly scanned for known vulnerabilities
- Secrets are never committed to the repository

## Security Best Practices

- Use environment variables for sensitive configuration
- Follow the principle of least privilege
- Validate all inputs
- Keep dependencies up to date
- Use prepared statements for database queries
- Implement proper error handling that doesn't leak sensitive information
