# MCP Control Center

Modern, offline-capable web interface for orchestrating multiple software projects with deep MCP (Model Context Protocol) integration.

## Features

- 🚀 **Multi-Language Project Management**: Manage projects across Python, JavaScript, Go, and more
- 🤖 **MCP Integration**: Real-time updates from AI agents via Model Context Protocol
- 📋 **Feature Tracking**: List, edit, and manage features, specs, refactors, and ADRs
- 🛡️ **Quality Gates**: Enforce separation of concerns and coding standards
- 📱 **PWA Support**: Works offline, installable on iPhone, iPad, and desktop
- ⚡ **Fast & Modern**: Built with FastAPI, HTMX, Alpine.js, and Tailwind CSS

## Quick Start

### Prerequisites

- Python 3.12+
- Redis (optional, for background jobs)
- Docker (optional)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/keithjasper83/mcp-control-center.git
cd mcp-control-center
```

2. Install dependencies:
```bash
pip install -e .
```

3. Copy environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Initialize the database:
```bash
python -m backend.app.cli init
```

5. Seed with demo data (optional):
```bash
python -m backend.app.cli seed
```

6. Run the application:
```bash
uvicorn backend.app.main:app --reload
```

Visit http://localhost:8000 to access the application.

### Docker Compose

```bash
cd ops
docker-compose up
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MCP_BASE_URL` | MCP server base URL | `http://localhost:8001` |
| `MCP_TOKEN` | MCP authentication token | - |
| `DATABASE_URL` | Database connection string | `sqlite:///./mcpcc.db` |
| `SECRET_KEY` | Application secret key | `change-me-in-production` |
| `DEBUG` | Debug mode | `False` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `REDIS_URL` | Redis connection URL | `redis://localhost:6379/0` |

## CLI Commands

```bash
# Initialize database
python -m backend.app.cli init

# Seed demo data
python -m backend.app.cli seed

# Sync from MCP server
python -m backend.app.cli sync-mcp --project <project-name>

# Generate SoC report
python -m backend.app.cli generate-soc-report

# Run quality gates
python -m backend.app.cli run-gates
```

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Development

### Install development dependencies:
```bash
pip install -e '.[dev]'
```

### Setup pre-commit hooks:
```bash
pre-commit install
```

### Run tests:
```bash
pytest
```

### Run with coverage:
```bash
pytest --cov=backend/app --cov-report=html
```

### Code formatting and linting:
```bash
ruff check .
black .
isort .
mypy backend/app
bandit -r backend/app
```

## Project Structure

```
mcp-control-center/
├── backend/
│   ├── app/
│   │   ├── api/          # API routes
│   │   ├── models/       # Database models
│   │   ├── services/     # Business logic
│   │   ├── views/        # Page renderers
│   │   ├── cli.py        # CLI commands
│   │   ├── config.py     # Configuration
│   │   ├── database.py   # Database setup
│   │   └── main.py       # FastAPI app
│   └── tests/            # Tests
├── frontend/
│   ├── templates/        # Jinja2 templates
│   ├── static/           # Static files
│   └── pwa/              # PWA assets
├── ops/
│   ├── Dockerfile        # Docker configuration
│   ├── docker-compose.yml
│   └── .devcontainer/    # VSCode devcontainer
├── ADRs/                 # Architecture Decision Records
├── pyproject.toml        # Python project configuration
└── README.md
```

## Domain Entities

- **Project**: Multi-language project with metadata
- **Feature**: User story or feature with status tracking
- **Specification**: API, UI, data, or security specs
- **RefactorPlan**: Planned refactoring with SoC findings
- **ADR**: Architecture Decision Record
- **Rule**: Quality gate rules (style, security, SoC, testing, performance)
- **AgentUpdate**: Updates received from AI agents
- **Proposal**: Change proposals with patches

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Security

See SECURITY.md for security policies and vulnerability reporting.
