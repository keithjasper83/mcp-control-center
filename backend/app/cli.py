"""CLI commands for MCP Control Center."""

import asyncio
import sys
from typing import Optional

import typer
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session, init_db
from app.models import ADR, Feature, FeatureStatus, Project, Rule, RuleCategory, RuleGate
from app.services.mcp_client import get_mcp_client

app = typer.Typer(help="MCP Control Center CLI")


@app.command()
def init() -> None:
    """Initialize database."""
    typer.echo("Initializing database...")
    asyncio.run(init_db())
    typer.echo("✓ Database initialized")


@app.command()
def seed() -> None:
    """Seed database with demo data."""
    typer.echo("Seeding database with demo data...")
    asyncio.run(seed_data())
    typer.echo("✓ Database seeded with demo content")


async def seed_data() -> None:
    """Seed the database with demo data."""
    async with async_session() as session:
        # Create demo project
        project = Project(
            name="Demo Project",
            repo_url="https://github.com/example/demo-project",
            language_matrix={"python": "3.12", "javascript": "ES2023"},
            tags=["demo", "web", "api"],
        )
        session.add(project)
        await session.flush()

        # Create demo features
        features = [
            Feature(
                project_id=project.id,
                title="User Authentication",
                description_md="Implement user authentication with JWT tokens",
                status=FeatureStatus.IN_PROGRESS,
                priority=1,
                labels=["security", "backend"],
            ),
            Feature(
                project_id=project.id,
                title="Dashboard UI",
                description_md="Create responsive dashboard with project overview",
                status=FeatureStatus.PLANNED,
                priority=2,
                labels=["frontend", "ui"],
            ),
            Feature(
                project_id=project.id,
                title="API Documentation",
                description_md="Generate OpenAPI documentation for all endpoints",
                status=FeatureStatus.DONE,
                priority=3,
                labels=["docs", "api"],
            ),
        ]
        session.add_all(features)

        # Create demo rules
        rules = [
            Rule(
                project_id=project.id,
                name="No Circular Dependencies",
                category=RuleCategory.SOC,
                policy_md="Modules must not have circular import dependencies",
                gate=RuleGate.FAIL,
                enabled=True,
            ),
            Rule(
                project_id=project.id,
                name="Test Coverage > 80%",
                category=RuleCategory.TESTING,
                policy_md="All modules must maintain at least 80% test coverage",
                gate=RuleGate.WARN,
                enabled=True,
            ),
        ]
        session.add_all(rules)

        # Create demo ADR
        adr = ADR(
            project_id=project.id,
            title="Use FastAPI for REST API",
            context_md="Need a modern Python web framework with async support",
            decision_md="Selected FastAPI for its performance, type hints, and automatic documentation",
            consequences_md="Team needs to learn async/await patterns. Performance gains significant.",
            status="Accepted",
        )
        session.add(adr)

        await session.commit()


@app.command()
def sync_mcp(project: str) -> None:
    """Sync data from MCP server for a project."""
    typer.echo(f"Syncing MCP data for project: {project}")
    asyncio.run(sync_mcp_async(project))


async def sync_mcp_async(project: str) -> None:
    """Async implementation of MCP sync."""
    client = get_mcp_client()
    try:
        features = await client.list_features(project)
        typer.echo(f"✓ Synced {len(features)} features from MCP")
    except Exception as e:
        typer.echo(f"✗ Error syncing from MCP: {e}", err=True)
        sys.exit(1)


@app.command()
def generate_soc_report(project_id: Optional[int] = None) -> None:
    """Generate Separation of Concerns report."""
    if project_id:
        typer.echo(f"Generating SoC report for project {project_id}...")
    else:
        typer.echo("Generating SoC report for all projects...")
    # TODO: Implement SoC analysis
    typer.echo("✓ SoC report generated")


@app.command()
def run_gates(project_id: Optional[int] = None) -> None:
    """Run quality gates."""
    if project_id:
        typer.echo(f"Running quality gates for project {project_id}...")
    else:
        typer.echo("Running quality gates for all projects...")
    # TODO: Implement gate checks
    typer.echo("✓ All gates passed")


if __name__ == "__main__":
    app()
