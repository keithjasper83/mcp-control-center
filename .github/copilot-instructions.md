# GitHub Copilot Instructions for MCP Control Center

## Project Overview

You are working inside the **MCP Control Center** — a FastAPI + HTMX + Tailwind web platform for managing multi-language software projects through the Model Control Protocol (MCP).

## Core Goals

1. **Modern, Responsive Interface**: Provide a mobile-first (iPhone/iPad/desktop) interface for listing, editing, and tracking Features, Specifications, Refactors, ADRs, and Rules across multiple projects.

2. **MCP Integration**: Integrate tightly with MCP APIs to:
   - Read project metadata
   - Receive AI Agent updates
   - Push structured proposals or refactor plans

3. **Professional Engineering Practices**: Enforce separation of concerns, clean architecture, and typed, testable code.

4. **AI Integration**: Optionally use a remote lightweight AI model (via API) to generate design prompts and code specs for Jarvis or related systems.

## Technology Stack

### Backend
- **Python 3.12+** with FastAPI
- **SQLModel** for data models
- **SQLite** by default (PostgreSQL optional)
- Type hints throughout (enforced by mypy)

### Frontend
- **Jinja2** templates
- **HTMX** for dynamic interactions
- **Alpine.js** for client-side interactivity
- **TailwindCSS** for styling
- **NO React, Next.js, or other large frameworks**

## Code Organization

Organize code into small, typed modules:

```
app/
├── api/          # API routes and endpoints
├── services/     # Business logic and integrations
├── models/       # SQLModel data models
├── templates/    # Jinja2 templates
└── static/       # CSS, JS, images
```

## Coding Standards

### Python Standards
1. **PEP 8**: Follow PEP 8 style guidelines
2. **Black**: Use Black for code formatting
3. **Ruff**: Use Ruff for linting
4. **MyPy**: Maintain full type hints and check with mypy
5. **Pytest**: Write tests using pytest conventions

### Code Quality
- Full type hints on all functions and methods
- Docstrings for all public functions, classes, and modules
- Separation between domain logic, presentation, and integration layers
- Small, focused modules (prefer composition over large classes)

### Example Code Style
```python
from typing import Optional
from sqlmodel import SQLModel, Field

class Feature(SQLModel, table=True):
    """Represents a feature in the project tracking system.
    
    Attributes:
        id: Unique identifier for the feature
        title: Short descriptive title
        description: Detailed feature description
        status: Current status (draft, active, completed)
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=200)
    description: str
    status: str = Field(default="draft")

async def create_feature(feature: Feature) -> Feature:
    """Create a new feature in the database.
    
    Args:
        feature: Feature object to create
        
    Returns:
        Created feature with assigned ID
        
    Raises:
        ValueError: If feature data is invalid
    """
    # Implementation here
    pass
```

## Development Guidelines

### When Making Changes

1. **Propose Small Commits**: Create small, focused commits or PRs
2. **Include Tests**: Every new feature should have corresponding tests
3. **Add Documentation**: Include docstrings and comments explaining architectural intent
4. **Maintain Separation**: Keep domain logic separate from presentation and integration

### When Unsure

- Propose changes with reasoning in comments
- Ask for clarification rather than making assumptions
- Consider long-term maintainability and AI extensibility

### For New Features

1. Start with data models (`app/models/`)
2. Add business logic (`app/services/`)
3. Create API endpoints (`app/api/`)
4. Design templates with HTMX (`app/templates/`)
5. Style with Tailwind CSS
6. Write tests (`tests/`)

## Frontend Guidelines

### Mobile-First Design
- Design for iPhone/iPad first, then adapt for desktop
- Use responsive Tailwind utilities
- Test on multiple screen sizes

### HTMX Patterns
- Use `hx-get`, `hx-post` for dynamic updates
- Leverage `hx-target` and `hx-swap` for partial updates
- Keep JavaScript minimal with Alpine.js for local state

### UI/UX Principles
- Clean, elegant, and professional appearance
- Fast loading and interaction
- Accessible (ARIA labels, keyboard navigation, semantic HTML)
- Consistent spacing and typography

## MCP Integration

### Key Integration Points

1. **MCP Client Service** (`app/services/mcp_client.py`):
   - Read project metadata
   - Subscribe to AI Agent updates
   - Push structured proposals

2. **Structured Prompts**:
   - Generate design prompts for AI agents
   - Create code specifications for Jarvis
   - Format refactor plans for MCP consumption

### Integration Patterns
```python
from app.services.mcp_client import MCPClient

async def sync_project_metadata(project_id: int) -> dict:
    """Fetch and sync project metadata from MCP.
    
    Args:
        project_id: ID of the project to sync
        
    Returns:
        Dict containing synced metadata
    """
    client = MCPClient()
    return await client.get_project_metadata(project_id)
```

## Testing Strategy

### Test Types
1. **Unit Tests**: Test individual functions and classes
2. **Integration Tests**: Test API endpoints and database interactions
3. **E2E Tests**: Test critical user flows with HTMX interactions

### Test Structure
```python
import pytest
from app.models import Feature

def test_create_feature():
    """Test feature creation with valid data."""
    feature = Feature(
        title="New Feature",
        description="Test description"
    )
    assert feature.title == "New Feature"
    assert feature.status == "draft"

@pytest.mark.asyncio
async def test_feature_api_endpoint(client):
    """Test feature creation via API."""
    response = await client.post(
        "/api/features",
        json={"title": "Test", "description": "Test desc"}
    )
    assert response.status_code == 201
```

## Reference Files

- **README.md**: Project overview and setup instructions
- **ARCHITECTURE.md**: Detailed architecture and design decisions
- **app/services/mcp_client.py**: MCP integration reference

## Style and Philosophy

- **Clean and Modular**: Prefer small, focused modules
- **Professional**: Enterprise-grade code quality
- **Maintainable**: Write code that's easy to understand and modify
- **AI-Extensible**: Design with future AI integrations in mind
- **Documentation**: Clear docstrings and architectural comments

## Common Patterns

### API Endpoints
```python
from fastapi import APIRouter, HTTPException
from app.models import Feature

router = APIRouter(prefix="/api/features", tags=["features"])

@router.get("/{feature_id}")
async def get_feature(feature_id: int) -> Feature:
    """Retrieve a feature by ID.
    
    Args:
        feature_id: ID of the feature to retrieve
        
    Returns:
        Feature object
        
    Raises:
        HTTPException: If feature not found
    """
    # Implementation
    pass
```

### Service Layer
```python
from typing import List
from app.models import Feature

class FeatureService:
    """Service for managing features."""
    
    async def list_features(
        self,
        project_id: int,
        status: Optional[str] = None
    ) -> List[Feature]:
        """List features for a project.
        
        Args:
            project_id: ID of the project
            status: Optional status filter
            
        Returns:
            List of features matching criteria
        """
        # Implementation
        pass
```

### HTMX Templates
```html
<!-- Feature list with dynamic updates -->
<div id="feature-list" 
     hx-get="/features" 
     hx-trigger="load"
     hx-swap="innerHTML">
    <!-- Content loaded dynamically -->
</div>

<!-- Feature creation form -->
<form hx-post="/api/features" 
      hx-target="#feature-list" 
      hx-swap="beforeend">
    <input type="text" name="title" required 
           class="w-full px-3 py-2 border rounded-lg">
    <button type="submit" 
            class="bg-blue-500 text-white px-4 py-2 rounded-lg">
        Create Feature
    </button>
</form>
```

## Remember

- Mobile-first, responsive design always
- Type hints and tests are not optional
- Separate concerns: domain, presentation, integration
- Clean, professional, maintainable code
- AI extensibility in mind for future enhancements
