"""Project API routes."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.database import get_session
from app.models import Project

router = APIRouter(prefix="/api/projects", tags=["projects"])


@router.get("", response_model=List[Project])
async def list_projects(session: AsyncSession = Depends(get_session)) -> List[Project]:
    """List all projects."""
    result = await session.execute(select(Project))
    return result.scalars().all()


@router.post("", response_model=Project)
async def create_project(
    project: Project, session: AsyncSession = Depends(get_session)
) -> Project:
    """Create a new project."""
    session.add(project)
    await session.commit()
    await session.refresh(project)
    return project


@router.get("/{project_id}", response_model=Project)
async def get_project(
    project_id: int, session: AsyncSession = Depends(get_session)
) -> Project:
    """Get a specific project."""
    project = await session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.patch("/{project_id}", response_model=Project)
async def update_project(
    project_id: int, project_update: dict, session: AsyncSession = Depends(get_session)
) -> Project:
    """Update a project."""
    project = await session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    for key, value in project_update.items():
        if hasattr(project, key):
            setattr(project, key, value)

    await session.commit()
    await session.refresh(project)
    return project
