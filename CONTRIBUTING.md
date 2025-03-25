# Contributing to FungiMap

Thank you for your interest in contributing to FungiMap! We welcome contributions from the community.

## Quick Start

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes and test them
4. Commit with clear messages: `git commit -m "feat: add new feature"`
5. Push to your fork: `git push origin feature/your-feature-name`
6. Create a pull request

## Types of Contributions

### 🐛 Bug Reports
- Use the issue tracker
- Include system information (OS, Python version, environment)
- Provide minimal reproducible example
- Include error logs and expected vs actual behavior

### 💡 Feature Requests
- Check existing issues first
- Describe the use case and expected functionality
- Consider implementation complexity and maintenance burden

### 🔧 Code Contributions
- Follow existing code style (see `.pre-commit-config.yaml`)
- Add tests for new functionality
- Update documentation
- Ensure all tests pass
- Keep changes focused and atomic

### 📚 Documentation
- Fix typos, improve clarity
- Add examples and use cases
- Update API documentation
- Improve installation and setup guides

## Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/mycology-project.git
cd mycology-project

# Create development environment
conda env create -f environment.yml
conda activate mycograph-xl-demo

# Install in development mode
pip install -e .

# Run tests
python -m pytest tests/

# Run demo to verify setup
python scripts/create_demo_data.py
bash src/run_eda_pipeline.sh
```

## Code Standards

### Python Code
- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Write docstrings for functions and classes
- Maximum line length: 88 characters (Black formatter)

### Documentation
- Use Markdown for documentation files
- Include code examples in docstrings
- Update README if adding new features
- Comment complex algorithms and business logic

### Testing
- Write tests for new functionality
- Aim for >80% code coverage
- Use pytest for testing framework
- Include both unit tests and integration tests

## Commit Guidelines

Use conventional commit messages:

- `feat:` new features
- `fix:` bug fixes
- `docs:` documentation changes
- `style:` formatting, missing semicolons, etc.
- `refactor:` code restructuring
- `test:` adding tests
- `chore:` maintenance tasks

## Pull Request Process

1. **Before submitting:**
   - Rebase on latest main branch
   - Run all tests and ensure they pass
   - Update documentation if needed
   - Add entry to CHANGELOG.md

2. **PR Description:**
   - Link to related issues
   - Describe what changed and why
   - Include screenshots for UI changes
   - Note any breaking changes

3. **Review Process:**
   - Maintain respect and constructive feedback
   - Address reviewer comments promptly
   - Update documentation based on feedback

## Getting Help

- **Documentation**: Start with README and docs/
- **Issues**: Search existing issues before creating new ones
- **Discussions**: Use GitHub Discussions for questions
- **Email**: Contact maintainers for private matters

## Recognition

Contributors will be acknowledged in:
- CONTRIBUTORS.md file
- Release notes for significant contributions
- Academic papers using the software (where appropriate)

## Code of Conduct

This project follows our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to abide by its terms.

---

Thank you for helping make FungiMap better! 🍄