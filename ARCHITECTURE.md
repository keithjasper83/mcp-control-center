# Architecture Overview

## System Design

MCP Control Center is built as a modern web application with clear separation between backend and frontend concerns.

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Client (Browser)                     │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────┐ │
│  │   PWA UI    │  │ Service      │  │  Alpine.js    │ │
│  │  (Jinja2)   │  │  Worker      │  │  HTMX         │ │
│  └─────────────┘  └──────────────┘  └───────────────┘ │
└───────────────────────────┬─────────────────────────────┘
                            │ HTTP/WebSocket
┌───────────────────────────┴─────────────────────────────┐
│               FastAPI Application Server                │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────┐ │
│  │  API Routes │  │  Services    │  │  Views        │ │
│  │  (REST)     │  │  Layer       │  │  (Jinja2)     │ │
│  └─────────────┘  └──────────────┘  └───────────────┘ │
└───────────────────────────┬─────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
┌───────┴────────┐  ┌──────┴───────┐  ┌────────┴────────┐
│  SQLite/       │  │  MCP Server  │  │  Redis Queue    │
│  PostgreSQL    │  │  (External)  │  │  (Background)   │
└────────────────┘  └──────────────┘  └─────────────────┘
```

## Component Architecture

### Backend Layer (FastAPI)

**API Routes** (`app/api/`)
- RESTful endpoints for all entities
- Request validation with Pydantic
- Authentication middleware (token-based, WebAuthn-ready)
- CORS configuration

**Services Layer** (`app/services/`)
- `mcp_client.py`: MCP protocol integration
- `soc_checks.py`: Separation of concerns analysis
- `rules.py`: Quality gate enforcement
- `reports.py`: Report generation
- `proposals.py`: Change proposal management

**Models Layer** (`app/models/`)
- SQLModel entities for database tables
- Type-safe with Pydantic validation
- JSON fields for flexible data structures

**Views Layer** (`app/views/`)
- Server-rendered pages with Jinja2
- HTMX partial responses
- Mobile-first templates

### Frontend Layer

**Templates** (`frontend/templates/`)
- Base layout with navigation
- Page-specific templates
- HTMX partials for dynamic updates
- Alpine.js for client-side interactivity

**Static Assets** (`frontend/static/`)
- Tailwind CSS for styling
- Minimal custom JavaScript
- Icons and images

**PWA** (`frontend/pwa/`)
- Service worker for offline support
- Web app manifest
- Installable on mobile and desktop

### Data Layer

**Database**
- SQLite for simplicity (default)
- PostgreSQL for production (optional)
- Async SQLAlchemy/SQLModel for ORM
- Alembic for migrations

**Caching**
- Redis for session storage
- Background job queue (RQ/Arq)

## Design Principles

### 1. Separation of Concerns

- Clear boundaries between API, services, and data layers
- No business logic in routes
- Services encapsulate domain logic
- Models only contain data structure

### 2. Server-Driven UI

- Minimize client-side JavaScript
- HTMX for dynamic updates without SPA complexity
- Progressive enhancement
- Fast initial page loads

### 3. Offline-First

- Service worker caches assets
- Read-only offline access to cached data
- Sync when connection restored
- PWA for native-like experience

### 4. Type Safety

- Python type hints throughout
- Pydantic for validation
- SQLModel for type-safe ORM
- Mypy for static type checking

### 5. Air-Gap Capable

- No external dependencies at runtime
- All assets served locally
- Optional CDN fallbacks
- Works without internet

## MCP Integration

### Inbound (Receiving Updates)

```
AI Agent → MCP Server → POST /api/mcp/updates → AgentUpdate Entity
```

- Agents push updates via webhook-like mechanism
- Updates stored for audit and processing
- Can trigger actions (create features, specs, etc.)

### Outbound (Querying & Proposals)

```
Control Center → MCP Client → MCP Server → Project Data
```

- Query projects, features, specs from MCP
- Submit proposals for agent review
- Pull latest status on demand

## Security Model

### Current (V1)

- Token-based API authentication
- Environment variable secrets
- No password storage
- CORS protection

### Future (V2)

- WebAuthn/Passkeys support
- Role-based access control
- Audit logging
- Rate limiting

## Quality Enforcement

### Static Analysis

```
Code → Analyzer → Rules Engine → Gate Decision (WARN/FAIL)
```

- Python: import graph analysis with grimp
- Generic: tag-based layer validation
- Custom rules per project
- CI integration for automated checks

### Reports

- **SoC Report**: Module dependencies, circular imports, layer violations
- **Quality Report**: Lint, type check, test coverage, security scan results

## Scalability Considerations

### Current Scale

- Single-process deployment
- SQLite sufficient for small teams
- In-process background jobs

### Future Scale

- Multi-worker deployment with Gunicorn/Uvicorn
- PostgreSQL for concurrent access
- Redis for distributed job queue
- Horizontal scaling behind load balancer

## Technology Choices (ADRs)

See `ADRs/` directory for detailed Architecture Decision Records:

1. **ADR-0001**: Use FastAPI for REST API
2. **ADR-0002**: Server-driven UI with HTMX over React/Next.js
3. **ADR-0003**: SQLite default, PostgreSQL optional
4. **ADR-0004**: PWA for mobile/offline support
5. **ADR-0005**: Token-based auth now, WebAuthn later

## Deployment Options

### Option 1: Direct Python
```bash
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
```

### Option 2: Docker Compose
```bash
docker-compose up
```

### Option 3: Kubernetes
- Deploy as container
- Use managed PostgreSQL
- Redis cluster for jobs
- Ingress for HTTPS

### Option 4: Platform as a Service
- Deploy to Render, Fly.io, Railway
- Automatic HTTPS
- Managed database
- Easy scaling
