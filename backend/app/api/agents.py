"""Agent activity API routes with SSE support."""

import asyncio
import json
from datetime import datetime
from typing import AsyncGenerator, Optional

from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.database import get_session
from app.models import AgentUpdate

router = APIRouter(prefix="/api/agents", tags=["agents"])


async def agent_event_generator(
    project_id: Optional[int] = None,
) -> AsyncGenerator[str, None]:
    """Generate Server-Sent Events for agent updates."""
    # Send initial connection message
    yield f"data: {json.dumps({'type': 'connected', 'timestamp': datetime.utcnow().isoformat()})}\n\n"

    # In a real implementation, this would listen to a message queue or database changes
    # For now, we'll simulate with periodic checks
    last_check = datetime.utcnow()

    while True:
        await asyncio.sleep(5)  # Check every 5 seconds

        # Simulated event - in production, fetch actual new updates from database
        event_data = {
            "type": "heartbeat",
            "timestamp": datetime.utcnow().isoformat(),
            "message": "Listening for agent updates...",
        }

        yield f"data: {json.dumps(event_data)}\n\n"


@router.get("/stream")
async def stream_agent_updates(
    project_id: Optional[int] = Query(None),
) -> StreamingResponse:
    """Stream agent updates via Server-Sent Events."""
    return StreamingResponse(
        agent_event_generator(project_id),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # Disable buffering in nginx
        },
    )


@router.get("/recent")
async def get_recent_updates(
    project_id: Optional[int] = Query(None),
    limit: int = Query(10, le=100),
    session: AsyncSession = Depends(get_session),
) -> list[dict]:
    """Get recent agent updates."""
    query = select(AgentUpdate).order_by(AgentUpdate.created_at.desc()).limit(limit)

    if project_id:
        query = query.where(AgentUpdate.project_id == project_id)

    result = await session.execute(query)
    updates = result.scalars().all()

    return [
        {
            "id": update.id,
            "project_id": update.project_id,
            "source": update.source,
            "payload": update.payload_json,
            "created_at": update.created_at.isoformat(),
        }
        for update in updates
    ]
