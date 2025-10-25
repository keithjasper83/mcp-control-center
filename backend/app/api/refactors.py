"""Refactor plan API routes."""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.database import get_session
from app.models import RefactorPlan

router = APIRouter(prefix="/api/refactors", tags=["refactors"])


@router.get("", response_model=List[RefactorPlan])
async def list_refactors(
    project_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    session: AsyncSession = Depends(get_session),
) -> List[RefactorPlan]:
    """List refactor plans with optional filters."""
    query = select(RefactorPlan)

    if project_id:
        query = query.where(RefactorPlan.project_id == project_id)
    if status:
        query = query.where(RefactorPlan.status == status)

    result = await session.execute(query)
    return result.scalars().all()


@router.post("", response_model=RefactorPlan)
async def create_refactor(
    refactor: RefactorPlan, session: AsyncSession = Depends(get_session)
) -> RefactorPlan:
    """Create a new refactor plan."""
    session.add(refactor)
    await session.commit()
    await session.refresh(refactor)
    return refactor


@router.get("/{refactor_id}", response_model=RefactorPlan)
async def get_refactor(
    refactor_id: int, session: AsyncSession = Depends(get_session)
) -> RefactorPlan:
    """Get a specific refactor plan."""
    refactor = await session.get(RefactorPlan, refactor_id)
    if not refactor:
        raise HTTPException(status_code=404, detail="Refactor plan not found")
    return refactor


@router.patch("/{refactor_id}", response_model=RefactorPlan)
async def update_refactor(
    refactor_id: int, refactor_update: dict, session: AsyncSession = Depends(get_session)
) -> RefactorPlan:
    """Update a refactor plan."""
    refactor = await session.get(RefactorPlan, refactor_id)
    if not refactor:
        raise HTTPException(status_code=404, detail="Refactor plan not found")

    for key, value in refactor_update.items():
        if hasattr(refactor, key):
            setattr(refactor, key, value)

    await session.commit()
    await session.refresh(refactor)
    return refactor
