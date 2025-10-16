# MCP Control Center Architecture

## Overview

The MCP Control Center is a web-based platform for managing multi-language software projects through the Model Control Protocol (MCP). It provides a modern interface for tracking Features, Specifications, Refactors, Architectural Decision Records (ADRs), and project Rules.

## Architecture Philosophy

### Core Principles

1. **Separation of Concerns**: Clear boundaries between domain logic, presentation, and integration
2. **Clean Architecture**: Dependencies point inward toward domain models
3. **Type Safety**: Full type hints throughout the codebase
4. **Testability**: All components designed for easy testing
5. **AI Extensibility**: Built to integrate with AI agents and automation

### Design Patterns

- **Repository Pattern**: Data access abstraction
- **Service Layer**: Business logic encapsulation
- **Dependency Injection**: Loose coupling between components
- **API Gateway**: Single entry point for external integrations

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Presentation Layer                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Jinja2     │  │    HTMX      │  │  TailwindCSS │  │
│  │  Templates   │  │  Dynamic UI  │  │    Styling   │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────────┐
│                      API Layer (FastAPI)                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Features   │  │    Specs     │  │  Refactors   │  │
│  │   Endpoints  │  │  Endpoints   │  │  Endpoints   │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│  ┌──────────────┐  ┌──────────────┐                    │
│  │     ADRs     │  │    Rules     │                    │
│  │   Endpoints  │  │  Endpoints   │                    │
│  └──────────────┘  └──────────────┘                    │
└─────────────────────────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────────┐
│                     Service Layer                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Feature    │  │     Spec     │  │   Refactor   │  │
│  │   Service    │  │   Service    │  │   Service    │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │     ADR      │  │    Rules     │  │  MCP Client  │  │
│  │   Service    │  │   Service    │  │   Service    │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────────┐
│                      Domain Models                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Feature    │  │     Spec     │  │   Refactor   │  │
│  │    Model     │  │    Model     │  │    Model     │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │     ADR      │  │    Rule      │  │   Project    │  │
│  │    Model     │  │    Model     │  │    Model     │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────────┐
│                     Data Layer (SQLModel)                │
│  ┌──────────────┐  ┌──────────────┐                    │
│  │    SQLite    │  │  PostgreSQL  │                    │
│  │   (Default)  │  │  (Optional)  │                    │
│  └──────────────┘  └──────────────┘                    │
└─────────────────────────────────────────────────────────┘
```

## External Integrations

```
┌─────────────────────────────────────────────────────────┐
│                  External Systems                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │     MCP      │  │   Jarvis AI  │  │   AI Model   │  │
│  │   Protocol   │  │    Agent     │  │     API      │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                            ▲
                            │
                    ┌───────┴───────┐
                    │  MCP Client   │
                    │    Service    │
                    └───────────────┘
```

## Directory Structure

```
mcp-control-center/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration management
│   ├── database.py             # Database setup and session management
│   │
│   ├── api/                    # API endpoints
│   │   ├── __init__.py
│   │   ├── features.py         # Feature CRUD endpoints
│   │   ├── specifications.py  # Specification endpoints
│   │   ├── refactors.py       # Refactor endpoints
│   │   ├── adrs.py            # ADR endpoints
│   │   ├── rules.py           # Rule endpoints
│   │   └── projects.py        # Project endpoints
│   │
│   ├── models/                 # SQLModel data models
│   │   ├── __init__.py
│   │   ├── feature.py
│   │   ├── specification.py
│   │   ├── refactor.py
│   │   ├── adr.py
│   │   ├── rule.py
│   │   └── project.py
│   │
│   ├── services/               # Business logic layer
│   │   ├── __init__.py
│   │   ├── feature_service.py
│   │   ├── spec_service.py
│   │   ├── refactor_service.py
│   │   ├── adr_service.py
│   │   ├── rule_service.py
│   │   ├── project_service.py
│   │   ├── mcp_client.py      # MCP integration service
│   │   └── ai_service.py      # AI model integration
│   │
│   ├── templates/              # Jinja2 templates
│   │   ├── base.html          # Base template with layout
│   │   ├── index.html         # Home page
│   │   ├── features/
│   │   ├── specifications/
│   │   ├── refactors/
│   │   ├── adrs/
│   │   ├── rules/
│   │   └── components/        # Reusable template components
│   │
│   └── static/                 # Static assets
│       ├── css/
│       │   └── tailwind.css
│       ├── js/
│       │   └── alpine.js
│       └── images/
│
├── tests/                      # Test suite
│   ├── __init__.py
│   ├── conftest.py            # Pytest fixtures
│   ├── test_api/              # API endpoint tests
│   ├── test_services/         # Service layer tests
│   └── test_models/           # Model tests
│
├── migrations/                 # Database migrations (Alembic)
│   └── versions/
│
├── .github/
│   └── copilot-instructions.md
│
├── pyproject.toml             # Project dependencies and config
├── README.md                  # Project documentation
├── ARCHITECTURE.md            # This file
└── .gitignore
```

## Data Models

### Core Entities

#### Project
- Represents a software project being managed
- Contains metadata, settings, and configuration
- Parent entity for Features, Specs, Refactors, ADRs, and Rules

#### Feature
- User-facing functionality or capability
- Tracked from conception to completion
- Links to Specifications and Refactors

#### Specification
- Detailed technical specification
- Describes implementation requirements
- Can be generated by AI or written manually

#### Refactor
- Code improvement or restructuring task
- Contains before/after descriptions
- Tracks technical debt reduction

#### ADR (Architectural Decision Record)
- Documents significant architectural decisions
- Provides context, decision, and consequences
- Maintains historical record of choices

#### Rule
- Project-specific coding rules and conventions
- Enforced by AI agents and linters
- Can be shared across projects

### Relationships

```
Project (1) ─────< (N) Feature
                       │
                       ├──< (N) Specification
                       └──< (N) Refactor

Project (1) ─────< (N) ADR

Project (1) ─────< (N) Rule
```

## Service Layer Design

### Service Responsibilities

Each service encapsulates business logic for its domain:

1. **Validation**: Ensure data integrity before persistence
2. **Business Rules**: Implement domain-specific rules
3. **Coordination**: Orchestrate operations across multiple models
4. **Integration**: Interface with external systems (MCP, AI)

### Example Service Pattern

```python
class FeatureService:
    """Service for managing features with business logic."""
    
    def __init__(self, db: Session, mcp_client: MCPClient):
        self.db = db
        self.mcp_client = mcp_client
    
    async def create_feature(
        self,
        project_id: int,
        feature_data: dict
    ) -> Feature:
        """Create a new feature with validation and MCP sync."""
        # 1. Validate data
        # 2. Create feature in database
        # 3. Sync with MCP
        # 4. Return created feature
        pass
    
    async def generate_specifications(
        self,
        feature_id: int
    ) -> List[Specification]:
        """Generate specifications for a feature using AI."""
        # 1. Fetch feature
        # 2. Call AI service
        # 3. Create specifications
        # 4. Return generated specs
        pass
```

## API Design

### RESTful Conventions

- `GET /api/{resource}` - List resources
- `GET /api/{resource}/{id}` - Get single resource
- `POST /api/{resource}` - Create resource
- `PUT /api/{resource}/{id}` - Update resource
- `DELETE /api/{resource}/{id}` - Delete resource

### HTMX-Specific Endpoints

Some endpoints return HTML fragments for HTMX:

- `GET /htmx/{resource}/{id}/edit` - Return edit form
- `GET /htmx/{resource}/{id}/view` - Return view component

### Response Formats

JSON for API endpoints:
```json
{
  "id": 1,
  "title": "Feature Title",
  "status": "active",
  "created_at": "2025-01-15T10:30:00Z"
}
```

HTML fragments for HTMX:
```html
<div id="feature-1" class="feature-card">
  <h3>Feature Title</h3>
  <span class="badge-active">Active</span>
</div>
```

## Frontend Architecture

### Mobile-First Design

1. **Base**: Design for iPhone (375px)
2. **Tablet**: Enhance for iPad (768px)
3. **Desktop**: Optimize for desktop (1024px+)

### HTMX Patterns

#### Partial Updates
```html
<div hx-get="/htmx/features" 
     hx-trigger="load" 
     hx-swap="innerHTML">
</div>
```

#### Form Submission
```html
<form hx-post="/api/features" 
      hx-target="#feature-list" 
      hx-swap="beforeend">
</form>
```

#### Polling for Updates
```html
<div hx-get="/htmx/updates" 
     hx-trigger="every 5s">
</div>
```

### Alpine.js Usage

Use Alpine.js for:
- Local UI state (dropdowns, modals)
- Client-side validation
- Interactive forms
- Conditional rendering

Avoid Alpine.js for:
- Server state management (use HTMX)
- Complex data fetching (use HTMX)
- Routing (use server-side routing)

## MCP Integration

### Protocol Overview

The Model Control Protocol (MCP) provides:
- Project metadata synchronization
- AI agent update notifications
- Structured proposal submission
- Refactor plan distribution

### Integration Points

1. **Metadata Sync**: Periodic sync of project data with MCP
2. **Event Subscriptions**: Real-time updates from AI agents
3. **Proposal Submission**: Send structured proposals to MCP
4. **Status Updates**: Receive and display agent progress

### MCP Client Service

Located in `app/services/mcp_client.py`, provides:
- Connection management
- Request/response handling
- Event stream processing
- Error handling and retry logic

## AI Integration

### AI Service Responsibilities

1. **Prompt Generation**: Create structured prompts for AI agents
2. **Specification Generation**: Generate technical specs from features
3. **Code Analysis**: Analyze code for refactor opportunities
4. **Documentation**: Generate ADRs and documentation

### Integration Pattern

```python
class AIService:
    """Service for AI model integration."""
    
    async def generate_specification(
        self,
        feature: Feature,
        context: dict
    ) -> Specification:
        """Generate specification using AI model."""
        # 1. Build prompt with context
        # 2. Call AI API
        # 3. Parse and validate response
        # 4. Create specification object
        pass
```

## Testing Strategy

### Test Pyramid

```
       ┌───────────┐
       │    E2E    │  <-- Few, critical user flows
       └───────────┘
      ┌─────────────┐
      │ Integration │  <-- API and database tests
      └─────────────┘
    ┌─────────────────┐
    │      Unit       │  <-- Many, fast, isolated tests
    └─────────────────┘
```

### Test Categories

1. **Unit Tests**: Test individual functions and classes in isolation
2. **Integration Tests**: Test API endpoints with database
3. **E2E Tests**: Test complete user flows with HTMX

### Testing Tools

- **pytest**: Test framework
- **pytest-asyncio**: Async test support
- **httpx**: API client for testing
- **factory_boy**: Test data factories
- **faker**: Generate test data

## Security Considerations

### Authentication & Authorization

- JWT-based authentication (future)
- Role-based access control
- API key management for MCP integration

### Data Protection

- Input validation on all endpoints
- SQL injection prevention via SQLModel
- XSS prevention in templates
- CSRF protection for forms

### External Integrations

- Secure credential storage
- API key rotation
- Rate limiting on external calls
- Error message sanitization

## Performance Optimization

### Database

- Indexes on frequently queried fields
- Connection pooling
- Query optimization
- Pagination for large datasets

### Frontend

- Lazy loading of components
- Minimal JavaScript bundle
- Optimized images
- CDN for static assets

### Caching

- Redis for session storage (future)
- HTTP caching headers
- Template fragment caching
- API response caching

## Deployment Considerations

### Environment Configuration

- Development: SQLite, debug mode
- Staging: PostgreSQL, testing environment
- Production: PostgreSQL, optimized settings

### Container Deployment

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Monitoring

- Application logs
- Error tracking (Sentry)
- Performance metrics
- Database query monitoring

## Future Enhancements

### Planned Features

1. **Real-time Collaboration**: Multiple users editing simultaneously
2. **Advanced AI Integration**: More sophisticated AI assistance
3. **Project Templates**: Pre-configured project setups
4. **Import/Export**: Integration with external tools
5. **Advanced Analytics**: Project metrics and insights

### Scalability

- Microservices architecture (if needed)
- Message queue for async tasks (Celery/RQ)
- Distributed caching (Redis cluster)
- Load balancing and horizontal scaling

## References

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **SQLModel Documentation**: https://sqlmodel.tiangolo.com/
- **HTMX Documentation**: https://htmx.org/
- **TailwindCSS Documentation**: https://tailwindcss.com/
- **Model Control Protocol**: (MCP documentation link)

## Contributing

When contributing to the architecture:

1. Follow the established patterns
2. Document significant decisions in ADRs
3. Update this document for major changes
4. Discuss architectural changes with the team
5. Maintain backward compatibility when possible

## Conclusion

This architecture provides a solid foundation for the MCP Control Center while maintaining flexibility for future enhancements. The clean separation of concerns, type safety, and test coverage ensure long-term maintainability and AI extensibility.
