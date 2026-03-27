# Contributing to kernpy

Thank you for your interest in contributing to kernpy! This guide explains how to set up your development environment, run tests, and submit contributions.

## Development Setup

### Prerequisites

- Python 3.9 or later
- Git
- macOS, Linux, or Windows

### Clone the Repository

```bash
git clone https://github.com/OMR-PRAIG-UA-ES/kernpy.git
cd kernpy
```

### Set Up Development Environment

We use `uv` for Python package management. Install it first:

```bash
# macOS or Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Then set up kernpy:

```bash
# Install dependencies and create virtual environment
uv sync

# Install with development tools
uv sync --group dev

# For documentation work
uv sync --group docs
```

### Verify Installation

```bash
# Activate the virtual environment
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate  # Windows

# Run tests
python -m pytest
```

## Running Tests

### Run All Tests

```bash
uv run pytest
```

### Run Specific Test File

```bash
uv run pytest test/test_importer.py
```

### Run with Verbose Output

```bash
uv run pytest -v
```

### Run with Coverage Report

```bash
uv run pytest --cov=kernpy
```

### Run Quick Tests Only

```bash
# Tests without downloading Polish dataset
uv run pytest -m "not slow"
```

## Documentation

### Build Documentation Locally

```bash
# Install documentation dependencies
uv sync --group docs

# Build the site
uv run mkdocs build

# View locally
uv run mkdocs serve
# Visit http://localhost:8000
```

### Edit Documentation

Documentation files are in `docs/`:

- `docs/index.md` — Landing page
- `docs/get-started.md` — Getting started guide
- `docs/get-started/quick-start-5min.md` — 5-minute quick start
- `docs/concepts/` — Core concept explanations
- `docs/guides/` — Practical how-to guides
- `docs/advanced/` — Advanced topics
- `docs/how-to-guides.md` — Index of all guides
- `docs/reference.md` — API reference
- `docs/examples.md` — Code examples collection
- `docs/faq.md` — Frequently asked questions
- `docs/citation.md` — Citation information
- `docs/about.md` — About the project
- `docs/contributing.md` — This file

### Documentation Standards

- Use clear, concise language
- Include code examples where applicable
- Add cross-links using `[text](path/to/file.md)`
- Use proper Markdown formatting
- For **kern notation, use backticks: `` `**kern` ``
- Avoid emojis
- Test all code examples before submitting

## Code Style

### Format Code

```bash
uv run black kernpy/ test/
```

### Check Linting

```bash
uv run flake8 kernpy/ test/
```

### Run Type Checking

```bash
# If mypy is installed
uv run mypy kernpy/
```

## Git Workflow

### Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### Make Your Changes

1. Edit files
2. Run tests: `uv run pytest`
3. Update documentation if needed
4. Verify no new warnings: `uv run mkdocs build`

### Commit Changes

```bash
git add .
git commit -m "Brief description of changes"
```

Use imperative mood ("Add feature" not "Added feature").

### Push to GitHub

```bash
git push origin feature/your-feature-name
```

### Open a Pull Request

1. Visit https://github.com/OMR-PRAIG-UA-ES/kernpy
2. Click "Compare & pull request"
3. Write clear PR description explaining:
   - What changes you made
   - Why these changes are needed
   - Any tests you added
   - Links to related issues
4. Submit the PR

## Types of Contributions

### Bug Reports

Found a bug? Open an issue on [GitHub Issues](https://github.com/OMR-PRAIG-UA-ES/kernpy/issues) with:

1. Clear description of the problem
2. Steps to reproduce
3. Expected vs actual behavior
4. Python version and kernpy version
5. Example code or file if possible

### Feature Requests

Have an idea? [Open an issue](https://github.com/OMR-PRAIG-UA-ES/kernpy/issues) with:

1. Clear description of the feature
2. Use case or motivation
3. Proposed API (if applicable)
4. Examples of how it would be used

### Code Contributions

To contribute code:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Update documentation
6. Submit a pull request

See [Git Workflow](#git-workflow) above.

### Documentation Improvements

Documentation improvements are always welcome:

1. Fix typos or clarify explanations
2. Add examples to existing docs
3. Create new guides for common tasks
4. Improve formatting or organization

No special process needed—just follow the [Git Workflow](#git-workflow).

## Testing

### Writing Tests

Test files are in the `test/` directory and follow this pattern:

```python
import kernpy as kp
import pytest

def test_load_basic():
    """Test basic file loading"""
    doc, errors = kp.load('test/resources/score.krn')
    assert doc is not None
    assert len(errors) == 0

def test_transpose():
    """Test transposition"""
    doc, _ = kp.load('test/resources/score.krn')
    transposed = doc.to_transposed('P4', 'up')
    assert transposed is not None
```

### Running Your Tests

```bash
# Run your specific test
uv run pytest test/test_your_feature.py -v

# Run with coverage
uv run pytest test/test_your_feature.py --cov=kernpy
```

## Community Guidelines

### Be Respectful

- Treat all contributors with respect
- Welcome diverse perspectives
- Assume good intent
- Focus on ideas, not people

### Ask Questions

- No question is too simple
- Ask for clarification if you're unsure
- Help others asking questions

### Attribution

When contributing:
- Ensure you have rights to contributed code
- Add your name to AUTHORS if significant contribution
- Include proper license headers where needed (AGPL-3.0-only)

## Project Structure

```
kernpy/
├── kernpy/
│   ├── __init__.py         # Main API exports
│   ├── core/               # Core functionality
│   ├── io/                 # Input/output utilities
│   └── util/               # Utility functions
├── test/                   # Test files
├── docs/                   # Documentation
├── pyproject.toml          # Project metadata
├── pytest.ini              # pytest configuration
└── mkdocs.yml              # Documentation configuration
```

## Licensing

kernpy is distributed under the **AGPL-3.0-only** license. By contributing, you agree that your contributions will be licensed under this license.

If you have questions about licensing, please open an issue.

## Getting Help

- Check [existing GitHub Issues](https://github.com/OMR-PRAIG-UA-ES/kernpy/issues)
- Read the [documentation](index.md)
- Look at [examples](examples.md)
- Ask in a new GitHub issue

## Recognition

Contributors are recognized in:
- [GitHub Contributors](https://github.com/OMR-PRAIG-UA-ES/kernpy/graphs/contributors)
- Release notes for significant contributions
- AUTHORS file (for substantial contributions)

## Roadmap

See [GitHub Issues](https://github.com/OMR-PRAIG-UA-ES/kernpy/issues) for:
- Planned features
- Known limitations
- Opportunities for contribution

## Questions?

Feel free to:
- Open an issue with your question
- Ask in pull request discussions
- Email the maintainers (see GitHub repository)

Thank you for contributing to kernpy!
