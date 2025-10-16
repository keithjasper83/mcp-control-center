# MCP Control Center

A modern web-based platform for managing multi-language software projects through the Model Control Protocol (MCP).

## Overview

The MCP Control Center provides a responsive, mobile-first interface for tracking and managing:
- **Features**: User-facing functionality and capabilities
- **Specifications**: Detailed technical specifications
- **Refactors**: Code improvement and restructuring tasks
- **ADRs**: Architectural Decision Records
- **Rules**: Project-specific coding rules and conventions

Built with FastAPI, HTMX, and TailwindCSS, it integrates tightly with MCP APIs to receive AI Agent updates and push structured proposals.

## Technology Stack

- **Backend**: Python 3.12+ with FastAPI
- **Database**: SQLModel with SQLite (PostgreSQL optional)
- **Frontend**: Jinja2 templates, HTMX, Alpine.js, TailwindCSS
- **Testing**: pytest with full type hints (mypy)
- **Code Quality**: Black, Ruff, PEP 8

## Quick Start

### Prerequisites

- Python 3.12 or higher
- pip or poetry for dependency management

### Installation

```bash
# Clone the repository
git clone https://github.com/keithjasper83/mcp-control-center.git
cd mcp-control-center

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn app.main:app --reload
```

The application will be available at `http://localhost:8000`

## Project Structure

```
mcp-control-center/
├── app/
│   ├── api/          # API endpoints
│   ├── services/     # Business logic
│   ├── models/       # SQLModel data models
│   ├── templates/    # Jinja2 templates
│   └── static/       # CSS, JS, images
├── tests/            # Test suite
├── .github/          # GitHub configurations
│   └── copilot-instructions.md
├── ARCHITECTURE.md   # Architecture documentation
└── README.md         # This file
```

## Development

### Code Quality

This project enforces high code quality standards:

```bash
# Format code with Black
black app/ tests/

# Lint with Ruff
ruff app/ tests/

# Type check with MyPy
mypy app/

# Run tests
pytest
```

### GitHub Copilot

This project includes comprehensive GitHub Copilot instructions. See `.github/copilot-instructions.md` for:
- Coding standards and patterns
- Architecture guidelines
- Technology stack usage
- Best practices

## Documentation

- **[ARCHITECTURE.md](ARCHITECTURE.md)**: Detailed architecture and design decisions
- **[.github/copilot-instructions.md](.github/copilot-instructions.md)**: GitHub Copilot guidelines
- **API Documentation**: Available at `/docs` when running the application

## Features

### Current
- Project metadata management
- MCP integration framework
- Clean architecture with separation of concerns

### Planned
- Feature tracking and management
- Specification generation with AI
- Refactor planning and execution
- ADR management
- Rule enforcement
- Real-time AI agent updates

## Contributing

Contributions are welcome! Please:
1. Follow the coding standards outlined in `.github/copilot-instructions.md`
2. Write tests for new features
3. Update documentation as needed
4. Ensure all tests pass before submitting PRs

## License

[Add your license here]

## Contact

[Add contact information or links]
