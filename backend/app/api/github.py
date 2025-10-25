"""GitHub integration API routes."""

from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.database import get_session
from app.models import Project
from app.services.github_service import GitHubService, get_github_service

router = APIRouter(prefix="/api/github", tags=["github"])


@router.get("/config")
async def get_github_config(
    github_service: GitHubService = Depends(get_github_service),
) -> dict[str, Any]:
    """Get GitHub configuration status."""
    return {
        "enabled": bool(github_service.token),
        "has_token": bool(github_service.token),
    }


@router.get("/repositories")
async def list_github_repositories(
    user: Optional[str] = None, github_service: GitHubService = Depends(get_github_service)
) -> list[dict[str, Any]]:
    """List GitHub repositories."""
    if not github_service.token:
        raise HTTPException(status_code=401, detail="GitHub token not configured")

    try:
        repos = await github_service.list_repositories(user)
        return repos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch repositories: {str(e)}")


@router.post("/sync")
async def sync_from_github(
    session: AsyncSession = Depends(get_session),
    github_service: GitHubService = Depends(get_github_service),
) -> dict[str, Any]:
    """Sync projects from GitHub repositories."""
    if not github_service.token:
        raise HTTPException(status_code=401, detail="GitHub token not configured")

    try:
        # Fetch repositories from GitHub
        repos = await github_service.list_repositories()

        synced_count = 0
        created_count = 0

        for repo in repos:
            # Check if project already exists
            result = await session.execute(
                select(Project).where(Project.repo_url == repo["html_url"])
            )
            existing_project = result.scalar_one_or_none()

            if existing_project:
                # Update existing project
                existing_project.name = repo["name"]
                existing_project.tags = repo.get("topics", [])
                synced_count += 1
            else:
                # Create new project
                languages = await github_service.list_repository_languages(
                    repo["owner"]["login"], repo["name"]
                )
                language_matrix = {lang: "" for lang in languages.keys()}

                new_project = Project(
                    name=repo["name"],
                    repo_url=repo["html_url"],
                    language_matrix=language_matrix,
                    tags=repo.get("topics", []),
                )
                session.add(new_project)
                created_count += 1

        await session.commit()

        return {
            "status": "success",
            "synced": synced_count,
            "created": created_count,
            "total": len(repos),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sync failed: {str(e)}")


@router.post("/repositories")
async def create_github_repository(
    name: str,
    description: str = "",
    private: bool = False,
    session: AsyncSession = Depends(get_session),
    github_service: GitHubService = Depends(get_github_service),
) -> dict[str, Any]:
    """Create a new GitHub repository and corresponding project."""
    if not github_service.token:
        raise HTTPException(status_code=401, detail="GitHub token not configured")

    try:
        # Create repository on GitHub
        repo = await github_service.create_repository(name, description, private)

        # Create project in database
        project = Project(
            name=repo["name"],
            repo_url=repo["html_url"],
            language_matrix={},
            tags=[],
        )
        session.add(project)
        await session.commit()
        await session.refresh(project)

        return {
            "status": "success",
            "project": project,
            "github_repo": {
                "url": repo["html_url"],
                "clone_url": repo["clone_url"],
            },
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create repository: {str(e)}"
        )
