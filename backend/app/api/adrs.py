"""ADR (Architecture Decision Record) API routes."""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.database import get_session
from app.models import ADR

router = APIRouter(prefix="/api/adrs", tags=["adrs"])


@router.get("", response_model=List[ADR])
async def list_adrs(
    project_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    session: AsyncSession = Depends(get_session),
) -> List[ADR]:
    """List ADRs with optional filters."""
    query = select(ADR)

    if project_id:
        query = query.where(ADR.project_id == project_id)
    if status:
        query = query.where(ADR.status == status)

    result = await session.execute(query)
    return result.scalars().all()


@router.post("", response_model=ADR)
async def create_adr(adr: ADR, session: AsyncSession = Depends(get_session)) -> ADR:
    """Create a new ADR."""
    session.add(adr)
    await session.commit()
    await session.refresh(adr)
    return adr


@router.get("/{adr_id}", response_model=ADR)
async def get_adr(adr_id: int, session: AsyncSession = Depends(get_session)) -> ADR:
    """Get a specific ADR."""
    adr = await session.get(ADR, adr_id)
    if not adr:
        raise HTTPException(status_code=404, detail="ADR not found")
    return adr


@router.patch("/{adr_id}", response_model=ADR)
async def update_adr(
    adr_id: int, adr_update: dict, session: AsyncSession = Depends(get_session)
) -> ADR:
    """Update an ADR."""
    adr = await session.get(ADR, adr_id)
    if not adr:
        raise HTTPException(status_code=404, detail="ADR not found")

    for key, value in adr_update.items():
        if hasattr(adr, key):
            setattr(adr, key, value)

    await session.commit()
    await session.refresh(adr)
    return adr
