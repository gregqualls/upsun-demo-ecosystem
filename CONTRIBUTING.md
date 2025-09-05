# Contributing to Upsun Demo Ecosystem Generator

Thank you for your interest in contributing to this project! This document provides guidelines for contributing to the Upsun Demo Ecosystem Generator.

## How to Contribute

### Reporting Issues

If you find a bug or have a feature request:

1. Check if the issue already exists in the [Issues](https://github.com/gregqualls/upsun-demo-ecosystem/issues) section
2. Create a new issue with:
   - Clear title and description
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Environment details (OS, Python version, Upsun CLI version)

### Submitting Changes

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Test your changes thoroughly
5. Commit with a clear message: `git commit -m "Add: your feature description"`
6. Push to your fork: `git push origin feature/your-feature-name`
7. Create a Pull Request

### Development Guidelines

#### Code Style
- Follow Python PEP 8 style guidelines
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions focused and small

#### Testing
- Test with different configuration files
- Verify both setup and cleanup scripts work
- Test with both GitHub and local project sources
- Ensure error handling works correctly

#### Documentation
- Update README.md for new features
- Add examples to example-config.json
- Update comments in code when needed

### Configuration File Changes

When modifying configuration structure:
- Update all example files (demo-config.json, example-config.json, final-test-config.json)
- Update README.md with new field descriptions
- Ensure backward compatibility when possible
- Add migration notes for breaking changes

## Questions?

Feel free to open an issue for any questions about contributing!
