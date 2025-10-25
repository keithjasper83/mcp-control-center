"""Specification API routes."""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.database import get_session
from app.models import Specification

router = APIRouter(prefix="/api/specs", tags=["specs"])


@router.get("", response_model=List[Specification])
async def list_specs(
    project_id: Optional[int] = Query(None),
    kind: Optional[str] = Query(None),
    session: AsyncSession = Depends(get_session),
) -> List[Specification]:
    """List specifications with optional filters."""
    query = select(Specification)

    if project_id:
        query = query.where(Specification.project_id == project_id)
    if kind:
        query = query.where(Specification.kind == kind)

    result = await session.execute(query)
    return result.scalars().all()


@router.post("", response_model=Specification)
async def create_spec(
    spec: Specification, session: AsyncSession = Depends(get_session)
) -> Specification:
    """Create a new specification."""
    session.add(spec)
    await session.commit()
    await session.refresh(spec)
    return spec


@router.get("/{spec_id}", response_model=Specification)
async def get_spec(spec_id: int, session: AsyncSession = Depends(get_session)) -> Specification:
    """Get a specific specification."""
    spec = await session.get(Specification, spec_id)
    if not spec:
        raise HTTPException(status_code=404, detail="Specification not found")
    return spec


@router.patch("/{spec_id}", response_model=Specification)
async def update_spec(
    spec_id: int, spec_update: dict, session: AsyncSession = Depends(get_session)
) -> Specification:
    """Update a specification."""
    spec = await session.get(Specification, spec_id)
    if not spec:
        raise HTTPException(status_code=404, detail="Specification not found")

    for key, value in spec_update.items():
        if hasattr(spec, key):
            setattr(spec, key, value)

    await session.commit()
    await session.refresh(spec)
    return spec
