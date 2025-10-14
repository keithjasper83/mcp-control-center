"""Main FastAPI application."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api import adrs, agents, documents, features, github, mcp, projects, proposals, refactors, reports, rules, specs
from app.config import get_settings
from app.database import init_db

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager."""
    # Startup
    await init_db()
    yield
    # Shutdown
    pass


app = FastAPI(
    title="MCP Control Center",
    description="Modern web control center for managing multi-language projects with MCP integration",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(projects.router)
app.include_router(features.router)
app.include_router(specs.router)
app.include_router(refactors.router)
app.include_router(adrs.router)
app.include_router(rules.router)
app.include_router(proposals.router)
app.include_router(reports.router)
app.include_router(agents.router)
app.include_router(documents.router)
app.include_router(mcp.router)
app.include_router(github.router)

# Mount static files
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Templates
templates = Jinja2Templates(directory="frontend/templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request) -> HTMLResponse:
    """Root page."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/projects", response_class=HTMLResponse)
async def projects_page(request: Request) -> HTMLResponse:
    """Projects page."""
    return templates.TemplateResponse("projects.html", {"request": request})


@app.get("/features", response_class=HTMLResponse)
async def features_page(request: Request) -> HTMLResponse:
    """Features page."""
    return templates.TemplateResponse("features.html", {"request": request})


@app.get("/documents", response_class=HTMLResponse)
async def documents_page(request: Request) -> HTMLResponse:
    """Documentation ingestion page."""
    return templates.TemplateResponse("documents.html", {"request": request})


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}
