"""Feature API routes."""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.database import get_session
from app.models import Feature

router = APIRouter(prefix="/api/features", tags=["features"])


@router.get("", response_model=List[Feature])
async def list_features(
    project_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    label: Optional[str] = Query(None),
    session: AsyncSession = Depends(get_session),
) -> List[Feature]:
    """List features with optional filters."""
    query = select(Feature)

    if project_id:
        query = query.where(Feature.project_id == project_id)
    if status:
        query = query.where(Feature.status == status)

    result = await session.execute(query)
    features = result.scalars().all()

    # Filter by label if provided (client-side filtering for JSON array)
    if label:
        features = [f for f in features if label in f.labels]

    return features


@router.post("", response_model=Feature)
async def create_feature(
    feature: Feature, session: AsyncSession = Depends(get_session)
) -> Feature:
    """Create a new feature."""
    session.add(feature)
    await session.commit()
    await session.refresh(feature)
    return feature


@router.get("/{feature_id}", response_model=Feature)
async def get_feature(
    feature_id: int, session: AsyncSession = Depends(get_session)
) -> Feature:
    """Get a specific feature."""
    feature = await session.get(Feature, feature_id)
    if not feature:
        raise HTTPException(status_code=404, detail="Feature not found")
    return feature


@router.patch("/{feature_id}", response_model=Feature)
async def update_feature(
    feature_id: int, feature_update: dict, session: AsyncSession = Depends(get_session)
) -> Feature:
    """Update a feature."""
    feature = await session.get(Feature, feature_id)
    if not feature:
        raise HTTPException(status_code=404, detail="Feature not found")

    for key, value in feature_update.items():
        if hasattr(feature, key):
            setattr(feature, key, value)

    await session.commit()
    await session.refresh(feature)
    return feature
