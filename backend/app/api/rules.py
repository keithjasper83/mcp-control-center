"""Rules API routes."""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.database import get_session
from app.models import Rule

router = APIRouter(prefix="/api/rules", tags=["rules"])


@router.get("", response_model=List[Rule])
async def list_rules(
    project_id: Optional[int] = Query(None),
    category: Optional[str] = Query(None),
    enabled: Optional[bool] = Query(None),
    session: AsyncSession = Depends(get_session),
) -> List[Rule]:
    """List rules with optional filters."""
    query = select(Rule)

    if project_id:
        query = query.where(Rule.project_id == project_id)
    if category:
        query = query.where(Rule.category == category)
    if enabled is not None:
        query = query.where(Rule.enabled == enabled)

    result = await session.execute(query)
    return result.scalars().all()


@router.post("", response_model=Rule)
async def create_rule(rule: Rule, session: AsyncSession = Depends(get_session)) -> Rule:
    """Create a new rule."""
    session.add(rule)
    await session.commit()
    await session.refresh(rule)
    return rule


@router.get("/{rule_id}", response_model=Rule)
async def get_rule(rule_id: int, session: AsyncSession = Depends(get_session)) -> Rule:
    """Get a specific rule."""
    rule = await session.get(Rule, rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    return rule


@router.patch("/{rule_id}", response_model=Rule)
async def update_rule(
    rule_id: int, rule_update: dict, session: AsyncSession = Depends(get_session)
) -> Rule:
    """Update a rule."""
    rule = await session.get(Rule, rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")

    for key, value in rule_update.items():
        if hasattr(rule, key):
            setattr(rule, key, value)

    await session.commit()
    await session.refresh(rule)
    return rule
