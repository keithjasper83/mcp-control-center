"""MCP integration API routes."""

from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models import AgentUpdate, UpdateSource
from app.services.mcp_client import get_mcp_client, MCPClient

router = APIRouter(prefix="/api/mcp", tags=["mcp"])


@router.get("/config")
async def get_mcp_config(client: MCPClient = Depends(get_mcp_client)) -> dict[str, Any]:
    """Get MCP configuration."""
    return {
        "base_url": client.base_url,
        "has_token": bool(client.token),
    }


@router.post("/updates")
async def receive_update(
    update_data: dict[str, Any], session: AsyncSession = Depends(get_session)
) -> dict[str, str]:
    """Receive updates from MCP agents."""
    project_id = update_data.get("project_id")
    if not project_id:
        raise HTTPException(status_code=400, detail="project_id is required")

    agent_update = AgentUpdate(
        project_id=project_id,
        source=UpdateSource.MCP,
        payload_json=update_data,
    )

    session.add(agent_update)
    await session.commit()

    return {"status": "received", "id": str(agent_update.id)}


@router.post("/sync")
async def sync_from_mcp(
    project: str, client: MCPClient = Depends(get_mcp_client)
) -> dict[str, Any]:
    """Sync features and specs from MCP server."""
    try:
        features = await client.list_features(project)
        return {
            "status": "synced",
            "project": project,
            "features_count": len(features),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sync failed: {str(e)}")
